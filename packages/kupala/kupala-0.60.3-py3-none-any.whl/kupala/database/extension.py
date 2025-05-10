import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware import Middleware

from kupala.applications import Kupala
from kupala.database.manager import Database
from kupala.database.middleware import DbSessionMiddleware
from kupala.dependencies import RequestResolver


class SQLAlchemy:
    def __init__(self, databases: dict[str, Database]) -> None:
        self._databases = databases

    @contextlib.asynccontextmanager
    async def initialize(self, _: Kupala) -> typing.AsyncGenerator[None, None]:
        async with contextlib.AsyncExitStack() as stack:
            for database in self._databases.values():
                await stack.enter_async_context(database)
            yield

    def configure(self, app: Kupala) -> None:
        app.initializers.append(self.initialize)
        app.state.sqlalchemy = self
        app.dependencies.registry[AsyncSession] = RequestResolver(lambda r: r.state.dbsession)
        app.asgi_middleware.insert(0, Middleware(DbSessionMiddleware, self._databases))

    @classmethod
    def of(cls, app: Kupala) -> typing.Self:
        return typing.cast(typing.Self, app.state.sqlalchemy)

    def get_database(self, name: str) -> Database:
        return self._databases[name]

    @classmethod
    def new_session(cls, name: str) -> typing.AsyncContextManager[AsyncSession]:
        """Create a new database session."""
        return cls.of(Kupala.current()).get_database(name).session()
