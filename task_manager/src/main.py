import asyncio

from config import settings
from grpc_server import server


async def start_server():
    server.add_insecure_port(f"{settings.me_host}:{settings.me_port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server())
