from sqlalchemy import create_engine
import os

def get_db_config():
    return {
        'user': os.getenv('MYSQL_DB_USER'),
        'password': os.getenv('MYSQL_ROOT_PASSWORD'),
        'host': 'db',
        'database': 'anomaly_detection'
    }

db_config = get_db_config()
db_url = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
engine = create_engine(db_url)



