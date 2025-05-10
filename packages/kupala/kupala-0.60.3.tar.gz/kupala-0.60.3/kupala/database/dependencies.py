import typing

from sqlalchemy.ext.asyncio import AsyncSession

from kupala.dependencies import RequestResolver

type DbSession = typing.Annotated[AsyncSession, RequestResolver(lambda r: r.state.dbsession)]
