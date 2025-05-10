import operator
import typing
import uuid

import sqlalchemy as sa
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

T = typing.TypeVar("T")
_DT = typing.TypeVar("_DT")
_ChoiceLabelT = typing.TypeVar("_ChoiceLabelT")
_ChoiceValueT = typing.TypeVar("_ChoiceValueT")


class QueryError(Exception): ...


class NoResultError(QueryError, NoResultFound): ...


class MultipleResultsError(QueryError, MultipleResultsFound): ...


class ExecutableQuery(typing.Generic[T]):
    def __init__(self, dbsession: AsyncSession, stmt: sa.Select[tuple[T]]) -> None:
        self.dbsession = dbsession
        self.stmt = stmt

    async def one(self) -> T:
        """Return exactly one row or raise an exception."""
        try:
            rows = await self.dbsession.scalars(self.stmt)
            return rows.one()
        except NoResultFound as ex:
            raise NoResultError from ex
        except MultipleResultsFound as ex:
            raise MultipleResultsError from ex

    async def one_or_none(self) -> T | None:
        """Return exactly one row or None.
        Note, if there are more than one row, it will raise MultipleResultsError exception.

        :param stmt: SQL statement
        :raises MultipleResultsError: if more than one row is found
        :return: T | None
        """
        try:
            rows = await self.dbsession.scalars(self.stmt)
            return rows.one_or_none()
        except MultipleResultsFound as ex:
            raise MultipleResultsError from ex

    async def one_or_raise(self, exc: Exception) -> T:
        """Return exactly one row or raise a custom exception if no row exists."""
        entity = await self.one_or_none()
        if entity is None:
            raise exc
        return entity

    async def one_or_default(self, default_value: _DT) -> T | _DT:
        entity = await self.one_or_none()
        return entity if entity else default_value

    async def all(self) -> typing.Sequence[T]:
        """Return all rows as a collection."""
        result = await self.dbsession.scalars(self.stmt)
        return result.all()

    async def iterator(self, batch_size: int = 1000) -> typing.AsyncGenerator[T, None]:
        stmt = self.stmt.execution_options(yield_per=batch_size)
        result = await self.dbsession.stream(stmt)
        async for partition in result.partitions(batch_size):
            for row in partition:
                yield row[0]

    async def exists(self) -> bool:
        stmt = sa.select(sa.exists(self.stmt))
        result = await self.dbsession.scalars(stmt)
        return result.one() is True

    async def count(self) -> int:
        stmt = sa.select(sa.func.count()).select_from(self.stmt.subquery())
        result = await self.dbsession.scalars(stmt)
        count = result.one()
        return int(count) if count else 0

    @typing.overload
    async def choices(
        self,
        label_attr: str = "",
        value_attr: str = "",
    ) -> typing.AsyncGenerator[tuple[typing.Any, typing.Any], None]:  # pragma: no cover
        yield tuple(["", ""])  # type: ignore[misc]

    @typing.overload
    async def choices(
        self,
        label_attr: typing.Callable[[T], _ChoiceLabelT],
        value_attr: typing.Callable[[T], _ChoiceValueT],
    ) -> typing.AsyncGenerator[
        tuple[_ChoiceValueT, _ChoiceLabelT], None
    ]:  # pragma: no cover
        yield tuple(["", ""])  # type: ignore[misc]

    async def choices(
        self,
        label_attr: typing.Any = str,
        value_attr: typing.Any = "id",
    ) -> typing.AsyncGenerator[tuple[_ChoiceValueT, _ChoiceLabelT], None]:
        label_getter: typing.Callable[[T], _ChoiceLabelT]
        value_getter: typing.Callable[[T], _ChoiceValueT]
        if isinstance(label_attr, str):
            label_getter = operator.attrgetter(label_attr)
        else:
            label_getter = label_attr

        if isinstance(value_attr, str):
            value_getter = operator.attrgetter(value_attr)
        else:
            value_getter = value_attr

        for item in await self.all():
            yield value_getter(item), label_getter(item)


class Query:
    def __init__(self, dbsession: AsyncSession) -> None:
        self.dbsession = dbsession

    @classmethod
    def of(cls, model_class: type[T]) -> sa.Select[tuple[T]]:
        """Return a select statement for the given model."""
        return sa.select(model_class)

    def select(self, stmt: sa.Select[tuple[T]]) -> ExecutableQuery[T]:
        return ExecutableQuery(self.dbsession, stmt)

    async def find(
        self,
        model_class: type[T],
        where_clause: sa.ColumnExpressionArgument[bool],
        *,
        options: typing.Sequence[ORMOption] = (),
    ) -> T | None:
        stmt = sa.select(model_class).where(where_clause)
        if options:
            stmt = stmt.options(*options)
        return await self.select(stmt).one_or_none()

    async def get(
        self,
        model_class: type[T],
        pk: int | str | uuid.UUID,
        *,
        options: typing.Sequence[ORMOption] = (),
    ) -> T | None:
        return await self.dbsession.get(model_class, pk, options=options)


query = Query
