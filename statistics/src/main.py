from config import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from kafka_consumer import kafka_likes_consumer, kafka_views_consumer
from kafka_wrappers import likes_clickhouse_wrapper, views_clickhouse_wrapper

import asyncio
import uvicorn
from clickhouse import ch_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_likes_consumer.init_consumer(settings.kafka_topic_likes,
                                             likes_clickhouse_wrapper)
    task = asyncio.create_task(kafka_likes_consumer.consume())

    await kafka_views_consumer.init_consumer(settings.kafka_topic_views,
                                             views_clickhouse_wrapper)
    task2 = asyncio.create_task(kafka_views_consumer.consume())

    yield
    await kafka_likes_consumer.stop()
    await kafka_views_consumer.stop()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/docs")


if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.me_host, port=settings.me_port, reload=True)
