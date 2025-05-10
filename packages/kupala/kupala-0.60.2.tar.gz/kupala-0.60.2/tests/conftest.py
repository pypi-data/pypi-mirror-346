import typing

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from starlette.applications import Starlette
from starlette.routing import BaseRoute
from starlette.testclient import TestClient
from starlette.types import ASGIApp

from kupala.database.models import Base
from kupala.routing import Middleware, RouteGroup
from tests.models import Profile, User


class AppFactory(typing.Protocol):  # pragma: nocover
    def __call__(
        self,
        debug: bool = True,
        middleware: list[Middleware] | None = None,
        routes: typing.Iterable[BaseRoute] | None = None,
        **kwargs: typing.Any,
    ) -> Starlette: ...


class ClientFactory(typing.Protocol):  # pragma: nocover
    def __call__(
        self,
        debug: bool = True,
        middleware: list[Middleware] | None = None,
        routes: typing.Iterable[BaseRoute] | None = None,
        raise_server_exceptions: bool = True,
        app: ASGIApp | None = None,
        **kwargs: typing.Any,
    ) -> TestClient: ...


@pytest.fixture
def test_app_factory() -> AppFactory:
    def factory(*args: typing.Any, **kwargs: typing.Any) -> Starlette:
        kwargs.setdefault("debug", True)
        kwargs.setdefault("routes", RouteGroup())
        kwargs.setdefault("middleware", [])
        return Starlette(*args, **kwargs)

    return factory


@pytest.fixture
def test_client_factory(test_app_factory: AppFactory) -> ClientFactory:
    def factory(**kwargs: typing.Any) -> TestClient:
        raise_server_exceptions = kwargs.pop("raise_server_exceptions", True)
        app = kwargs.pop("app", test_app_factory(**kwargs))
        return TestClient(app, raise_server_exceptions=raise_server_exceptions)

    return typing.cast(ClientFactory, factory)


@pytest.fixture
def routes() -> RouteGroup:
    return RouteGroup()


@pytest.fixture()
async def dbengine() -> typing.AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        yield engine


@pytest.fixture
async def dbsession(dbengine: AsyncEngine) -> typing.AsyncGenerator[AsyncSession, None]:
    async with dbengine.connect() as conn:
        async with conn.begin() as tx:
            async with async_sessionmaker(
                bind=conn,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            )() as dbsession:
                try:
                    yield dbsession
                finally:
                    await tx.rollback()


@pytest.fixture(autouse=True)
async def setup_users(dbsession: AsyncSession) -> None:
    users = [
        User(id=1, name="user_01", email="01@user", password="", profile=Profile(bio="bio_01")),
        User(id=2, name="user_02", email="02@user", password="", profile=Profile(bio="bio_02")),
        User(id=3, name="user_03", email="03@user", password="", profile=Profile(bio="bio_03")),
        User(id=4, name="user_04", email="04@user", password="", profile=Profile(bio="bio_04")),
        User(id=5, name="user_05", email="05@user", password="", profile=Profile(bio="bio_05")),
        User(id=6, name="user_06", email="06@user", password="", profile=Profile(bio="bio_06")),
        User(id=7, name="user_07", email="07@user", password="", profile=Profile(bio="bio_07")),
        User(id=8, name="user_08", email="08@user", password="", profile=Profile(bio="bio_08")),
        User(id=9, name="user_09", email="09@user", password="", profile=Profile(bio="bio_09")),
    ]
    dbsession.add_all(users)
    await dbsession.flush()


@pytest.fixture()
def user() -> User:
    return User(email="root@localhost")
