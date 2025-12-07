"""
setup.py

Centralized, environment-aware database setup using .env files.
Supports development and test environments.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from app.utils.errors import DatabaseNotInitializedError, UnknownEnvironmentError
from app.utils.logger import logger


class DatabaseSetup:
    """
    Singleton-style database setup. Ensures one engine and session per process.
    """
    _engine = None
    _SessionLocal = None
    _session: Session = None

    @classmethod
    def initialize(cls):
        """
        Initializes engine and session depending on ENV.
        Subsequent calls return the existing session.
        """
        if cls._session is not None:
            return cls._session

        env = os.getenv("ENV", "development").lower()
        dotenv_file = f".env.{env}.local"

        if env not in ("development", "test"):
            raise UnknownEnvironmentError(f"Unknown environment: {env}")

        load_dotenv(dotenv_file)

        user = os.getenv("MYSQL_DB_USER")
        password = os.getenv("MYSQL_DB_PASSWORD")
        host = os.getenv("MYSQL_DB_HOST")
        database = os.getenv("MYSQL_DB_NAME")
        port = os.getenv("MYSQL_DB_PORT", "3306")

        if not all([user, password, host, database]):
            raise DatabaseNotInitializedError(
                "Missing database environment variables.")

        # Create engine and session factory
        cls._engine = create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}",
            echo=False
        )
        cls._SessionLocal = sessionmaker(bind=cls._engine)
        cls._session = cls._SessionLocal

        # Test connection
        try:
            cls._session.execute(text("SELECT 1"))
            logger.info("Database connection alive for %s environment!", env)
        except OperationalError as e:
            logger.error(
                "Could not connect to the %s database: %s", env, str(e))
            cls._session = None
            raise

        return cls._session

    @classmethod
    def get_session(cls) -> Session:
        """
        Returns the current session. Must call initialize() first.
        """
        if cls._session is None:
            raise DatabaseNotInitializedError(
                "DatabaseSetup not initialized. Call initialize() first."
            )
        return cls._session

    @classmethod
    def get_engine(cls):
        """
        Returns the current engine. Must call initialize() first.
        """
        if cls._engine is None:
            raise DatabaseNotInitializedError(
                "DatabaseSetup not initialized. Call initialize() first."
            )
        return cls._engine

    @classmethod
    def close(cls):
        """
        Closes the session if it exists.
        """
        if cls._session:
            cls._session.close()
            logger.info("Database session closed.")
            cls._session = None
