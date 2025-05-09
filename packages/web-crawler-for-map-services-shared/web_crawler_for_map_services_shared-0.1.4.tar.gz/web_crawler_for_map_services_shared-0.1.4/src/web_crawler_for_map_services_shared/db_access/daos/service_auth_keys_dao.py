from typing import Callable
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from ..db_context import DbContext
from ..dtos.service_authentication_key_dto import ServiceAuthenticationKeyDto
from ..utils.retry_decorator import db_retry

class ServiceAuthKeysDao:
    def __init__(self):
        def _get_db_context_factory() -> DbContext:
            return DbContext()
        self.get_db_context_factory: Callable[[], DbContext] = _get_db_context_factory

    @db_retry()
    async def is_valid_key(self, key_value: str, *, session: AsyncSession) -> bool:
        stmt = select(exists().where(
            ServiceAuthenticationKeyDto.key_value == key_value,
            ServiceAuthenticationKeyDto.deleted == False
        ))
        return (await session.execute(stmt)).scalar_one()
