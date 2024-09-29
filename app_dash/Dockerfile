FROM python:3.9-slim

WORKDIR /app_dash

COPY requirements4.txt .

RUN pip install --no-cache-dir -r requirements4.txt


COPY app_dash.py ./
COPY app_layout.py ./
COPY data_processing.py ./
COPY db_config.py ./


CMD ["python", "app_dash.py"]
