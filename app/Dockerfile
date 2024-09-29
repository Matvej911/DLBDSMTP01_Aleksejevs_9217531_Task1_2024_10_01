FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY best_model.pkl ./
COPY scaler.pkl ./

CMD ["python", "app.py"]  

