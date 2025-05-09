from sqlalchemy import Column, String, Boolean, BigInteger
from ..db_context import Base

class ServiceAuthenticationKeyDto(Base):
    __tablename__ = "service_authentication_keys"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key_name = Column(String(255), nullable=False, unique=True)
    key_value = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False, default='')
    deleted = Column(Boolean, nullable=False, default=False)