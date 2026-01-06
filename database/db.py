from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from database.models import Base

engine = create_async_engine(
    url="mysql+asyncmy://root:1234@127.0.0.1:3306/url_shortener",
    echo=True
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as connector:
        await connector.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

