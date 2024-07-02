from clickhouse_driver import Client
from datetime import datetime
from google.protobuf.json_format import MessageToDict
from testcontainers.compose import compose
from pathlib import Path
from protos.statistics_pb2 import GetStatsOneRequest, GetTopTasksRequest, google_dot_protobuf_dot_empty__pb2
from protos.statistics_pb2_grpc import StatisticsServerStub

import asyncio
import grpc
import pytest


pytest_plugins = ('pytest_asyncio',)

service = compose.DockerCompose(Path(__file__).parent.absolute(),
                                pull=True,
                                build=True,
                                services=["kafka", "init-kafka", "clickhouse", "statistics"])
insert_likes_query = "INSERT INTO statistic.likes VALUES ({timestamp}, '{user_login}', {task_id}, '{author}')"
insert_views_query = "INSERT INTO statistic.views VALUES ({timestamp}, '{user_login}', {task_id}, '{author}')"


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    service.start()

    def cleanup():
        service.stop()

    request.addfinalizer(cleanup)


@pytest.mark.asyncio
async def test_task_stats():
    ch_client = Client(service.get_service_host("clickhouse", 9000))
    s_host = service.get_service_host("statistics", 8002)
    s_port = service.get_service_port("statistics", 8002)

    ch_client.execute(insert_likes_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="lmao", task_id="1", author="lmao"))
    ch_client.execute(insert_likes_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="kekus", task_id="1", author="lmao"))
    ch_client.execute(insert_views_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="kekus", task_id="1", author="lmao"))

    async with grpc.aio.insecure_channel(f"{s_host}:{s_port}") as channel:
        stub = StatisticsServerStub(channel)
        resp = await stub.GetStatsOne(GetStatsOneRequest(task_id=1))

    assert resp.views_num == 1
    assert resp.likes_num == 2

    async with grpc.aio.insecure_channel(f"{s_host}:{s_port}") as channel:
        stub = StatisticsServerStub(channel)
        resp = await stub.GetStatsOne(GetStatsOneRequest(task_id=2))

    assert resp.views_num == 0
    assert resp.likes_num == 0

    ch_client.execute(insert_likes_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="kekus", task_id="2", author="kekus"))
    ch_client.execute(insert_views_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="kekus", task_id="2", author="kekus"))

    async with grpc.aio.insecure_channel(f"{s_host}:{s_port}") as channel:
        stub = StatisticsServerStub(channel)
        resp = await stub.GetStatsOne(GetStatsOneRequest(task_id=2))

    assert resp.views_num == 1
    assert resp.likes_num == 1


@pytest.mark.asyncio
async def test_top_tasks():
    ch_client = Client(service.get_service_host("clickhouse", 9000))
    s_host = service.get_service_host("statistics", 8002)
    s_port = service.get_service_port("statistics", 8002)

    async with grpc.aio.insecure_channel(f"{s_host}:{s_port}") as channel:
        stub = StatisticsServerStub(channel)
        resp = await stub.GetTopTasks(GetTopTasksRequest(type="likes"))

    result = [MessageToDict(i, preserving_proto_field_name=True) for i in resp.tasks]
    assert result[0]["metric"] == "2"
    assert result[0]["author_login"] == "lmao"

    assert result[1]["metric"] == "1"
    assert result[1]["author_login"] == "kekus"

    ch_client.execute(insert_views_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="lmao", task_id="2", author="kekus"))
    ch_client.execute(insert_views_query.format(timestamp=int(round(datetime.now().timestamp())), user_login="lmao", task_id="2", author="kekus"))

    async with grpc.aio.insecure_channel(f"{s_host}:{s_port}") as channel:
        stub = StatisticsServerStub(channel)
        resp = await stub.GetTopTasks(GetTopTasksRequest(type="views"))

    result = [MessageToDict(i, preserving_proto_field_name=True) for i in resp.tasks]
    assert result[0]["metric"] == "3"
    assert result[0]["author_login"] == "kekus"

    assert result[1]["metric"] == "1"
    assert result[1]["author_login"] == "lmao"


@pytest.mark.asyncio
async def test_top_users():
    ch_client = Client(service.get_service_host("clickhouse", 9000))
    s_host = service.get_service_host("statistics", 8002)
    s_port = service.get_service_port("statistics", 8002)

    async with grpc.aio.insecure_channel(f"{s_host}:{s_port}") as channel:
        stub = StatisticsServerStub(channel)
        resp = await stub.GetTopUsers(google_dot_protobuf_dot_empty__pb2.Empty())

    result = [MessageToDict(i, preserving_proto_field_name=True) for i in resp.users]
    assert result[0]["likes"] == "2"
    assert result[0]["login"] == "lmao"

    assert result[1]["likes"] == "1"
    assert result[1]["login"] == "kekus"
