import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
            id='phrase_dd_menu',
            options=[],
            value = 'kabel',
            )],
        id='phrase-dropdown-div',
        style=dict(
            width='68%',
            display = 'table-cell',
        )),
        html.Div([
            dcc.Dropdown(
            id='type_dd_menu',
            options=[
            {'label': 'daily' , 'value': 'daily'},
            {'label': '15-min', 'value': '15-min'}],
            value = 'daily',
            )],
        id='type-dropdown-div',
        style=dict(
            width='68%',
            display = 'table-cell',
        )),
        html.Div([
            html.Button('Jest aktualne',id='refresh_button'),
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