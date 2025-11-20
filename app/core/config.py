from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""

    project_name: str = "Financial Dashboard"
    debug: bool = True
    version: str = "0.1.0"

    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = ["*"]

    # Настройки базы данных (День 2)
    database_url: str = (
        "postgresql+asyncpg://admin:password@localhost:5432/financial_dashboard"
    )
    sync_database_url: str = (
        "postgresql://admin:password@localhost:5432/financial_dashboard"
    )
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Настройки внешних API
    cbr_api_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    moex_api_url: str = "https://iss.moex.com/iss"
    api_timeout: int = 10

    # Логирование
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


def get_settings() -> Settings:
    """Возвращает экземпляр настроект (для dependency injection)"""
    return settings
