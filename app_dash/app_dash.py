import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_ag_grid as dag
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
import re
import datetime as dt
from db_config import engine
from data_processing import validate_time_format, fetch_data
from app_layout import create_layout


app  = dash.Dash(__name__)

create_layout(app)


@app.callback(
    [
        Output('anomaly-data-grid', 'rowData'),
        Output('temperature-graph', 'figure'),
        Output('humidity-graph', 'figure'),
        Output('sound-volume-graph', 'figure'),
        Output('avg-temp', 'children'),
        Output('avg-humidity', 'children'),
        Output('avg-sound', 'children'),
    ],
    [Input('filter-button', 'n_clicks'),
     Input('prediction-interval', 'n_intervals')],  
    [Input('start-date', 'value'), Input('end-date', 'value'), Input('start-time', 'value'), Input('end-time', 'value')]
)
def update_data(n_clicks, n_intervals, start_date, end_date, start_time, end_time):
    df = fetch_data(start_date, end_date, start_time, end_time)

    if df.empty:
        empty_fig = go.Figure() 
        empty_fig.update_layout(title='No Data Available')
        return [], empty_fig, empty_fig, empty_fig, "N/A", "N/A", "N/A"

    avg_temp = df['temperature'].mean()
    avg_humidity = df['humidity'].mean()
    avg_sound = df['sound_volume'].mean()

    temp_fig = px.line(df, x='timestamp', y='temperature', title='Temperature over time')
    hum_fig = px.line(df, x='timestamp', y='humidity', title='Humidity over time')
    sound_fig = px.line(df, x='timestamp', y='sound_volume', title='Sound level over time')


    return df.to_dict("records"), temp_fig, hum_fig, sound_fig, f"{avg_temp:.2f} °C", f"{avg_humidity:.2f} %", f"{avg_sound:.2f} dB"



@app.callback(
    Output('alert-store', 'data'),
    [Input('alert-interval', 'n_intervals')]
)
def check_alert(n_intervals):
    df = fetch_data()
    
    if df.empty:
        return {'visible': False, 'message': ''}

    last_prediction = df['prediction'].iloc[-1]


    if last_prediction == 1:
        return {'visible': True, 'message': "Alert: Anomaly detected"}
    else:
        return {'visible': False, 'message': ''}


@app.callback(
    Output('alert-box', 'children'),
    Output('alert-box', 'style'),
    [Input('alert-store', 'data'), Input('mode-store', 'data')]  
)
def update_alert(alert_data, mode):
 
    if mode == 'historical':
        return "Historical data: detector stopped", {
            'height': '120px',
            'width': '300px',
            'border': '1px solid gray',
            'borderRadius': '10px',
            'padding': '10px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'backgroundColor': 'gray',
            'color': 'white',
            'fontSize': '24px',
            'fontWeight': 'bold',
        }

    if alert_data['visible']:
        return alert_data['message'], {
            'height': '120px',
            'width': '300px',
            'border': '1px solid red',
            'borderRadius': '10px',
            'padding': '10px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'backgroundColor': 'red',
            'color': 'white',
            'fontSize': '24px',
            'fontWeight': 'bold'
        }
    else:
        return "No anomaly detected", {
            'height': '120px',
            'width': '300px',
            'border': '1px solid green',
            'borderRadius': '10px',
            'padding': '10px',
            'margin': '10px',
            'textAlign': 'center',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'backgroundColor': 'white',
            'color': 'green',
            'fontSize': '24px',
            'fontWeight': 'bold',
        }

@app.callback(
    Output('max-min-values', 'children'),
    [Input('alert-interval', 'n_intervals')],
    [Input('start-date', 'value'), Input('end-date', 'value'), Input('start-time', 'value'), Input('end-time', 'value')]
)
def update_min_max(n_intervals, start_date, end_date, start_time, end_time):
    df = fetch_data(start_date, end_date, start_time, end_time)
    
    if df.empty:
        return "N/A"

    max_temp = df['temperature'].max()
    min_temp = df['temperature'].min()
    max_humidity = df['humidity'].max()
    min_humidity = df['humidity'].min()
    max_sound = df['sound_volume'].max()
    min_sound = df['sound_volume'].min()

    return (
        "Temperature:          Max = {:.2f} °C      Min = {:.2f} °C\n"
        "Humidity:           Max = {:.2f} %      Min = {:.2f} %\n"
        "Noise level:       Max = {:.2f} dB     Min = {:.2f} dB".format(
            max_temp, min_temp, max_humidity, min_humidity, max_sound, min_sound
        )
    )

@app.callback(
    Output('prediction-distribution', 'figure'),
    [Input('alert-interval', 'n_intervals'),
     Input('start-date', 'value'),  
     Input('end-date', 'value'),
     Input('start-time', 'value'),
     Input('end-time', 'value')]
)
def update_distribution_chart(n_intervals, start_date, end_date, start_time, end_time):
    df = fetch_data(start_date, end_date, start_time, end_time)

    if df.empty:
        return go.Figure()  

    counts = df['prediction'].value_counts().sort_index()  


    fig = go.Figure([go.Bar(x=['Non-Anomalies (0)', 'Anomalies (1)'], y=[counts.get(0, 0), counts.get(1, 0)])])


    fig.update_layout(
        title="Distribution of Predictions (1 and 0)",
        xaxis_title="Type of Prediction",
        yaxis_title="Count",
        plot_bgcolor='rgba(0,0,0,0)',  
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig


@app.callback(
    Output('error-message', 'children'),
    [Input('filter-button', 'n_clicks')],
    [Input('start-date', 'value'),
     Input('start-time', 'value'),
     Input('end-date', 'value'),
     Input('end-time', 'value')]
)

def validate_time_format(n_clicks, start_date, start_time, end_date, end_time):
    error_message = ""
    

    if start_date and start_date != '':
        try:
            pd.to_datetime(start_date, format='%Y-%m-%d')
        except ValueError:
            error_message += f"Invalid start date format: {start_date}. Expected format: YYYY-MM-DD. "
    

    if end_date and end_date != '':
        try:
            pd.to_datetime(end_date, format='%Y-%m-%d')
        except ValueError:
            error_message += f"Invalid end date format: {end_date}. Expected format: YYYY-MM-DD. "
    

    if start_time and start_time != '':
        try:
            pd.to_datetime(start_time, format='%H:%M')
        except ValueError:
            error_message += f"Invalid start time format: {start_time}. Expected format: HH:MM. "
    

    if end_time and end_time != '':
        try:
            pd.to_datetime(end_time, format='%H:%M')
        except ValueError:
            error_message += f"Invalid end time format: {end_time}. Expected format: HH:MM. "

    
    return error_message if error_message else ""


@app.callback(
    Output('mode-store', 'data'),
    [Input('start-date', 'value'), Input('end-date', 'value'),
     Input('start-time', 'value'), Input('end-time', 'value')]
)



def update_mode(start_date, end_date, start_time, end_time):

    current_date = dt.date.today()
    current_time = dt.datetime.now().time()
    

    if end_date:
        end_date_parsed = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce').date()
        if end_date_parsed < current_date: 
            return 'historical'

    if end_time:
        end_time_parsed = pd.to_datetime(end_time, format='%H:%M', errors='coerce').time()
        if end_time_parsed < current_time:  
            return 'historical'

    if start_date or start_time:
        return 'historical'

    return 'real-time'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True) 