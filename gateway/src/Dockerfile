FROM python:3.11.4

COPY gateway/src/ /app/src/
COPY protos/ /app/protos
COPY gateway/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV DATABASE_URL="postgresql+asyncpg://postgres:postgres@postgresql:5432/gateway"
ENV TM_HOST="task_manager"
ENV TM_PORT=8001

ENTRYPOINT ["python", "src/main.py"]
