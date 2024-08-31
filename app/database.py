from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import PG_DSN

engine = create_async_engine(PG_DSN, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session