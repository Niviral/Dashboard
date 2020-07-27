import pandas as pd
import os
import time
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

date_format='%d-%m-%Y %H:%M'
file_time_class = os.stat('hana_search.csv')
file_time = time.strftime(date_format,time.localtime(file_time_class.st_mtime))
df = pd.read_csv('hana_search.csv')
df3 = pd.read_csv('hana_search.csv').groupby(['DATE','QUERY_RAW_PHRASE']).agg(
    min_logtime=('LOG_TIME',min),
    max_logtime=('LOG_TIME',max),
    mean_logtime=('LOG_TIME',"mean")).reset_index()




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ ,external_stylesheets=external_stylesheets)
server = app.server

phrase = df3['QUERY_RAW_PHRASE'].unique()

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dd_menu',
                options=[
                {'label': unique_phrase, 'value': unique_phrase} for unique_phrase in phrase],
                value = 'kabel',
            )
        ],
        style=dict(
            width='68%',
            display = 'table-cell',
        )),
        html.Div([
            dcc.Dropdown(
                id='dd_type',
                options=[
                {'label': 'dzienne' , 'value': 'Dzienne'},
                {'label': 'godzinowe', 'value': 'Godzinowe'}],
                value = 'Dzienne',
            )
        ],
        style=dict(
            width='68%',
            display = 'table-cell',
        )),
        html.Div([
            html.Button(f'{file_time}',id='refresh_button'),
        ],
        style=dict(
            width='30%',
            display = 'table-cell',
        )),
    ],id='dd_div'),
    html.Div(id='search-time-graph-div'),
    html.Div(id='search-time-date-slider'),
    html.Div(id='search-time-dt-div'),
    html.Div(id='tricky-div', style={'display': 'none'}),
],
style=dict(
    width='98%',
    height='99%',
    overflowX='hidden',
    scroll='no'

))

@app.callback(
    Output('search-time-graph-div','children'),
    [Input('dd_menu', 'value'),
    Input('tricky-div','children'),
    Input('dd_type','value')])

def update_graph(dd_menu_value, phrase_value,type_value):
    if type_value == 'Dzienne': 
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
    else: 
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

@app.callback(
    Output('search-time-dt-div','children'),
    [Input('dd_menu', 'value'),
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
    

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8100',debug=True)


