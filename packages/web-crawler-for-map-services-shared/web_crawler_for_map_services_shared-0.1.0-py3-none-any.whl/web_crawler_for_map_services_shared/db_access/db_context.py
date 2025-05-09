import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()

class DbContext:
    def __init__(self, pool_size: int = 5, max_overflow: int = 10, pool_pre_ping: bool = True, echo_pool: bool = False):
        
        self.db_user = os.getenv("DB_USER", "your_default_user")
        self.db_password = os.getenv("DB_PASSWORD", "your_default_password")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "your_default_db_name")
        
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_pre_ping = pool_pre_ping
        self.echo_pool = echo_pool

        self.database_url = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        self.engine = None
        self.SessionLocal = None

    async def __aenter__(self):
        if self.engine is not None:
            return self
        try:
            self.engine = create_async_engine(
                self.database_url, 
                pool_size=self.pool_size, 
                max_overflow=self.max_overflow, 
                pool_pre_ping=self.pool_pre_ping,
                echo_pool=self.echo_pool
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)
            return self
        except ImportError:
            print("Error: asyncpg is not installed. Please install it for asynchronous PostgreSQL support with SQLAlchemy.")
            if self.engine:
                await self.engine.dispose()
                self.engine = None
            raise 
        except SQLAlchemyError as e:
            print(f"Error creating SQLAlchemy async engine or session factory in __aenter__ for {self.database_url}: {e}")
            if self.engine:
                await self.engine.dispose()
                self.engine = None
            raise

    def get_session(self) -> AsyncSession:
        return self.SessionLocal()
            
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            await self.engine.dispose()
            self.engine = None 
            self.SessionLocal = None