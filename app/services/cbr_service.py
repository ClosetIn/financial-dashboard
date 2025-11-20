import json
import logging
from datetime import datetime
from types import TracebackType
from typing import Any, Dict, Optional, Type

import aiohttp
from pydantic import BaseModel, field_validator

# Настраиваем логирование
logger = logging.getLogger(__name__)


class CurrencyRate(BaseModel):
    """Модель для хранения данных о курсе валюты."""

    currency: str
    rate: float
    change: float
    change_percent: float
    timestamp: datetime

    @field_validator("rate", "change", "change_percent")
    @classmethod
    def validate_positive_number(cls: Any, v: float) -> float:
        """Валидация числовых значений"""
        if v < 0:
            logger.warning(f"Negative value detected: {v}")
        return round(v, 4)


class CBRService:
    """Сервис для работы с API Центрального Банка России"""

    def __init__(self) -> None:
        self.base_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)
        self.tracked_currencies = ["USD", "EUR", "CNY", "GBP", "JPY"]
        self._cache: Optional[Dict[str, CurrencyRate]] = None
        self._cache_timestamp: Optional[datetime] = None

    async def __aenter__(self) -> "CBRService":
        """Асинхронный контекстный менеджер"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Закрытие сессии при выходе из контекста"""
        if self.session:
            await self.session.close()

    async def get_rates(self) -> Dict[str, CurrencyRate]:
        """
        Получает актуальные курсы валют от ЦБ РФ

        Returns:
            Dict[str, CurrencyRate]: Словарь с курсами валют
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url,
                    timeout=aiohttp.ClientTimeout(total=10),
                    headers={"Accept": "application/json"},
                ) as response:
                    if response.status != 200:
                        self.logger.error(f"CBR API returned status {response.status}")
                        return {}

                    text = await response.text()
                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Failed to parse JSON: {e}")
                        return {}

                    rates = await self._parse_rates(data)

                    # Обновляем кэш
                    self._cache = rates
                    self._cache_timestamp = datetime.now()

                    return rates
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error while fetching CBR rates: {e}")
            return self._cache or {}
        except Exception as e:
            self.logger.error(f"Unexpected error in CBR service: {e}")
            return self._cache or {}

    async def _parse_rates(self, data: dict) -> Dict[str, CurrencyRate]:
        """
        Парсит данные от API ЦБ РФ.

        Args:
            data: Сырые данные от API

        Returns:
            Dict[str, CurrencyRate]: Отпарсенные данные
        """
        rates = {}

        try:
            for currency_code in self.tracked_currencies:
                if currency_code in data.get("Valute", {}):
                    valute_data = data["Valute"][currency_code]
                    current_value = float(valute_data["Value"])
                    previous_value = float(valute_data["Previous"])
                    change = current_value - previous_value

                    # Рассчитываем процент изменения
                    if previous_value != 0:
                        change_percent = (change / previous_value) * 100
                    else:
                        change_percent = 0.0

                    rates[currency_code] = CurrencyRate(
                        currency=f"{currency_code}/RUB",
                        rate=current_value,
                        change=change,
                        change_percent=change_percent,
                        timestamp=datetime.now(),
                    )
            self.logger.info(f"Successfully parsed rates for {len(rates)} currencies")
            return rates
        except KeyError as e:
            self.logger.error(f"Missing expected key in CBR response: {e}")
            return {}
        except ValueError as e:
            self.logger.error(f"Error parsing numeric values: {e}")
            return {}

    async def get_specific_rate(self, currency: str) -> Optional[CurrencyRate]:
        """
        Получает курс конкретной валюты.

        Args:
            currency: Код валюты (USD, EUR, etc.)

        Returns:
            Optional[CurrencyRate]: Данные по валюте или None
        """
        rates = await self.get_rates()
        return rates.get(currency.upper())

    def get_cached_rates(self) -> Optional[Dict[str, CurrencyRate]]:
        """
        Возвращает закешированнаые данные (если есть).

        Returns:
            Optional[Dict[str, CurrencyRate]]: Кэшированные данные
        """
        return self._cache


cbr_service = CBRService()
