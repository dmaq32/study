from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import pool
from logging.config import fileConfig
from alembic import context
import asyncio

# Импортируйте модели из вашего приложения
from app.models import Base  # Убедитесь, что Base правильно импортирован

# Интерпретация файла конфигурации Alembic
config = context.config

# Установите файл конфигурации для логирования
fileConfig(config.config_file_name)

# Укажите строку подключения к базе данных
target_metadata = Base.metadata

def run_migrations_offline():
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

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
        echo=True
    )

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())

def do_run_migrations(connection: AsyncConnection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

run_migrations_online()
