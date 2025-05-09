from sqlalchemy import Column, Integer, String, Boolean, BigInteger, CHAR

from ..db_context import Base

class ProxyConfigDto(Base):
    __tablename__ = "proxy_config"
    __table_args__ = {'schema': 'public'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    proxy_ip = Column(String(50), nullable=False)
    proxy_port = Column(Integer, nullable=False)
    proxy_user = Column(String, nullable=True)
    proxy_pass = Column(String, nullable=True)
    protocol = Column(String(5), nullable=False)
    source = Column(String, nullable=True)
    country = Column(CHAR(2), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False) 