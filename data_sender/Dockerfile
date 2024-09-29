FROM python:3.9-slim

WORKDIR /data_sender

COPY data_sender.py ./
COPY df_testing_without_target.csv ./
COPY requirements2.txt ./

RUN pip install --no-cache-dir -r requirements2.txt

CMD ["python", "data_sender.py"]
