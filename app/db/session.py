import logging
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Настройка логирования
logger = logging.getLogger(__name__)

# Асинхронный движок для приложения
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Логировать SQL запросы в debug режиме
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Проверять соединение перед использованием
)

# Синхронный движок для Alembic
sync_engine = create_engine(settings.sync_database_url)

# Асинхронная сессия
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Синхронная сессия (для Alembic и тестов)
SyncSessionLocal = sessionmaker(
    sync_engine,
    autoflush=False,
    autocommit=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для получения асинхронной сессии БД.

    Yields:
        AsyncSession: Асинхронная сессия БД
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Generator[Session, None, None]:
    """
    Dependency для получения синхронной сессии БД (для тестов).

    Yields:
        Session: Синхронная сессия БД
    """
    db = SyncSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


async def test_database_connection() -> bool:
    """Тестирование подключения к базе данных"""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            logger.info("Database connection test: SUCCESS")
            return True
    except Exception as e:
        logger.error(f"Database connection test: FAILED - {e}")
        return False
