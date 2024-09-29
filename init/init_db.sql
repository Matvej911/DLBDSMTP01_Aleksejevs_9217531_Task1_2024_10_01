CREATE DATABASE IF NOT EXISTS anomaly_detection;

USE anomaly_detection;

CREATE TABLE IF NOT EXISTS sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    sound_volume FLOAT,
    prediction INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
