from logging.config import fileConfig
from alembic import context
from app.models import Base
from app.connection.setup import DatabaseSetup

# Alembic Config object
config = context.config

# Set up logging from config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode (no DB connection)."""
    # Use DatabaseSetup to load env and build URL
    # initializes env and engine
    DatabaseSetup.initialize(create_session=False)
    engine = DatabaseSetup.get_engine()
    url = str(engine.url)  # get the connection URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with DB connection)."""
    # Use DatabaseSetup to get engine
    DatabaseSetup.initialize()
    engine = DatabaseSetup.get_engine()

    with engine.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Decide mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
