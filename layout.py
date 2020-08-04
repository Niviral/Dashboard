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
<<<<<<< HEAD
            width='40vw',
=======
            width='25vw',
>>>>>>> 93748199de5475a27a78f0922a145f4bc20bbf84
            display = 'table-cell',
            left=0
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
<<<<<<< HEAD
            width='20vw',
            display = 'table-cell',
            right=True,
        ))
    ],id='nav-bar-div'),
=======
            width='25vw',
            display = 'table-cell',
        ))
    ],id='dd_div'),
>>>>>>> 93748199de5475a27a78f0922a145f4bc20bbf84
    html.Div(id='search-time-graph-div'),
    html.Div(id='search-time-date-slider'),
    html.Div(id='search-time-dt-div'),
    html.Div([
        dcc.Interval(
            id='global-interval',
            interval=1*1200000,
            n_intervals=0
        )
    ],
    id='interval-div',
    style={'display': 'none'}),
    html.Div(id='tricky-div', style={'display': 'none'}),
],
style=dict(
    width='98%',
    height='99%',
    overflowX='hidden',
    scroll='no'
))