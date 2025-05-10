from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from starlette.responses import Response
from starlette.testclient import TestClient

from kupala.applications import Kupala
from kupala.database.dependencies import DbSession
from kupala.database.extension import SQLAlchemy
from kupala.database.manager import Database
from kupala.routing import Route


async def inject_async_session_view(dbsession: AsyncSession) -> Response:
    return Response(dbsession.__class__.__name__)


async def inject_db_session_view(dbsession: DbSession) -> Response:
    return Response(dbsession.__class__.__name__)


def test_provides_async_session_dependency() -> None:
    app = Kupala(
        secret_key="key!",
        routes=[
            Route("/", inject_async_session_view),
        ],
        extensions=[
            SQLAlchemy(
                {
                    "default": Database("sqlite+aiosqlite:///:memory:"),
                }
            )
        ],
    )
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.text == "AsyncSession"


def test_provides_dbsession_dependency() -> None:
    app = Kupala(
        secret_key="key!",
        routes=[
            Route("/", inject_db_session_view),
        ],
        extensions=[
            SQLAlchemy(
                {
                    "default": Database("sqlite+aiosqlite:///:memory:"),
                }
            )
        ],
    )
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.text == "AsyncSession"


async def test_get_database() -> None:
    app = Kupala(
        secret_key="key!",
        routes=[
            Route("/", inject_db_session_view),
        ],
        extensions=[
            SQLAlchemy(
                {
                    "default": Database("sqlite+aiosqlite:///:memory:"),
                    "secondary": Database("sqlite+aiosqlite:///:memory:"),
                }
            )
        ],
    )
    async with app.initialize():
        database = SQLAlchemy.of(app).get_database("default")
        assert isinstance(database, Database)

        database = SQLAlchemy.of(app).get_database("secondary")
        assert isinstance(database, Database)


async def test_new_session() -> None:
    app = Kupala(
        secret_key="key!",
        routes=[
            Route("/", inject_db_session_view),
        ],
        extensions=[
            SQLAlchemy(
                {
                    "default": Database("sqlite+aiosqlite:///:memory:"),
                    "secondary": Database("sqlite+aiosqlite:///tmp/db"),
                }
            )
        ],
    )
    async with app.initialize():
        db = SQLAlchemy.of(app)
        async with db.new_session("default") as dbsession:
            assert isinstance(dbsession, AsyncSession)
            assert isinstance(dbsession.bind, AsyncEngine)
            assert str(dbsession.bind.url) == "sqlite+aiosqlite:///:memory:"

        async with db.new_session("secondary") as dbsession:
            assert isinstance(dbsession, AsyncSession)
            assert isinstance(dbsession.bind, AsyncEngine)
            assert str(dbsession.bind.url) == "sqlite+aiosqlite:///tmp/db"
