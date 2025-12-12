"""Fixtures for setting up and tearing down the test database."""
# conftest.py
import os
import sys
import pytest
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from app.connection.setup import DatabaseSetup
from app.models.base import Base


sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ["ENV"] = "test"


@pytest.fixture(scope="session", autouse=True)
def run_alembic_upgrade():
    """Automatically upgrade the database before tests."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def setup_test_db():
    """Set up the test database for the test session."""

    # Initialize database
    session = DatabaseSetup.initialize()
    engine = DatabaseSetup.get_engine()

    # Drop and create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield session

    # Clean up after all tests
    Base.metadata.drop_all(bind=engine)  # delete all tables from sqlalchemy
    DatabaseSetup.close()


@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """Provide a clean session for each test."""
    session = setup_test_db

    # Truncate all tables before test (handle FK constraints)
    conn = session.connection()
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    for table in reversed(Base.metadata.sorted_tables):
        conn.execute(table.delete())
    conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    session.commit()

    yield session

    # Rollback any changes to keep session clean
    session.rollback()
