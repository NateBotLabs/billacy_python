"""
setup.py

Environment-aware database setup using different .env files
(development vs test).
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
    Singleton-style database setup with environment-specific configuration.
    """
    _engine = None
    _SessionLocal = None
    session: Session = None

    @classmethod
    def initialize(cls):
        """
        Initializes the engine and session depending on ENV.
        """
        if cls.session is not None:
            return cls.session

        env = os.getenv("ENV", "development").lower()

        # Load the correct .env file
        if env == "development":
            load_dotenv(".env.development.local")
        elif env == "test":
            load_dotenv(".env.test.local")
        else:
            raise UnknownEnvironmentError(f"Unknown environment: {env}")

        # Read DB credentials (same variable names in both files)
        user = os.getenv("MYSQL_DB_USER")
        password = os.getenv("MYSQL_DB_PASSWORD")
        host = os.getenv("MYSQL_DB_HOST")
        database = os.getenv("MYSQL_DB_NAME")

        cls._engine = create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{host}/{database}",
            echo=False
        )
        # create a fresh, callable session factory and use it to open a session
        session_factory = sessionmaker(bind=cls._engine)
        cls._SessionLocal = session_factory
        cls.session = session_factory()

        # Test connection
        try:
            cls.session.execute(text("SELECT 1"))
            logger.info("Database connection alive for %s environment!", env)
        except OperationalError:
            logger.error("Error: Could not connect to the %s database.", env)
            cls.session = None

        return cls.session

    @classmethod
    def get_session(cls):
        """
        Returns the current database session.
        Raises DatabaseNotInitializedError if the session is not initialized.
        """
        if cls.session is None:
            raise DatabaseNotInitializedError(
                "DatabaseSetup not initialized. Call initialize() first.")
        return cls.session

    @classmethod
    def get_engine(cls):
        """
        Returns the current database engine.
        Raises DatabaseNotInitializedError if the engine is not initialized.
        """
        if cls._engine is None:
            raise DatabaseNotInitializedError(
                "DatabaseSetup not initialized. Call initialize() first.")
        return cls._engine

    @classmethod
    def close(cls):
        """
        Closes the current database session if it exists.
        """
        if cls.session:
            cls.session.close()
            logger.info("Database session closed.")
            cls.session = None
