from dash import Dash, Input, Output, State, html, dcc, callback, no_update
import dash_bootstrap_components as dbc
import os
import time
from steamdb_parser import SteamdbParser
import dash_auth
import config

VALID_USERNAME_PASSWORD_PAIRS = {config.USERNAME: config.PASSWORD}

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])


auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)


options = ['https://steamdb.info/charts/', 'https://steamdb.info/topsellers/']

# Layout elements
dropdown= dcc.Dropdown(
    options = options, value = [],
    multi=False, id='dropdown', style={'background-color':'#151515', 'color':'#ffffff'}, clearable=False)

#dropdown = dcc.Dropdown(id='input_dropdown', clearable=False)
btn_download = dbc.Button('Download Data', id='download_btn', color='primary', outline=True, 
                          style = {'width':'180px'})
text_area = dcc.Textarea(
        id='text_area',
        value= '',
        style={'width': '90%', 'height': 210, 'background-color': '#151515', 'color': '#E0E0E0'},
        draggable = False,
        readOnly=True),

loading_element = dcc.Loading(id='loading_2', type='default', fullscreen=True
                              , children=[html.Div(id='loading_output_1')], 
                              style={'backgroundColor':'rgba(0, 0, 0, 0.5)'})

# Layout body
tab1_content = dbc.Container(
html.Div([
    #Title
    dbc.Row([html.H1('SteamDB Dumper')], style = {'margin-left':'7px', 'margin-top':'40px'}),

    #Dropdown with button
    dbc.Row([dbc.Col([html.H5('Data to Download'), dropdown], width=9),
        dbc.Col([btn_download])], style = {'margin-top':'14px'},
            align='center'),
    dbc.Row(html.Div(id='output_download', style = {'color':'#90EE90'})),
    dbc.Row(loading_element),

    #Text area
    dbc.Row(children=text_area, id='table', style = {'margin-top':'14px'}),
    dcc.Download(id='download_csv'),
    ]
),style={'height': '100vh', 'width': '70%', 'font-family':'Motiva Sans, Sans-serif'})

tabs = dbc.Tabs(
    [   dbc.Tab(tab1_content, label='SteamDB Dumper'),
        dbc.Tab(label='Post Dumper'),
        dbc.Tab(label='News Grabber')
    ])

# Layout
app.layout = html.Div([tabs])
server = app.server

# Functions
def prepare_csv(data):
    data_csv = '\n'.join([','.join(map(str, row)) for row in data])
    data_csv = data_csv.encode('utf-8')
    return data_csv

# Callbacks
@app.callback(
    [Output('text_area', 'value'), Output('download_csv', 'data'), Output('loading_2', 'children')],
    [Input('download_btn', 'n_clicks')],
    [State('dropdown', 'value')],
    prevent_initial_call=True
)
def parse_data(n_clicks, option):
    if n_clicks > 0:
        if option in ['https://steamdb.info/charts/', 'https://steamdb.info/topsellers/']:
            steamdb_parser = SteamdbParser()
            if option == 'https://steamdb.info/charts/':
                status_code = steamdb_parser.get_charts_data()
                if status_code == 200:
                    total_apps = len(steamdb_parser.data_charts) - 1
                    res_message = f'Charts data downloaded, total apps: {total_apps}.'
                    steamdb_parser.save_to_csv(steamdb_parser.file_charts)
                    data_csv = prepare_csv(steamdb_parser.data_charts)
                    data_send = dcc.send_bytes(data_csv, 'charts.csv')
                else:
                    res_message = f'Status code: {status_code}. Try again later'
                    data_send = None

            if option == 'https://steamdb.info/topsellers/':
                status_code = steamdb_parser.get_sellers_data()
                if status_code == 200:
                    total_apps = len(steamdb_parser.data_sellers) - 1
                    res_message = f'Sellers data downloaded, total apps: {total_apps}.'
                    steamdb_parser.save_to_csv(steamdb_parser.file_sellers)
                    data_csv = prepare_csv(steamdb_parser.data_sellers)
                    data_send = dcc.send_bytes(data_csv, 'topsellers.csv')
                else:
                    res_message = f'Status code: {status_code}. Try again later'
                    data_send = None
            return res_message, data_send, ''
    return 

if __name__=='__main__':
    app.run_server(debug=True)