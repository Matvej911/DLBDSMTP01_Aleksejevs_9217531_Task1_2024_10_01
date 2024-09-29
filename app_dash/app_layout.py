import dash
from dash import dcc, html
import dash_ag_grid as dag
from data_processing import fetch_data  

df = fetch_data()


columnDefs = [
    {
        "headerName": "Environment",
        "children": [
            {"field": "temperature", "headerName": "Temperature (°C)"},
            {"field": "humidity", "headerName": "Humidity (%)"},
            {"field": "sound_volume", "headerName": "Sound Volume (dB)"}
        ],
    },
    {
        "headerName": "Prediction",
        "children": [
            {"field": "prediction", "headerName": "Anomaly Prediction"}
        ],
    },
    {
        "headerName": "Timestamp",
        "field": "timestamp",
    }
]

defaultColDef = {
    "filter": True,
    "sortable": True,
    "resizable": True,
    "enableRowGroup": True,
    "enablePivot": True,
    "enableValue": True,
}

sideBar = {
    "toolPanels": [
        {
            "id": "columns",
            "labelDefault": "Columns",
            "labelKey": "columns",
            "iconKey": "columns",
            "toolPanel": "agColumnsToolPanel",
        },
        {
            "id": "filters",
            "labelDefault": "Filters",
            "labelKey": "filters",
            "iconKey": "filter",
            "toolPanel": "agFiltersToolPanel",
        }
    ],
    "position": "left",
    "defaultToolPanel": "filters",
}


def create_layout(app):

    app.layout = html.Div([
        html.H1(children='Data Analysis and Anomaly Predictions', style={'textAlign': 'center'}),
        
        dcc.Store(id='alert-store', data={'visible': False, 'message': ''}),
        dcc.Store(id='mode-store', data='real-time'),
        

        html.Div([
        
            html.Div([
                dcc.Input(id='start-date', type='text', placeholder='start date (YYYY-MM-DD)', style={'margin': '10px','padding': '10px','border': '1px solid #ccc', 'borderRadius': '5px', 'fontSize': '16px', 'width': '200px',}),
                dcc.Input(id='start-time', type='text', placeholder='start time (HH:MM)', style={'margin': '10px','padding': '10px','border': '1px solid #ccc', 'borderRadius': '5px', 'fontSize': '16px', 'width': '200px',}),
                dcc.Input(id='end-date', type='text', placeholder='end date (YYYY-MM-DD)', style={'margin': '10px','padding': '10px','border': '1px solid #ccc', 'borderRadius': '5px', 'fontSize': '16px', 'width': '200px',}),
                dcc.Input(id='end-time', type='text', placeholder='end time (HH:MM)', style={'margin': '10px','padding': '10px','border': '1px solid #ccc', 'borderRadius': '5px', 'fontSize': '16px', 'width': '200px',}),
                html.Button('Filter', id='filter-button', n_clicks=0, style={'margin': '10px','padding': '10px','border': '1px solid #ccc', 'borderRadius': '5px', 'fontSize': '16px', 'width': '200px',}),
                html.Div(id='error-message', style={'color': 'red', 'fontWeight': 'bold', 'marginTop': '10px'}),
            ], style={'display': 'le', 'flexDirection': 'column', 'alignItems': 'center', 'marginBottom': '20px'}),
            
      
            html.Div([ 
                html.Div([
                    html.H3('Average Temperature'),
                    html.P(id='avg-temp', style={'fontSize': '24px', 'fontWeight': 'bold'}),
                ], style={'border': '1px solid #007bff', 'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
                
                html.Div([
                    html.H3('Average Humidity'),
                    html.P(id='avg-humidity', style={'fontSize': '24px', 'fontWeight': 'bold'}),
                ], style={'border': '1px solid #28a745', 'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
                
                html.Div([
                    html.H3('Average Noise Level'),
                    html.P(id='avg-sound', style={'fontSize': '24px', 'fontWeight': 'bold'}),
                ], style={'border': '1px solid #dc3545', 'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
                
                html.Div(
                    id='alert-box',
                    style={
                        'height': '120px',
                        'width': '300px',
                        'border': '1px solid #000000',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'margin': '10px',
                        'textAlign': 'center',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'backgroundColor': 'white',
                        'fontSize': '24px',
                        'fontWeight': 'bold'
                    }
                ),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}),
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
        

        html.Div([
            html.Div([
                html.H3('Maximum and Minimum Values'),
                html.P(id='max-min-values', style={'fontSize': '24px', 'lineHeight': '1.6', 'fontWeight': 'bold', 'whiteSpace': 'pre-line'}),
            ], style={'border': '1px solid #007bff', 
                    'borderRadius': '10px', 
                    'padding': '20px',
                    'width': '48%', 
                    'margin': '10px', 
                    'textAlign': 'center', 
                    'maxWidth': '400px'}),
            
            html.Div([
                dcc.Graph(id='prediction-distribution')
            ], style={'padding': '20px', 'width': '48%', 'margin': '10px', 'maxWidth': '400px', 'backgroundColor': '#f9f9f9'}),
        ], style={'display': 'flex', 'gap': '20px', 'margin': '20px auto', 'flexDirection': 'row', 'justifyContent': 'space-between', 'flexWrap': 'wrap', 'width': '80%'}),
        

        html.Div([
            dag.AgGrid(
                id="anomaly-data-grid",
                columnDefs=columnDefs,
                rowData=df.to_dict("records"),
                dashGridOptions={"rowSelection": "multiple", "animateRows": True, "sideBar": sideBar},
                defaultColDef=defaultColDef,
                enableEnterpriseModules=False, 
                style={'height': '400px', 'width': '100%', 'overflowX': 'auto'}
            )
        ], style={'textAlign': 'center', 'maxWidth': '1200px', 'margin': '0 auto'}),
        
        dcc.Interval(
            id='prediction-interval',
            interval=5 * 1000, 
            n_intervals=0
        ),
        
        dcc.Interval(
            id='alert-interval',
            interval=5 * 1000, 
            n_intervals=0
        ),
        

        dcc.Graph(id='temperature-graph'),
        dcc.Graph(id='humidity-graph'),
        dcc.Graph(id='sound-volume-graph'),
    ])
