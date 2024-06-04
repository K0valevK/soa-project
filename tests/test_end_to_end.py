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
from pydantic import BaseModel
from time import sleep
from typing import Any, AsyncIterator, Optional

import asyncio
import contextlib
import httpx
import json
import pytest

pytest_plugins = ('pytest_asyncio',)

service = compose.DockerCompose(Path(__file__).parent.absolute(),
                                pull=True,
                                build=True)

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
    sleep(5.0)

    def cleanup():
        service.stop()

    request.addfinalizer(cleanup)


@pytest.mark.asyncio
async def test_create_task():
    tm_db_host = service.get_service_host("postgresql_taskm", 5432)
    tm_db_port = service.get_service_port("postgresql_taskm", 5432)
    sessionmanager = DatabaseSessionManager(
        f"postgresql+asyncpg://postgres:postgres@{tm_db_host}:{tm_db_port}/task_manager",
        {"echo": True})
    g_host = service.get_service_host("gateway", 8000)
    g_port = service.get_service_port("gateway", 8000)

    url = "http://{host}:{port}/users{path}"
    token_url = "http://{host}:{port}/login{path}"
    task_url = "http://{host}:{port}/task{path}"
    post_header = {"accept": "application/json", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(url.format(host=g_host, port=g_port, path="/signup"),
                                 headers=post_header,
                                 json={"login": "lol", "password": "1"})

        resp = await client.post(token_url.format(host=g_host, port=g_port, path=""),
                                 headers={"accept": "application/json",
                                          "Content-Type": "application/x-www-form-urlencoded"},
                                 data={"username": "lol", "password": "1"})

        token = json.loads(resp.text)["access_token"]

        resp = await client.post(task_url.format(host=g_host, port=g_port, path=""),
                                 headers={"accept": "application/json",
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {token}"},
                                 json={"name": "meme",
                                       "text": "funny meme"})
        resp = await client.post(task_url.format(host=g_host, port=g_port, path=""),
                                 headers={"accept": "application/json",
                                          "Content-Type": "application/json",
                                          "Authorization": f"Bearer {token}"},
                                 json={"name": "another meme",
                                       "text": "funnier meme"})

    await asyncio.sleep(10.0)

    async with sessionmanager.session() as session:
        resp = (await session.execute(select(TaskDBModel))).scalars().all()

    result = list(map(toTaskSchema, resp))
    for task in result:
        if task.creator_login == "lol":
            if task.name == "meme":
                assert task.text == "funny meme"
            elif task.name == "another meme":
                assert task.text == "funnier meme"
            else:
                raise Exception("Unknwon task added")
        else:
            raise Exception("Unknwon user added")


@pytest.mark.asyncio
async def test_get_likes():
    g_host = service.get_service_host("gateway", 8000)
    g_port = service.get_service_port("gateway", 8000)

    token_url = "http://{host}:{port}/login{path}"
    task_url = "http://{host}:{port}/task{path}"
    stats_url = "http://{host}:{port}/statistics{path}"

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url.format(host=g_host, port=g_port, path=""),
                                 headers={"accept": "application/json",
                                          "Content-Type": "application/x-www-form-urlencoded"},
                                 data={"username": "lol", "password": "1"})
        token = json.loads(resp.text)["access_token"]
        resp = await client.post(task_url.format(host=g_host, port=g_port, path="/1/like"),
                                 headers={"accept": "application/json",
                                          "Authorization": f"Bearer {token}"})
        resp = await client.post(task_url.format(host=g_host, port=g_port, path="/1/like"),
                                 headers={"accept": "application/json",
                                          "Authorization": f"Bearer {token}"})
        resp = await client.post(task_url.format(host=g_host, port=g_port, path="/2/like"),
                                 headers={"accept": "application/json",
                                          "Authorization": f"Bearer {token}"})

    await asyncio.sleep(10.0)

    async with httpx.AsyncClient() as client:
        resp = await client.get(stats_url.format(host=g_host, port=g_port, path="/tasks/likes"),
                                headers={"accept": "application/json"})

    result = json.loads(resp.text)
    assert result[0]["id"] == "1"
    assert result[0]["metric"] == "2"
    assert result[0]["author_login"] == "lol"
    assert result[1]["id"] == "2"
    assert result[1]["metric"] == "1"
    assert result[1]["author_login"] == "lol"
