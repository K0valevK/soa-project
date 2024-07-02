from testcontainers.compose import compose
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base
from pathlib import Path
from protos.task_manager_pb2 import CreateUserRequest, CreateTaskRequest, UpdateTaskRequest
from protos.task_manager_pb2_grpc import TaskManagerServerStub
from pydantic import BaseModel
from time import sleep
from typing import Any, AsyncIterator, Optional

import asyncio
import contextlib
import grpc
import pytest


pytest_plugins = ('pytest_asyncio',)

service = compose.DockerCompose(Path(__file__).parent.absolute(),
                                pull=True,
                                build=True,
                                services=["postgresql_taskm", "migrations_tm", "task_manger"])
Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class TaskBase(BaseModel):
    pass


class TaskCreate(TaskBase):
    creator_login: str
    name: str
    text: str


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    text: Optional[str] = None


class TaskSchema(TaskCreate):
    id: int

    class Config:
        from_attributes = True


class TaskDBModel(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    creator_login: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)


def toTaskSchema(task: TaskDBModel) -> TaskSchema:
    return TaskSchema(id=task.id,
                      creator_login=task.creator_login,
                      name=task.name,
                      text=task.text)


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    service.start()
    sleep(3.0)

    def cleanup():
        service.stop()

    request.addfinalizer(cleanup)


@pytest.mark.asyncio
async def test_create_task():
    host = service.get_service_host("postgresql_taskm", 5432)
    port = service.get_service_port("postgresql_taskm", 5432)
    sessionmanager = DatabaseSessionManager(f"postgresql+asyncpg://postgres:postgres@{host}:{port}/task_manager",
                                            {"echo": True})
    tm_host = service.get_service_host("task_manger", 8001)
    tm_port = service.get_service_port("task_manger", 8001)

    async with grpc.aio.insecure_channel(f"{tm_host}:{tm_port}") as channel:
        stub = TaskManagerServerStub(channel)
        resp = await stub.CreateUser(CreateUserRequest(login="lmao"))
        resp = await stub.CreateUser(CreateUserRequest(login="kekus"))

        resp = await stub.CreateTask(CreateTaskRequest(creator_login="lmao", name="1", text="empty"))
        resp = await stub.CreateTask(CreateTaskRequest(creator_login="lmao", name="2", text="empty2"))
        resp = await stub.CreateTask(CreateTaskRequest(creator_login="kekus", name="3", text="empty3"))

    async with sessionmanager.session() as session:
        resp = (await session.execute(select(TaskDBModel))).scalars().all()

    result = list(map(toTaskSchema, resp))
    for task in result:
        if task.creator_login == "lmao":
            assert task.name in ["1", "2"]
        elif task.creator_login == "kekus":
            assert task.name in ["3"]
        else:
            raise Exception("Unknwon user added")


@pytest.mark.asyncio
async def test_update_task():
    host = service.get_service_host("postgresql_taskm", 5432)
    port = service.get_service_port("postgresql_taskm", 5432)
    sessionmanager = DatabaseSessionManager(f"postgresql+asyncpg://postgres:postgres@{host}:{port}/task_manager",
                                            {"echo": True})
    tm_host = service.get_service_host("task_manger", 8001)
    tm_port = service.get_service_port("task_manger", 8001)

    async with sessionmanager.session() as session:
        resp = (await session.execute(select(TaskDBModel).where(TaskDBModel.name == "1"))).scalars().all()

    result = list(map(toTaskSchema, resp))
    if len(result) != 1:
        raise Exception("Too many tasks")

    assert result[0].text == "empty"

    async with grpc.aio.insecure_channel(f"{tm_host}:{tm_port}") as channel:
        stub = TaskManagerServerStub(channel)
        resp = await stub.UpdateTask(UpdateTaskRequest(id=1, creator_login="lmao", new_name="new1", text="No more empty"))

    async with sessionmanager.session() as session:
        resp = (await session.execute(select(TaskDBModel).where(TaskDBModel.name == "new1"))).scalars().one()

    result = toTaskSchema(resp)

    assert result.text == "No more empty"
