from typing import Callable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class DatabaseAdapter:
  url: str
  engine: AsyncEngine
  getSession: Callable[[], AsyncSession]

  def __init__(self, databaseUrl: str):
    self.url = databaseUrl
    self.engine = create_async_engine(self.url, echo=False)
    self.getSession = sessionmaker(
      self.engine, class_=AsyncSession, expire_on_commit=False
    )

  async def cleanDB(self):
    async with self.engine.begin() as conn:
      await conn.run_sync(Base.metadata.drop_all)
      await conn.run_sync(Base.metadata.create_all)
