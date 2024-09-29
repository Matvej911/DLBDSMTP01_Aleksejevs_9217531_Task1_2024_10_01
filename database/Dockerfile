FROM python:3.9-slim

WORKDIR /database

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "create_db.py"]
