from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context
import os
import sys


# Agregar la ruta del proyecto para importar los modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa Base y los modelos de SQLAlchemy
from app.core.database import Base
from app.models.users import User
from app.models.profiles import Profile
from app.models.products import Product
from app.models.transactions import Transaction

from app.core.config import settings

# Cargar configuración de logging de Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Obtener la URL de la base de datos desde la configuración o variables de entorno
DATABASE_URL = settings.DATABASE_URL
print(f"DATABASE_URL: {DATABASE_URL}")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Añadir los modelos de SQLAlchemy a la metadata de Alembic
target_metadata = Base.metadata


def run_migrations_offline():
    """Ejecuta las migraciones en modo 'offline'."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta las migraciones en modo 'online' con una conexión activa."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()