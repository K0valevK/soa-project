import grpc

from config import settings
from protos.task_manager_pb2_grpc import TaskManagerServerStub


async def get_stub():
    async with grpc.aio.insecure_channel(f"{settings.tm_host}:{settings.tm_port}") as channel:
        stub = TaskManagerServerStub(channel)
        yield stub
