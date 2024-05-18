from aiokafka import AIOKafkaProducer
from config import settings

import contextlib
import json


class KafkaProducerSessionManager:
    def __init__(self, kafka_conf):
        self._kafka_conf = kafka_conf
        self._kafka_producer: AIOKafkaProducer = None

    async def init_producer(self):
        self._kafka_producer = AIOKafkaProducer(**self._kafka_conf)
        await self._kafka_producer.start()

    async def stop(self):
        await self._kafka_producer.stop()

    @contextlib.asynccontextmanager
    async def session(self):
        if self._kafka_producer is None:
            raise Exception("Kafka producer is not initialized")

        yield self._kafka_producer


async def send_message(producer: AIOKafkaProducer, topic: str, value=None, key=None, headers=None):
    return await producer.send(topic, json.dumps(value).encode("ascii"), key=key, headers=headers)


KAFKA_CONF = {"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}"}
kafka_producer = KafkaProducerSessionManager(KAFKA_CONF)


async def get_kafka_producer():
    async with kafka_producer.session() as session:
        yield session
