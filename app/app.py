from flask import Flask, request, jsonify
import mysql.connector
import pickle
import joblib  
import os

app = Flask(__name__)

db_config = {
    'user': os.getenv('MYSQL_DB_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'host': 'db',
    'database': 'anomaly_detection'
}

def load_model_and_scaler():
    try:

        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except Exception as e:
        print(f"Error loading the model or scaler: {e}")
        return None, None

model, scaler = load_model_and_scaler()


def save_to_db(data, prediction):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
            INSERT INTO sensor_data (temperature, humidity, sound_volume, prediction)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (data['temperature'], data['humidity'], data['sound_volume'], prediction))
        conn.commit()

    except mysql.connector.Error as e:
        print(f"Error writing to the database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print(request.data)  
    data = request.json
    print(data)  

    if not all(k in data for k in ['temperature', 'humidity', 'sound_volume']):
        return jsonify({'error': 'Incorrect data'}), 400


    try:
     
        input_data = [[data['temperature'], data['humidity'], data['sound_volume']]]
        
       
        scaled_data = scaler.transform(input_data)
        
  
        prediction = int(model.predict(scaled_data)[0])
    except Exception as e:
        return jsonify({'error': f'Prediction error: {e}'}), 500

 
    save_to_db(data, prediction)

    return jsonify({'prediction': prediction}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  

