FROM python:3.11.4

COPY task_manager/src/ /app/src/
COPY protos/ /app/protos
COPY task_manager/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV DATABASE_URL="postgresql+asyncpg://postgres:postgres@postgresql_taskm:5432/task_manager"

ENTRYPOINT ["python", "src/main.py"]
