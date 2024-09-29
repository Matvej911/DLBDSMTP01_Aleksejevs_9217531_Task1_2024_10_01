import dash
from dash import dcc, html
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_ag_grid as dag
import plotly.express as px
import plotly.graph_objects as go
# Data handling and database
import pandas as pd
from sqlalchemy import create_engine
import re
import datetime as dt
import mysql
import mysql.connector


# Настройки подключения к базе данных
def get_db_config():
    return {
        'user': 'root',
        'password': 'OKM$%^nbvCDE',
        'host': 'db',
        'database': 'anomaly_detection'
    }

def create_connection():
    """Create a database connection."""
    config = get_db_config()
    try:
        connection = mysql.connector.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            database=config['database']
        )
        print("Connection successful")
        return connection
    except mysql.connector.Error as e:
        print(f"Connection error: {e}")
        return None

def validate_time_format(time_str):
    """Validate the time format as HH:MM."""
    # Time format regex
    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    return time_pattern.match(time_str) is not None

def fetch_data(start_date=None, end_date=None, start_time=None, end_time=None):
    query = "SELECT temperature, humidity, sound_volume, prediction, timestamp FROM sensor_data"
    
    # Create a connection to the database
    connection = create_connection()
    
    try:
        # Use pandas to read the query results into a DataFrame
        df = pd.read_sql(query, connection)
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure timestamp is in datetime format
        
        # Convert start_date and end_date to datetime, coerce errors to NaT
        if start_date:
            start_date_dt = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
            if pd.notna(start_date_dt):
                df = df[df['timestamp'].dt.date >= start_date_dt.date()]
        
        if end_date:
            end_date_dt = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')
            if pd.notna(end_date_dt):
                df = df[df['timestamp'].dt.date <= end_date_dt.date()]
        
        # Similar approach for times
        if start_time:
            try:
                start_time_dt = pd.to_datetime(start_time, format='%H:%M').time()
                df = df[df['timestamp'].dt.time >= start_time_dt]
            except ValueError:
                pass  # Ignore invalid time formats

        if end_time:
            try:
                end_time_dt = pd.to_datetime(end_time, format='%H:%M').time()
                df = df[df['timestamp'].dt.time <= end_time_dt]
            except ValueError:
                pass  # Ignore invalid time formats

        return df

    finally:
        connection.close()  # Ensure the connection is closed after the operation

# Initialize Dash app

# Получаем данные для отображения
df = fetch_data()

# Настройка столбцов
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

# Настройка по умолчанию для столбцов
defaultColDef = {
    "filter": True,
    "sortable": True,
    "resizable": True,
    "enableRowGroup": True,
    "enablePivot": True,
    "enableValue": True,
}

# Настройка боковой панели
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

# Создаем приложение Dash
app = dash.Dash(__name__)

