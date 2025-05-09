from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Optional, Any, Dict

from ..db_context import DbContext
from ..dtos.task_queue_dto import TaskQueueDto
from ...enums.crawl_status import CrawlStatus
from ..utils.retry_decorator import db_retry

class TaskQueueDao:
    def __init__(self):
        def _get_db_context_factory() -> DbContext:
            return DbContext()
        self.get_db_context_factory: Callable[[], DbContext] = _get_db_context_factory

    @db_retry()
    async def get_task_by_session_id(self, session_id: str, *, session: AsyncSession) -> Optional[TaskQueueDto]:
        stmt = select(TaskQueueDto).where(TaskQueueDto.session_id == session_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @db_retry()
    async def create_task(self, session_id: str, request_data: Dict[str, Any], *, session: AsyncSession) -> None:
        new_task = TaskQueueDto(
            session_id=session_id,
            status=CrawlStatus.QUEUED,
            request=request_data
        )
        session.add(new_task)

    
    @db_retry()
    async def update_task(self, session_id: str, status: CrawlStatus,
        processed_at: Optional[datetime] = None,
        result: Optional[Dict[str, Any]] = None, *, session: AsyncSession) -> None:

        stmt = select(TaskQueueDto).where(TaskQueueDto.session_id == session_id)
        task_to_update = (await session.execute(stmt)).scalar_one_or_none()

        if task_to_update is None:
            print(f"Task with session_id {session_id} not found")
            return

        task_to_update.status = status
        if processed_at is not None:
            task_to_update.processed_at = processed_at
        if result is not None:
            task_to_update.result = result
        
        session.add(task_to_update)
    