from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.settings.config import settings

engine = create_async_engine(settings.DATABASE_URL_ASYNC, echo=True, future=True)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
