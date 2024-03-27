import contextlib
import grpc

from config import settings
from protos import task_manager_pb2_grpc


async def get_stub():
    async with grpc.aio.insecure_channel(f"{settings.tm_host}:{settings.tm_port}") as channel:
        stub = task_manager_pb2_grpc.TaskManagerServerStub(channel)
        yield stub
