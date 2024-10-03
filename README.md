# Anomaly Detection with Flask, MySQL, and Dash

[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/flask-python%203.9-orange.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7-blue.svg)](https://www.mysql.com/)
[![Dash](https://img.shields.io/badge/Dash-plotly-blueviolet.svg)](https://plotly.com/dash/)

## 📑 Project Overview

This project implements a real-time **Anomaly Detection System** using a machine learning model deployed through Flask, with MySQL as the database and Dash for visualization. The project uses Docker for seamless deployment across environments.

### Key Features:

- **Real-time anomaly detection** using a trained machine learning model.
- **Data visualization** through Plotly Dash for monitoring anomalies.
- **MySQL** integration for data storage.
- Fully **containerized** using Docker for easy deployment.

---

## 🚀 Tech Stack

- **Backend**: Flask, Python 3.9
- **Database**: MySQL 5.7
- **Machine Learning**: K-Nearest Neighbors, RandomForest, GradientBoosting, Logistic Regression, Support Vector Machine
- **Visualization**: Dash (Plotly)
- **Containerization**: Docker

---

## 📂 Project Structure

```bash
Model_2_product/
│
├── app/                      # Flask app for ML prediction and DB interaction
│   ├── app.py                # Main Flask app for handling predictions and database communication
│   ├── best_model.pkl        # Trained machine learning model for anomaly detection
│   ├── scaler.pkl            # Scaler for feature normalization used during model training
│   ├── requirements.txt      # Python dependencies for the Flask app
│   └── Dockerfile            # Dockerfile for the Flask app
│
├── app_dash/                 # Dash app for data visualization
│   ├── app_dash.py           # Dash app layout and callback logic
│   ├── app_layout.py         # Layout settings for the Dash application
│   ├── data_processing.py    # Data transformation and processing logic
│   ├── db_config.py          # Configuration to connect Dash app to the database
│   ├── requirements4.txt     # Python dependencies for the Dash app
│   └── Dockerfile            # Dockerfile for the Dash app
│
├── dashapp/                  # Alternative Dash app for extended functionality
│   ├── dashapp.py            # Another Dash app variation
│   ├── Dockerfile            # Dockerfile for the alternative Dash app
│   └── requirements5.txt     # Python dependencies for the alternative Dash app
│
├── data_sender/              # Component for sending test data to the Flask app
│   ├── data_sender.py        # Script that sends data to the Flask app via API requests
│   ├── df_testing_without_target.csv  # Test dataset for sending to the API
│   ├── requirements2.txt     # Python dependencies for the data sender component
│   └── Dockerfile            # Dockerfile for the data sender
│
├── database/                 # Database initialization and configuration
│   ├── create_db.py          # Script for creating and initializing MySQL database tables
│   ├── init/                 # Initialization folder for SQL scripts
│   │   └── init_db.sql       # SQL script for initializing the database schema
│   ├── requirements.txt      # Python dependencies for database management
│   └── Dockerfile            # Dockerfile for the database setup
│
├── model_not_need/           # Machine learning model and data files
│   ├── dataset.csv           # Dataset used for model training and testing
│   └── model.py              # Model building script, not need to execute, best model and scaler is saved in app/ 
│
├── venv/                     # Python virtual environment (not included in the repository)
│
├── .env                      # Environment variables for sensitive data (passwords, API keys)
├── .gitignore                # Git ignore file to exclude unnecessary files from being committed
├── docker-compose.yml        # Docker Compose file to orchestrate the multi-container services
└── README.md                 # Documentation for setting up and running the project

```

---

## 🚀 Setup Instructions

Follow these steps to get your project up and running.

### Prerequisites

Ensure you have the following tools installed:

```bash
# Install Docker
 For installation instructions, visit: https://docs.docker.com/get-docker/

# Install Docker Compose
 For installation instructions, visit: https://docs.docker.com/compose/install/

```

### 1. Clone the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/Matvej911/DLBDSMTP01_Aleksejevs_9217531_Task1_2024_10_01.git
cd DLBDSMTP01_Aleksejevs_9217531_Task1_2024_10_01
```

### 2. Setup Environment Variables

Create a .env file in the root of the project to store your sensitive information:

Open the .env file for editing using nano:

```bash
nano .env
```

Add the following content to the .env file:

```bash
MYSQL_ROOT_PASSWORD=pasword
MYSQL_DB_USER=root
```

Save the file:

- Press CTRL + O to write the changes.
- Press Enter to confirm the file name.
- Press CTRL + X to exit the editor.

📝 Note: Ensure the .env file is included in your .gitignore to prevent committing sensitive information

### 3. Build and Run Docker Containers

Build the Docker images and start the containers:

```bash
docker-compose up --build
```

### 4. Access the Applications

Once the containers are running, you can access the applications at the following URLs:

```bash
Dash Visualization App: http://localhost:8050
```

---

### 🔄 Data Flow Steps

![anomaly_detection_system_architecture (3)](https://github.com/user-attachments/assets/c1f3ce68-7697-4fc3-9408-0a2c5d146309)

1. **Data Stream**:

   - In this project is used Synthetic data and data stream is made using python functions.
   - Can make that data is collected from sensors (e.g., temperature, humidity, sound volume).
   - The data stream feeds directly into the machine learning model for analysis.

2. **ML Model Prediction**:

   - A Python script processes the incoming data using a pre-trained machine learning model.
   - The model makes predictions regarding anomalies in the data.

3. **Database**:

   - The predictions, with data, are stored in a MySQL database.
   - This allows for efficient retrieval and management of data for future analysis and visualization.

4. **Visualization**:
   - A Dash application retrieves data from the database to present it visually.
   - The application provides graphical representations (such as charts and graphs) to help users understand the data trends and anomalies.

### 🚀 Potential for Real Data Flow

While the current implementation uses simulated data for testing, this structure allows for easy integration with real-time data streams.

🕒 Date and Time Filtering
Easily filter the data to view specific time periods.
Start Date/Time: Specify when to start the data view.
End Date/Time: Select the end of the period for detailed analysis.
This feature allows for detailed analysis of specific intervals of interest.

## 📊 Dashboard Functionality

The dashboard is designed to monitor real-time data and the predictive performance of the machine learning model. It offers several key features to ensure the system's reliability and ease of use:

### 🧮 Interactive Data Table

- Displays essential data including:
  - **Temperature** 🌡️
  - **Humidity** 💧
  - **Sound Volume** 🔊
  - **Anomaly Prediction** ⚠️
  - **Timestamp** 🕒
- **Sorting Options**: Easily sort the data, for example, from highest to lowest or from oldest to newest.

### 📈 Real-Time Metrics and Statistics

- **Maximum and Minimum Values**:
  - **Temperature:** Max = 27.60°C | Min = 20.00°C 🌡️
  - **Humidity:** Max = 59.20% | Min = 40.80% 💧
  - **Noise Level:** Max = 98.80 dB | Min = 36.80 dB 🔊
- **Averages**:
  - **Average Temperature**: 24.08 °C 🌡️
  - **Average Humidity**: 50.84% 💧
  - **Average Noise Level**: 61.50 dB 🔊

### 🚨 Anomaly Alerts

Visual alerts are displayed to notify the user of the current system state:

- **No Anomaly Detected**: Standard status.
- **Alert: Anomaly Detected**: The box turns red when an anomaly is detected, allowing for quick recognition.

### 📊 Data Distribution Graph

- **Visual representation of anomaly predictions:**
  0 (Normal) vs. 1 (Anomaly).
  Easily monitor how often anomalies occur across the dataset.

### 📅 Time Series Graphs

- **Temperature Over Time**🌡️: Line graph showing temperature variations over time.
- **Humidity Over Time**💧: Line graph tracking changes in humidity over time.
- **Noise Level Over Time**🔊: Graph displaying sound volume trends over time.

### ⏳ Custom Date and Time Filtering

- Enter **Start Date/Time** and **End Date/Time** to filter and view data within a specific time period.

---

## 📈 Scaling the Data Sender with Docker Compose

In order to handle a higher volume of data, you can easily scale the `data_sender` service in Docker Compose. This will allow you to run multiple instances of the `data_sender`, simulating parallel data streams, which can be useful for performance testing or handling real-time data at a larger scale.

### 🔧 How to Scale the data_sender

To scale the data_sender service, you can run the following command:

```
docker-compose up --scale data_sender=2 -d
```

## 💡 Benefits of Scaling

- **Increased Throughput:** Running multiple instances of the data_sender can help process more data simultaneously, improving overall throughput.
- **Load Balancing:** Distributing the data load across multiple instances can lead to better performance and responsiveness.
- **Redundancy:** Having multiple instances increases the reliability of your data acquisition process, as one instance can take over if another fails.

## 🧑‍🤝‍🧑 Contributing

Contributions are welcome! Please create an issue first to discuss what you would like to change.

## 📞 Contact

For any issues, feel free to open an issue on the GitHub repository or contact me via
matvejaleksejv@gmail.com
