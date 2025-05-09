from sqlalchemy import Column, Integer, String, DateTime, JSON, BigInteger

from ..db_context import Base

class TaskQueueDto(Base):
    __tablename__ = "task_queue"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False)
    request = Column(JSON, nullable=False)
    status = Column(Integer, nullable=False)
    queued_at = Column(DateTime, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    result = Column(JSON, nullable=True)