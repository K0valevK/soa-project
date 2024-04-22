FROM python:3.11.4

COPY statistics/src/ /app/src/
COPY statistics/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV KAFKA_HOST="kafka"
ENV KAFKA_PORT=29092
ENV CH_HOST="clickhouse"
ENV CH_PORT=9000

ENTRYPOINT ["python", "src/main.py"]
