import os
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import time

from app import app

date_format='%d-%m-%Y %H:%M'
file_time_class = os.stat('hana_search.csv')
file_time = time.strftime(date_format,time.localtime(file_time_class.st_mtime))
df = pd.read_csv('hana_search.csv')
df3 = pd.read_csv('hana_search.csv').groupby(['DATE','QUERY_RAW_PHRASE']).agg(
    min_logtime=('LOG_TIME',min),
    max_logtime=('LOG_TIME',max),
    mean_logtime=('LOG_TIME',"mean")).reset_index()

@app.callback(
    Output('phrase_dd_menu','options'),
    [Input('none','children')])

def retrun_phrase_dd(none):
    phrase = df3['QUERY_RAW_PHRASE'].unique()
    for unique_phrase in phrase: 
        yield [{'label': unique_phrase, 'value': unique_phrase}]


@app.callback(
    Output('search-time-graph-div','children'),
    [Input('phrase_dd_menu', 'value'),
    Input('tricky-div','children'),
    Input('type_dd_menu','value')])

def update_graph(dd_menu_value, phrase_value,type_value):
    if type_value == 'daily': 
        ddf = df3[df3['QUERY_RAW_PHRASE']==dd_menu_value]
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
                        'title': f'Czas wyszukiwania {dd_menu_value}'
                    }
                }
                )
        ]
    elif type_value =='15-min': 
        ddf = df[df['QUERY_RAW_PHRASE']==dd_menu_value]
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
                        'title': f'Czas wyszukiwania {dd_menu_value}'
                    }
                }
                )
        ]
    else:
        pass
@app.callback(
    Output('search-time-dt-div','children'),
    [Input('phrase_dd_menu', 'value'),
    Input('tricky-div','children')])

def update_table(dd_menu_value,value):
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
                'height': '13px',
                'lineHeight': '13px',
                'padding' : '0px'
            }
        )
    ]

@app.callback(
    Output('tricky-div','children'),
    [Input('refresh_button','n_clicks')])

def refresher(value):
    global df
    df = pd.read_csv('hana_search.csv')
    global df3 
    df3 = pd.read_csv('hana_search.csv').groupby(['DATE','QUERY_RAW_PHRASE']).agg(
        min_logtime=('LOG_TIME',min),
        max_logtime=('LOG_TIME',max),
        mean_logtime=('LOG_TIME',"mean")).reset_index()
    global file_time_class
    file_time_class = os.stat('hana_search.csv')
    global file_time
    file_time = time.asctime(time.localtime(file_time_class.st_mtime))