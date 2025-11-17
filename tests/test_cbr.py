import json
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from app.services.cbr_service import CBRService, CurrencyRate


class TestCBRService:
    """Тесты для сервиса ЦБ РФ"""

    @pytest.fixture
    def cbr_service(self):
        """Фикстура для создания экземпляра сервиса"""
        return CBRService()

    @pytest.fixture
    def mock_cbr_response(self):
        """Фикстура с мок данными от API ЦБ РФ."""
        return {
            "Valute": {
                "USD": {
                    "CharCode": "USD",
                    "Name": "Доллар США",
                    "Value": 91.5,
                    "Previous": 91.3,
                },
                "EUR": {
                    "CharCode": "EUR",
                    "Name": "Евро",
                    "Value": 99.8,
                    "Previous": 99.5,
                },
            }
        }

    def test_currency_rate_model(self):
        """Тестирование модели CurrencyRate"""
        timestamp = datetime.now()
        rate = CurrencyRate(
            currency="USD/RUB",
            rate=91.5,
            change=0.2,
            change_percent=0.22,
            timestamp=timestamp,
        )

        assert rate.currency == "USD/RUB"
        assert rate.rate == 91.5
        assert rate.change == 0.2
        assert rate.change_percent == 0.22
        assert rate.timestamp == timestamp

    @pytest.mark.asyncio
    async def test_get_rates_success(self, cbr_service, mock_cbr_response):
        """Тестирование успешного получения курсов."""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text.return_value = json.dumps(mock_cbr_response)
            mock_get.return_value.__aenter__.return_value = mock_response

            rates = await cbr_service.get_rates()

            assert isinstance(rates, dict)
            assert "USD" in rates
            assert "EUR" in rates
            assert rates["USD"].currency == "USD/RUB"
            assert rates["USD"].rate == 91.5
            assert rates["USD"].change == 0.2

    @pytest.mark.asyncio
    async def test_get_rates_network_error(self, cbr_service):
        """Тестирование обработки сетевой ошибки"""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.side_effect = Exception("Network error")
            # Должен вернуть пустой словарь при ошибке
            rates = await cbr_service.get_rates()
            assert rates == {}

    @pytest.mark.asyncio
    async def test_get_rates_invalid_response(self, cbr_service):
        """Тестирование обработки навалидного ответа."""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 500
            mock_get.return_value.__aenter__.return_value = mock_response

            rates = await cbr_service.get_rates()
            assert rates == {}

    @pytest.mark.asyncio
    async def test_get_specific_rate(self, cbr_service, mock_cbr_response):
        """Тестирование получения конкретной валюты."""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text.return_value = json.dumps(mock_cbr_response)
            mock_get.return_value.__aenter__.return_value = mock_response

            rate = await cbr_service.get_specific_rate("USD")

            assert rate is not None
            assert rate.currency == "USD/RUB"
            assert rate.rate == 91.5

    @pytest.mark.asyncio
    async def test_get_specific_rate_not_found(self, cbr_service, mock_cbr_response):
        """Тестирование случая, когда валюта не найдена."""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text.return_value = json.dumps(mock_cbr_response)
            mock_get.return_value.__aenter__.return_value = mock_response

            rate = await cbr_service.get_specific_rate("XYZ")  # Несуществующая валюта
            assert rate is None

    def test_tracked_currencies(self, cbr_service):
        """Тестирование списка отслеживаемых валют"""
        expected_currencies = ["USD", "EUR", "CNY", "GBP", "JPY"]
        assert cbr_service.tracked_currencies == expected_currencies


class TestCurrencyRateValidation:
    """Тесты валидации данных валют"""

    def test_negative_values_are_allowed(self):
        """Тестирование, что отрицательные значения допускаются с warning."""
        rate = CurrencyRate(
            currency="TEST/RUB",
            rate=-1.0,
            change=-0.5,
            change_percent=-0.55,
            timestamp=datetime.now(),
        )

        # Значения должны быть округлены, но не изменены
        assert rate.rate == -1.0
        assert rate.change == -0.5
        assert rate.change_percent == -0.55
