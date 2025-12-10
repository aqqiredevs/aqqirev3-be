from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv(override=True)

Base = declarative_base()

URL_DATABASE = os.getenv("DB_URL")

engine = create_async_engine(
    URL_DATABASE,
    echo=False,
    pool_pre_ping=True,
    # connect_args={"server_settings": {"statement_cache_size": "0"}}
)
sessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with sessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)