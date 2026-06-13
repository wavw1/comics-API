from pytest_alembic.config import Config
import pytest
import sqlalchemy

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