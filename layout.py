import datetime as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='phrase_dd_menu',
                options=[]
            )],
            id='phrase-dropdown-div',
            style=dict(
                width='25vw',
                border='10px',
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
                width='25vw',
                border='10px',
                display = 'table-cell',
        )),
        html.Div([
            dcc.DatePickerRange(
                id='date-range-picker',
                end_date=dt.datetime.today(),
                start_date=dt.datetime.today() - dt.timedelta(days=60)
            )],
            id='date_picker_div',
            style=dict(
                width='25vw',
                border='10px',
                display = 'table-cell'
        )),
        html.Div([
            dcc.RadioItems(
                id='radio_graph_picker',
                options=[
                    {'label':'Bar Graph','value':'bar'},
                    {'label':'Line Graph','value':'line'}
                ],
                value='bar',
                labelStyle={'display': 'inline-block'}
            )],
            id='radio_item_div',
            style=dict(
                width='25vw',
                border='10px',
                display = 'table-cell'
        )),
    ],id='dd_div'),
    html.Div(
        id='search-time-graph-div',
        style=dict(
            height='450px',
            width='98vw'
        )
    ),
    html.Div(
        id='search-time-date-slider',
        style=dict(
            height='1,5vh',
            width='98vw'
        )
    ),
    html.Div(
        id='search-time-dt-div',
        style=dict(
            height='45vh',
            width='98vw'
        )
    ),
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
    width='99vw',
    height='99vh',
    padding='0,5vw',
    overflow='hidden',
    scroll='no'
))