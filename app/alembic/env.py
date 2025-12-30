import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context


# Ensure /app is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Now imports can see the 'app' package
from app.models.base import Base
from app.models import users_model, farmers_model, buyers_model, products_model

# Alembic Config object
config = context.config

# Load environment variables
DB_PASSWORD = os.environ.get("DB_PASSWORD", "payitpass")
DB_DATABASE = os.environ.get("DB_DATABASE", "payit_db")
DB_USER = os.environ.get("DB_USER", "root")
DB_HOST = os.environ.get("DB_HOST", "payit_db")
DB_PORT = os.environ.get("DB_PORT", "3306")

# Build the database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Override the SQLAlchemy URL in Alembic config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