# Макет приложения
app.layout = html.Div([
    html.H1(children='Анализ данных и предсказаний аномалий', style={'textAlign': 'center'}),
    
    dcc.Store(id='alert-store', data={'visible': False, 'message': ''}),
    dcc.Store(id='mode-store', data='real-time'),
    
    # Statistics in boxes
    html.Div([
        # Input fields and error message
        html.Div([
            dcc.Input(id='start-date', type='text', placeholder='start date (YYYY-MM-DD)', style={'margin': '10px'}),
            dcc.Input(id='start-time', type='text', placeholder='start time (HH:MM)', style={'margin': '10px'}),
            dcc.Input(id='end-date', type='text', placeholder='end date (YYYY-MM-DD)', style={'margin': '10px'}),
            dcc.Input(id='end-time', type='text', placeholder='end time (HH:MM)', style={'margin': '10px'}),
            html.Button('Применить фильтр', id='filter-button', n_clicks=0, style={'margin': '10px'}),
            html.Div(id='error-message', style={'color': 'red', 'fontWeight': 'bold', 'marginTop': '10px'}),
        ], style={'display': 'le', 'flexDirection': 'column', 'alignItems': 'center', 'marginBottom': '20px'}),
        
        # Average boxes
        html.Div([ 
            html.Div([
                html.H3('Средняя температура'),
                html.P(id='avg-temp', style={'fontSize': '24px', 'fontWeight': 'bold'}),
            ], style={'border': '1px solid #007bff', 'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
            
            html.Div([
                html.H3('Средняя влажность'),
                html.P(id='avg-humidity', style={'fontSize': '24px', 'fontWeight': 'bold'}),
            ], style={'border': '1px solid #28a745', 'borderRadius': '10px', 'padding': '10px', 'margin': '10px'}),
            
            html.Div([
                html.H3('Средний уровень шума'),
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
    
    # Max/Min values and distribution
    html.Div([
        html.Div([
            html.H3('Максимальные и минимальные значения'),
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
    
    # AG Grid table
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
    
    # Intervals
    dcc.Interval(
        id='prediction-interval',
        interval=5 * 1000,  # 5 seconds in milliseconds
        n_intervals=0
    ),
    
    dcc.Interval(
        id='alert-interval',
        interval=5 * 1000,  # 5 seconds in milliseconds
        n_intervals=0
    ),
    
    # Graphs
    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Graph(id='sound-volume-graph'),
])


# Callback для обновления графиков и таблицы
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
     Input('prediction-interval', 'n_intervals')],  # Add the interval as an input
    [Input('start-date', 'value'), Input('end-date', 'value'), Input('start-time', 'value'), Input('end-time', 'value')]
)
def update_data(n_clicks, n_intervals, start_date, end_date, start_time, end_time):
    # Fetch data with the provided filters
    df = fetch_data(start_date, end_date, start_time, end_time)

    if df.empty:
        empty_fig = go.Figure()  # Create an empty figure
        empty_fig.update_layout(title='No Data Available')
        return [], empty_fig, empty_fig, empty_fig, "N/A", "N/A", "N/A"

    avg_temp = df['temperature'].mean()
    avg_humidity = df['humidity'].mean()
    avg_sound = df['sound_volume'].mean()

    # Create figures using the filtered data
    temp_fig = px.line(df, x='timestamp', y='temperature', title='Температура во времени')
    hum_fig = px.line(df, x='timestamp', y='humidity', title='Влажность во времени')
    sound_fig = px.line(df, x='timestamp', y='sound_volume', title='Уровень шума во времени')

    return df.to_dict("records"), temp_fig, hum_fig, sound_fig, f"{avg_temp:.2f} °C", f"{avg_humidity:.2f} %", f"{avg_sound:.2f} dB"



# Callback для обновления сообщения об аномалиях
@app.callback(
    Output('alert-store', 'data'),
    [Input('alert-interval', 'n_intervals')]
)
def check_alert(n_intervals):
    df = fetch_data()
    
    if df.empty:
        return {'visible': False, 'message': ''}

    # Check only the last prediction
    last_prediction = df['prediction'].iloc[-1]


    if last_prediction == 1:
        return {'visible': True, 'message': "Alert:Anomaly detected"}
    else:
        return {'visible': False, 'message': ''}

# Callback для отображения сообщения об аномалиях
@app.callback(
    Output('alert-box', 'children'),
    Output('alert-box', 'style'),
    [Input('alert-store', 'data'), Input('mode-store', 'data')]  # Add mode-store as an input
)
def update_alert(alert_data, mode):
    # Only show real-time alerts if in real-time mode
    if mode == 'historical':
        return "Исторические данные - нет аномалий", {
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

    # Real-time mode alert behavior
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
        return "Аномалия не обнаружена", {
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
        "Температура:          Макс = {:.2f} °C      Мин = {:.2f} °C\n"
        "Влажность:          Макс = {:.2f} %      Мин = {:.2f} %\n"
        "Уровень шума:      Макс = {:.2f} dB     Мин = {:.2f} dB".format(
            max_temp, min_temp, max_humidity, min_humidity, max_sound, min_sound
        )
    )

@app.callback(
    Output('prediction-distribution', 'figure'),
    [Input('alert-interval', 'n_intervals'),
     Input('start-date', 'value'),  # Move these inputs to trigger the callback
     Input('end-date', 'value'),
     Input('start-time', 'value'),
     Input('end-time', 'value')]
)
def update_distribution_chart(n_intervals, start_date, end_date, start_time, end_time):
    # Fetch filtered data based on the provided start/end dates and times
    df = fetch_data(start_date, end_date, start_time, end_time)

    if df.empty:
        return go.Figure()  # Return an empty figure if there's no data

    # Count how many 1s and 0s in the 'prediction' column
    counts = df['prediction'].value_counts().sort_index()  # Ensures 0 and 1 are sorted

    # Bar chart with Plotly
    fig = go.Figure([go.Bar(x=['Non-Anomalies (0)', 'Anomalies (1)'], y=[counts.get(0, 0), counts.get(1, 0)])])

    # Add titles and labels
    fig.update_layout(
        title="Распределение предсказаний (1 и 0)",
        xaxis_title="Тип предсказания",
        yaxis_title="Количество",
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
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
    
    # Validate start_date
    if start_date and start_date != '':
        try:
            pd.to_datetime(start_date, format='%Y-%m-%d')
        except ValueError:
            error_message += f"Неправильный формат даты начала: {start_date}. Ожидаемый формат: YYYY-MM-DD. "
    
    # Validate end_date
    if end_date and end_date != '':
        try:
            pd.to_datetime(end_date, format='%Y-%m-%d')
        except ValueError:
            error_message += f"Неправильный формат даты окончания: {end_date}. Ожидаемый формат: YYYY-MM-DD. "
    
    # Validate start_time
    if start_time and start_time != '':
        try:
            pd.to_datetime(start_time, format='%H:%M')
        except ValueError:
            error_message += f"Неправильный формат времени начала: {start_time}. Ожидаемый формат: HH:MM. "
    
    # Validate end_time
    if end_time and end_time != '':
        try:
            pd.to_datetime(end_time, format='%H:%M')
        except ValueError:
            error_message += f"Неправильный формат времени окончания: {end_time}. Ожидаемый формат: HH:MM. "
    
    # Return the error message if there's any
    return error_message if error_message else ""


@app.callback(
    Output('mode-store', 'data'),
    [Input('start-date', 'value'), Input('end-date', 'value'),
     Input('start-time', 'value'), Input('end-time', 'value')]
)



def update_mode(start_date, end_date, start_time, end_time):
    # Current date and time
    current_date = dt.date.today()
    current_time = dt.datetime.now().time()
    
    # Check if end_date and end_time are "current" (i.e., within the range of today/now)
    if end_date:
        end_date_parsed = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce').date()
        if end_date_parsed < current_date:  # If end_date is not today, it's historical
            return 'historical'

    if end_time:
        end_time_parsed = pd.to_datetime(end_time, format='%H:%M', errors='coerce').time()
        if end_time_parsed < current_time:  # If end_time is before current time, it's historical
            return 'historical'

    # If there is a start date/time but end date/time is current, treat it as historical
    if start_date or start_time:
        return 'historical'

    # Default to real-time if no filters are applied or if end_date and end_time are "now"
    return 'real-time'




if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
