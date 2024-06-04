from aiokafka import AIOKafkaProducer
from clickhouse_driver import Client
from datetime import datetime
from testcontainers.compose import compose
from pathlib import Path

import asyncio
import contextlib
import json
import pytest


pytest_plugins = ('pytest_asyncio',)

service = compose.DockerCompose(Path(__file__).parent.absolute(),
                                pull=True,
                                build=True,
                                services=["kafka", "init-kafka", "clickhouse", "statistics"])


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


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    service.start()

    def cleanup():
        service.stop()

    request.addfinalizer(cleanup)


@pytest.mark.asyncio
async def test_post_like():
    ch_client = Client(service.get_service_host("clickhouse", 9000))
    s_host = service.get_service_host("statistics", 8002)
    s_port = service.get_service_port("statistics", 8002)

    kafka_host = service.get_service_host("kafka", 9092)
    kafka_port = service.get_service_port("kafka", 9092)
    KAFKA_CONF = {"bootstrap_servers": f"{kafka_host}:{kafka_port}"}
    kafka_producer = KafkaProducerSessionManager(KAFKA_CONF)

    await kafka_producer.init_producer()

    async with kafka_producer.session() as session:
        await send_message(session, "likes", {"user_login": "lmao",
                                              "timestamp": int(round(datetime.now().timestamp())),
                                              "task_id": 1,
                                              "author": "lmao"})

    await asyncio.sleep(5.0)

    resp = ch_client.execute("SELECT * FROM statistic.likes")
    assert resp[0][1] == "lmao"
    assert resp[0][2] == 1
    assert resp[0][3] == "lmao"

    async with kafka_producer.session() as session:
        await send_message(session, "likes", {"user_login": "kekus",
                                              "timestamp": int(round(datetime.now().timestamp())),
                                              "task_id": 2,
                                              "author": "kekus"})

    await asyncio.sleep(5.0)

    resp = ch_client.execute("SELECT * FROM statistic.likes")
    for row in resp:
        if row[1] == "lmao":
            assert row[2] == 1
            assert row[3] == "lmao"
        elif row[1] == "kekus":
            assert row[2] == 2
            assert row[3] == "kekus"
        else:
            raise Exception("Unknown user")

    await kafka_producer.stop()


@pytest.mark.asyncio
async def test_post_view():
    ch_client = Client(service.get_service_host("clickhouse", 9000))
    s_host = service.get_service_host("statistics", 8002)
    s_port = service.get_service_port("statistics", 8002)

    kafka_host = service.get_service_host("kafka", 9092)
    kafka_port = service.get_service_port("kafka", 9092)
    KAFKA_CONF = {"bootstrap_servers": f"{kafka_host}:{kafka_port}"}
    kafka_producer = KafkaProducerSessionManager(KAFKA_CONF)

    await kafka_producer.init_producer()

    async with kafka_producer.session() as session:
        await send_message(session, "views", {"user_login": "lmao",
                                              "timestamp": int(round(datetime.now().timestamp())),
                                              "task_id": 1,
                                              "author": "lmao"})

    await asyncio.sleep(5.0)

    resp = ch_client.execute("SELECT * FROM statistic.views")
    assert resp[0][1] == "lmao"
    assert resp[0][2] == 1
    assert resp[0][3] == "lmao"

    async with kafka_producer.session() as session:
        await send_message(session, "views", {"user_login": "kekus",
                                              "timestamp": int(round(datetime.now().timestamp())),
                                              "task_id": 2,
                                              "author": "kekus"})

    await asyncio.sleep(5.0)

    resp = ch_client.execute("SELECT * FROM statistic.views")
    for row in resp:
        if row[1] == "lmao":
            assert row[2] == 1
            assert row[3] == "lmao"
        elif row[1] == "kekus":
            assert row[2] == 2
            assert row[3] == "kekus"
        else:
            raise Exception("Unknown user")

    await kafka_producer.stop()
