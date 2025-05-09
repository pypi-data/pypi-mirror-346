import asyncio
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential, 
    retry_if_exception_type
)

from ..db_context import DbContext

def db_retry(retries=5, delay=1, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        @retry(
            stop=stop_after_attempt(retries),
            wait=wait_exponential(multiplier=delay, min=delay, max=delay * (backoff_factor ** (retries -1)) if retries > 0 else delay ),
            retry=retry_if_exception_type((SQLAlchemyError, asyncio.TimeoutError)),
            reraise=True
        )
        async def wrapper(*args, **kwargs):
            db_context_instance = DbContext()
            db_session = None
            try:
                async with db_context_instance:
                    db_session = db_context_instance.get_session()
                    result = await func(*args, **kwargs, session=db_session)
                    await db_session.commit()
                    return result
            except Exception as e:
                if db_session:
                    await db_session.rollback()
                print(f"Error in {func.__name__}: {e}")
                raise
            finally:
                if db_session:
                    try:
                        await db_session.close()
                    except Exception as close_exc:
                        print(f"Error closing DB session for {func.__name__}: {close_exc}")
        return wrapper
    return decorator 