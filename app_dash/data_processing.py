import pandas as pd
import re
from db_config import engine  

def validate_time_format(time_str):
    """Validate the time format as HH:MM."""

    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    return time_pattern.match(time_str) is not None

def fetch_data(start_date=None, end_date=None, start_time=None, end_time=None):
    query = "SELECT temperature, humidity, sound_volume, prediction, timestamp FROM sensor_data"
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  
    
   
    if start_date:
        start_date_dt = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
        if pd.notna(start_date_dt):
            df = df[df['timestamp'].dt.date >= start_date_dt.date()]
    
    if end_date:
        end_date_dt = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')
        if pd.notna(end_date_dt):
            df = df[df['timestamp'].dt.date <= end_date_dt.date()]
    

    if start_time:
        try:
            start_time_dt = pd.to_datetime(start_time, format='%H:%M').time()
            df = df[df['timestamp'].dt.time >= start_time_dt]
        except ValueError:
            pass  

    if end_time:
        try:
            end_time_dt = pd.to_datetime(end_time, format='%H:%M').time()
            df = df[df['timestamp'].dt.time <= end_time_dt]
        except ValueError:
            pass 

    return df
