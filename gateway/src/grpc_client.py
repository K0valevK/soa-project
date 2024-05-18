import grpc

from config import settings
from protos.task_manager_pb2_grpc import TaskManagerServerStub
from protos.statistics_pb2_grpc import StatisticsServerStub


async def get_stub():
    async with grpc.aio.insecure_channel(f"{settings.tm_host}:{settings.tm_port}") as channel:
        stub = TaskManagerServerStub(channel)
        yield stub


async def get_stats_stub():
    async with grpc.aio.insecure_channel(f"{settings.statistics_host}:{settings.statistics_port}") as channel:
        stub = StatisticsServerStub(channel)
        yield stub
