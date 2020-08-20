import os
import time
import dash_table
import datetime as dt
import pandas as pd
import dash_core_components as dcc
import plotly.graph_objs as go 
from dash.dependencies import Input, Output
from app import app

FILE = os.environ['DASH_FILE_NAME']
def refresher():
    date_format='%d-%m-%Y %H:%M'
    file_time_class = os.stat(FILE)
    file_time = time.strftime(date_format,time.localtime(file_time_class.st_mtime))
    df = pd.read_csv(FILE)
    df_grouped = pd.read_csv(FILE).groupby(['DATE','QUERY_RAW_PHRASE']).agg(
        min_logtime=('LOG_TIME',min),
        max_logtime=('LOG_TIME',max),
        mean_logtime=('LOG_TIME',"mean")).reset_index()
    return date_format, file_time, df, df_grouped

@app.callback([
    Output('phrase_dd_menu','options'),
    Output('phrase_dd_menu','value')],
    [Input('type_dd_menu','value')])

def return_phrase_dd(type_value):
    date_format, file_time, df, df_grouped = refresher()
    phrases = df_grouped['QUERY_RAW_PHRASE'].unique()
    options=[{'label':uniq_phrase, 'value':uniq_phrase} for uniq_phrase in phrases]
    value=phrases[0]
    return options, value

@app.callback(
    Output('search-time-graph-div','children'),
    [Input('phrase_dd_menu', 'value'),
    Input('type_dd_menu','value'),
    Input('global-interval','n_intervals'),
    Input('date-range-picker','end_date'),
    Input('date-range-picker','start_date'),
    Input('radio_graph_picker','value')])

def update_graph(phrase_value,type_value,n,end_date,start_date,radio_graph_value):
    date_format, file_time, df, df_grouped = refresher()
    if type_value == 'daily': 
        ddf = df_grouped[df_grouped['QUERY_RAW_PHRASE'] == phrase_value]
        ddf = ddf.set_index('DATE')
        ddf.index = pd.to_datetime(ddf.index)
        ddf = ddf.asfreq('D').assign(QUERY_RAW_PHRASE=lambda x: x['QUERY_RAW_PHRASE'].ffill())
        ddf = ddf.loc[start_date:end_date]
        return [
            dcc.Graph(
                id='search-time-graph',
                figure={
                    'data': [
                        {'x': ddf.index, 'y': ddf['min_logtime'], 'type': radio_graph_value , 'name': 'Min','visible': 'legendonly', 'connectgaps': False,},
                        {'x': ddf.index, 'y': ddf['mean_logtime'], 'type': radio_graph_value , 'name': 'Avg', 'connectgaps': False,},
                        {'x': ddf.index, 'y': ddf['max_logtime'], 'type': radio_graph_value , 'name': 'Max', 'visible': 'legendonly', 'connectgaps': False},
                    ],
                    'layout': {
                        'title': f'Czas wyszukiwania {phrase_value}, - {file_time}',
                        'bargap': 0.02
                    },
                }
            )
        ]
    elif type_value == '15-min':
        date_format, file_time, df, df_grouped = refresher()
        ddf = df[df['QUERY_RAW_PHRASE'] == phrase_value]
        ddf['DATE_TIME'] = ddf['DATE'] + ' ' + ddf['TIME']
        ddf = ddf.drop(['DATE','TIME'], axis=1)
        pd.to_datetime(ddf['DATE_TIME'])
        return [
            dcc.Graph(
                id='search-time-graph',
                figure={
                    'data': [
                        {'x': ddf['DATE_TIME'], 'y': ddf['LOG_TIME'], 'type': radio_graph_value , 'name': 'Log time', 'connectgaps': False},
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
    date_format, file_time, df, df3 = refresher()
    return [
        dash_table.DataTable(
            id='hana_raw_data',
            data = df[df['QUERY_RAW_PHRASE'] == dd_menu_value].to_dict('records'),
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