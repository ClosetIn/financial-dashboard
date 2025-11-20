import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.endpoints import router as api_router
from app.core.config import settings

# Настраиваем логирование
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format=settings.log_format,
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Фабрика для создания FastAPI приложения

    Returns:
        FastAPI: Настроенное приложение
    """
    application = FastAPI(
        title=settings.project_name,
        description="Real-time financial data dashboard API",
        version=settings.version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Настраиваем CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем роутеры
    application.include_router(api_router, prefix=settings.api_prefix)
    return application


# Создаём экземпляр приложения
app = create_application()


@app.on_event("startup")
async def startup_event() -> None:
    """Действия при запуске приложения"""
    logger.info(f"Starting {settings.project_name} v{settings.version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Log level: {settings.log_level}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Действия при остановке приложения"""
    logger.info("Shutting down application")


@app.get("/")
async def root() -> dict:
    """
    Корневой эндпоинт.

    Returns:
        dict: Основная информация о API
    """
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": settings.version,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs" if settings.debug else None,
    }


@app.get("/health")
async def health_check() -> JSONResponse:
    """
    Health check эндпоинт для мониторинга.

    Returns:
        JSONResponse: Статус здоровья приложения
    """
    from app.db.session import test_database_connection

    db_status = "healthy" if await test_database_connection() else "unhealthy"

    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.version,
        "services": {
            "api": "operational",
            "database": db_status,
            "cbr_api": "operational",
            "moex_api": "operational",
        },
    }

    return JSONResponse(content=health_data)


# Для запуска напрямую
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
    )
