import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

class BuildDF:
    def __init__(self):
        self.df = pd.read_csv('hana_search.csv')
        self.df3 = pd.read_csv('hana_search.csv').groupby(['DATE','QUERY_RAW_PHRASE']).agg(
                min_logtime=('LOG_TIME',min),
                max_logtime=('LOG_TIME',max),
                mean_logtime=('LOG_TIME',"mean")
                ).reset_index()

def get_df():
    return BuildDF()
t=get_df()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ ,external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#272b30',
    'font':'#878b90'
}

phrase = t.df3['QUERY_RAW_PHRASE'].unique()

app.layout = html.Div(children=[
    html.H1(children=''),
    html.Div([
        dcc.Dropdown(
            id='dd_menu',
            options=[
            {'label': unique_phrase, 'value': unique_phrase} for unique_phrase in phrase],
            value = 'kabel',
            style=dict(
                width='50%',
                verticalAlign='left'
            )),
        html.Button(
            'Refresh', 
            id='DF_refresh_button',
            n_clicks=0,
            style=dict(
                width='200px',
                verticalAlign='right'
            )),
    ],id='dd_div'),
    html.Div(id='search-time-graph-div'),
    html.Div(id='search-time-date-slider'),
    html.Div(id='search-time-dt-div'),
])

@app.callback(
    Output('search-time-graph-div','children'),
    [Input('dd_menu', 'value')])

def update_graph(dd_menu_value):
    ddf = t.df3[t.df3['QUERY_RAW_PHRASE']==dd_menu_value]
    yax = [ddf['mean_logtime']*1.2,ddf['mean_logtime']*0.75]

    return [
        dcc.Graph(
            id='search-time-graph',
            figure={
                'data': [
                    {'x': ddf['DATE'], 'y': ddf['mean_logtime'], 'type': 'line' , 'name': 'Avg'},
                    {'x': ddf['DATE'], 'y': ddf['min_logtime'], 'type': 'line' , 'name': 'Min'},
                    {'x': ddf['DATE'], 'y': ddf['max_logtime'], 'type': 'line' , 'name': 'Max', 'visible': 'legendonly'}
                ],
                'layout': {
                    'title': f'Czas wyszukiwania {dd_menu_value}',
                    'yaxis':{
                        'range': [yax]
                    }
                }
            }
        )
    ]
@app.callback(
    Output('search-time-dt-div','children'),
    [Input('dd_menu', 'value')])

def update_table(dd_menu_value):
    return [
        dash_table.DataTable(
            id='hana_raw_data',
            data = t.df[t.df['QUERY_RAW_PHRASE']==dd_menu_value].to_dict('records'),
            columns=[{"name": i, "id": i} for i in t.df.columns],
            page_size=10,
            filter_action='native',
            sort_action="native",
        )
    ]

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8000',debug=True)


