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


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    login: str
    password: str


class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
    email: Optional[str] = None
    phone_num: Optional[str] = None


class UserResponse(UserUpdate):
    login: str


class UserSchema(UserCreate):
    id: int
    first_name: str
    last_name: str
    birth_date: str
    email: str
    phone_num: str

    class Config:
        from_attributes = True


class UserDBModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    login: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String, default="")
    last_name: Mapped[str] = mapped_column(String, default="")
    birth_date: Mapped[str] = mapped_column(String, default="")
    email: Mapped[str] = mapped_column(String, default="")
    phone_num: Mapped[str] = mapped_column(String, default="")


def toUserSchema(user: UserDBModel) -> UserSchema:
    return UserSchema(id=user.id,
                      login=user.login,
                      password=user.password,
                      first_name=user.first_name,
                      last_name=user.last_name,
                      birth_date=user.birth_date,
                      email=user.email,
                      phone_num=user.phone_num)


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    service.start()
    sleep(5.0)

    def cleanup():
        service.stop()

    request.addfinalizer(cleanup)


@pytest.mark.asyncio
async def test_create_user():
    host = service.get_service_host("postgresql_gateway", 5432)
    port = service.get_service_port("postgresql_gateway", 5432)
    sessionmanager = DatabaseSessionManager(f"postgresql+asyncpg://postgres:postgres@{host}:{port}/gateway",
                                            {"echo": True})
    g_host = service.get_service_host("gateway", 8000)
    g_port = service.get_service_port("gateway", 8000)

    url = "http://{host}:{port}/users{path}"
    post_header = {"accept": "application/json", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(url.format(host=g_host, port=g_port, path="/signup"),
                                 headers=post_header,
                                 json={"login": "lol", "password": "1"})

        resp = await client.post(url.format(host=g_host, port=g_port, path="/signup"),
                                 headers=post_header,
                                 json={"login": "kekus", "password": "2"})

    async with sessionmanager.session() as session:
        resp = (await session.execute(select(UserDBModel))).scalars().all()

    result = list(map(toUserSchema, resp))
    assert len(result) == 2

    for user in result:
        if user.login == "lol":
            assert user.password != "1"
        elif user.login == "kekus":
            assert user.password != "2"
        else:
            raise Exception("Unknown user")


@pytest.mark.asyncio
async def test_update_user():
    host = service.get_service_host("postgresql_gateway", 5432)
    port = service.get_service_port("postgresql_gateway", 5432)
    sessionmanager = DatabaseSessionManager(f"postgresql+asyncpg://postgres:postgres@{host}:{port}/gateway",
                                            {"echo": True})
    g_host = service.get_service_host("gateway", 8000)
    g_port = service.get_service_port("gateway", 8000)

    url = "http://{host}:{port}/users{path}"
    token_url = "http://{host}:{port}/login{path}"

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url.format(host=g_host, port=g_port, path=""),
                                 headers={"accept": "application/json",
                                          "Content-Type": "application/x-www-form-urlencoded"},
                                 data={"username": "lol", "password": "1"})

    token = json.loads(resp.text)["access_token"]

    async with httpx.AsyncClient() as client:
        resp = await client.put(url.format(host=g_host, port=g_port, path=""),
                                headers={"accept": "application/json",
                                         "Content-Type": "application/json",
                                         "Authorization": f"Bearer {token}"},
                                json={"first_name": "meme",
                                      "last_name": "funny meme"})

    async with sessionmanager.session() as session:
        resp = (await session.execute(select(UserDBModel).where(UserDBModel.login == "lol"))).scalars().one()

    result = toUserSchema(resp)

    assert result.first_name == "meme"
    assert result.last_name == "funny meme"
