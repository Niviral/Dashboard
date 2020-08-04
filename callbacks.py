import os
import time
import dash_table
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app

date_format='%d-%m-%Y %H:%M'
file_time_class = os.stat(os.environ['DASH_FILE_NAME'])
file_time = time.strftime(date_format,time.localtime(file_time_class.st_mtime))
df = pd.read_csv(os.environ['DASH_FILE_NAME'])
df3 = pd.read_csv(os.environ['DASH_FILE_NAME']).groupby(['DATE','QUERY_RAW_PHRASE']).agg(
    min_logtime=('LOG_TIME',min),
    max_logtime=('LOG_TIME',max),
    mean_logtime=('LOG_TIME',"mean")).reset_index()

@app.callback(
    Output('phrase_dd_menu','options'),
    [Input('type_dd_menu','value')])

def retrun_phrase_dd(type_value):
    phrases = df3['QUERY_RAW_PHRASE'].unique()
    return [{'label':uniq_phrase, 'value':uniq_phrase} for uniq_phrase in phrases ]
        
@app.callback(
    Output('search-time-graph-div','children'),
    [Input('phrase_dd_menu', 'value'),
    Input('type_dd_menu','value'),
    Input('global-interval','n_intervals')])

def update_graph(phrase_value,type_value,n):
    if type_value == 'daily': 
        ddf = df3[df3['QUERY_RAW_PHRASE']==phrase_value]
        ddf = ddf.set_index('DATE')
        ddf.index = pd.to_datetime(ddf.index)
        ddf = ddf.asfreq('D').assign(QUERY_RAW_PHRASE=lambda x: x['QUERY_RAW_PHRASE'].ffill())
        return [
            dcc.Graph(
                id='search-time-graph',
                figure={
                    'data': [
                        {'x': ddf.index, 'y': ddf['mean_logtime'], 'type': 'line' , 'name': 'Avg', 'connectgaps': False},
                        {'x': ddf.index, 'y': ddf['min_logtime'], 'type': 'line' , 'name': 'Min', 'connectgaps': False},
                        {'x': ddf.index, 'y': ddf['max_logtime'], 'type': 'line' , 'name': 'Max', 'visible': 'legendonly', 'connectgaps': False},
                    
                    ],
                    'layout': {
                        'title': f'Czas wyszukiwania {phrase_value} - {file_time}'
                    }
                }
                )
        ]
    elif type_value =='15-min': 
        ddf = df[df['QUERY_RAW_PHRASE']==phrase_value]
        ddf['DATE_TIME'] = ddf['DATE'] +' '+ ddf['TIME']
        ddf = ddf.drop(['DATE','TIME'], axis=1)
        pd.to_datetime(ddf['DATE_TIME'])
        return [
            dcc.Graph(
                id='search-time-graph',
                figure={
                    'data': [
                        {'x': ddf['DATE_TIME'], 'y': ddf['LOG_TIME'], 'type': 'line' , 'name': 'Log time', 'connectgaps': False},
                    ],
                    'layout': {
                        'title': f'Czas wyszukiwania {phrase_value}, - {file_time}'
                    }
                }
                )
        ]
    else:
        pass
@app.callback(
    Output('search-time-dt-div','children'),
    [Input('phrase_dd_menu', 'value'),
    Input('global-interval','n_intervals')])

def update_table(dd_menu_value,n):
    return [
        dash_table.DataTable(
            id='hana_raw_data',
            data = df[df['QUERY_RAW_PHRASE']==dd_menu_value].to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            fixed_rows={'headers':True},
            style_table=dict(
                height='40vh',
                overflowY='auto'),
            page_size=50,
            filter_action='native',
            sort_action='native',
            style_data={
                'whiteSpace': 'normal',
                'height': '15px',
                'lineHeight': '15px',
                'padding' : '0px'
            }
        )
    ]
 
### \/ THIS NEED TO BE FIXED ###
@app.callback(
    Output('tricky-div','children'),
    [Input('global-interval','n_intervals')])

def refresher(n):
    df = pd.read_csv(os.environ['DASH_FILE_NAME'])
    df3 = pd.read_csv(os.environ['DASH_FILE_NAME']).groupby(['DATE','QUERY_RAW_PHRASE']).agg(
        min_logtime=('LOG_TIME',min),
        max_logtime=('LOG_TIME',max),
        mean_logtime=('LOG_TIME',"mean")).reset_index()
    file_time_class = os.stat(os.environ['DASH_FILE_NAME'])
    file_time = time.asctime(time.localtime(file_time_class.st_mtime))