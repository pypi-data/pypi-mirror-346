import os
from unittest import mock

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from kupala.database.manager import Database, NoActiveSession, on_commit
from kupala.database.models import Base
from tests.models import User

POSTGRES_URL = os.environ.get("POSTGRES_URL", "postgresql+psycopg_async://postgres:postgres@127.0.0.1/test_kupala")


class TestDatabase:
    async def test_manager_initializes_engine(self) -> None:
        database = Database("sqlite+aiosqlite:///:memory:")
        async with database as engine:
            async with engine.begin() as conn:
                result = await conn.execute(sa.text("SELECT 1"))
                assert result.scalar() == 1

    async def test_creates_normal_session(self) -> None:
        database = Database("sqlite+aiosqlite:///:memory:")
        async with database as engine:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            async with database.session() as session:
                user = User(id=1, name="test", email="test", password="test")
                session.add(user)
                await session.commit()

            async with database.session() as session:
                result = await session.execute(sa.text("select count(*) from users"))
                assert result.scalar() == 1
                assert database.current_session is session

    async def test_retrieve_current_session(self) -> None:
        database = Database("sqlite+aiosqlite:///:memory:")
        async with database as engine:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            async with database.session() as parent_session:
                assert database.current_session is parent_session

                async with database.session() as child_session:
                    assert database.current_session is child_session

                assert database.current_session is parent_session

            with pytest.raises(NoActiveSession):
                assert database.current_session

    async def test_creates_rolling_back_session(self) -> None:
        database = Database(POSTGRES_URL)
        async with database as engine:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

            async with database.session(force_rollback=True) as session:
                user = User(id=1, name="test", email="test", password="test")
                session.add(user)
                await session.commit()

            async with database.session() as session:
                result = await session.execute(sa.select(User))
                users = result.scalars().all()
                assert len(users) == 0
                assert database.current_session is session


async def test_on_commit(dbsession: AsyncSession) -> None:
    spy = mock.MagicMock()
    spy2 = mock.MagicMock()
    on_commit(dbsession, spy)
    on_commit(dbsession, spy2)
    await dbsession.commit()
    spy.assert_called_once()
    spy2.assert_called_once()
