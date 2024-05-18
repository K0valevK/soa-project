from config import settings
from grpc_server import server
from kafka_consumer import kafka_likes_consumer, kafka_views_consumer
from kafka_wrappers import likes_clickhouse_wrapper, views_clickhouse_wrapper

import asyncio


async def start_kafka():
    pass


async def start_server():
    await kafka_likes_consumer.init_consumer(settings.kafka_topic_likes,
                                             likes_clickhouse_wrapper)
    task = asyncio.create_task(kafka_likes_consumer.consume())

    await kafka_views_consumer.init_consumer(settings.kafka_topic_views,
                                             views_clickhouse_wrapper)
    task2 = asyncio.create_task(kafka_views_consumer.consume())

    server.add_insecure_port(f"{settings.me_host}:{settings.me_port}")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    # asyncio.run(start_kafka())
    asyncio.get_event_loop().run_until_complete(start_server())
