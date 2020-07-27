import callbacks
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from layout import layout


app.layout = layout

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8100',debug=True)
