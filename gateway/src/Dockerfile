FROM python:3.11.4

COPY gateway/src/ /app/src/
COPY protos/ /app/protos
COPY gateway/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV DATABASE_URL="postgresql+asyncpg://postgres:postgres@postgresql_gateway:5432/gateway"
ENV TM_HOST="task_manager"
ENV TM_PORT=8001
ENV STATISTICS_HOST="statistics"
ENV STATISTICS_PORT=8002
ENV KAFKA_HOST="kafka"
ENV KAFKA_PORT=29092

ENTRYPOINT ["python", "src/main.py"]
