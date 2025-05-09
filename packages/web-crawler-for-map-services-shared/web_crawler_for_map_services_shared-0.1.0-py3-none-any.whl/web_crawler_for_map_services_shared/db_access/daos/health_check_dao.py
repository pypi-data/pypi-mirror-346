from typing import Callable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.retry_decorator import db_retry
from ..db_context import DbContext

class HealthCheckDao:
    def __init__(self):
        self.get_db_context: Callable[[], DbContext] = DbContext

    @db_retry()
    async def check_db_connection(self, *, session: AsyncSession) -> bool:
        try:
            await session.execute(select(1))
            return True
        except Exception:
            return False 