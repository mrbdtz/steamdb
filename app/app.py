from dash import Dash, Input, Output, State, html, dcc, callback
import dash_bootstrap_components as dbc
import os

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

options = ['https://steamdb.info/charts/', 'https://steamdb.info/topsellers/']

# Layout elements
dropdown= dcc.Dropdown(
    options = options, value = [],
    multi=False, id='dropdown', style={"background-color":"#151515", 'color':'#ffffff'}, clearable=False)

#dropdown = dcc.Dropdown(id='input_dropdown', clearable=False)
btn_download = dbc.Button('Download Data', color='primary', outline=True, 
                          style = {'width':'180px'})
text_area = dcc.Textarea(
        id='text_area',
        value= 'Text area data',
        style={'width': '90%', 'height': 210},
        draggable = False,
        readOnly=True),

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

    #Text area
    dbc.Row(children=text_area, id='table', style = {'margin-top':'14px'}),
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

if __name__=='__main__':
    app.run_server(debug=True)