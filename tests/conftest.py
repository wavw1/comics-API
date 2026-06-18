import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from pytest_alembic.config import Config
import sqlalchemy
import pytest_asyncio
import asyncio

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost/test_postgres"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)

TestingSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db_session):
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    from app.core.db.db import get_db

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
def alembic_config():
    return Config(
        config_options={
            "file": "alembic.ini",
            "script_location": "alembic",
        }
    )

@pytest.fixture
def alembic_engine():
    """Override this fixture to provide pytest-alembic powered tests with a database handle.
    """
    return sqlalchemy.create_engine("postgresql+psycopg://postgres:123@localhost/test_postgres")