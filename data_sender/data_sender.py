import time
import requests
import pandas as pd

FLASK_APP_URL = "http://flask_app:5000/predict" 

data_frame = pd.read_csv('df_testing_without_target.csv')

def send_data(row):
    """Send a single row of data to the Flask app and print the response."""
    data = {
        'temperature': row['temperature'],
        'humidity': row['humidity'],
        'sound_volume': row['sound_volume']
    }
    
    try:
        response = requests.post(FLASK_APP_URL, json=data)
        print(f"Sent data: {data}, Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    for index, row in data_frame.iterrows():
        send_data(row)
        time.sleep(10) 
