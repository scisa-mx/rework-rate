import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# Añadir tu path para importar settings y modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar configuración y modelos
from core.settings.settings import Settings 
from database import Base  # Ajusta esto según tu estructura real

from models.rework import ReworkDataDB 
from models.tags import TagDB
from models.repository import RepositoryEntity

# Config Alembic
config = context.config
fileConfig(config.config_file_name)

# Cargar settings y metadata
settings = Settings()
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = str(settings.sqlalchemy_url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    engine = create_engine(settings.sqlalchemy_url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

