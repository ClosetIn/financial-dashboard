from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from app.services.moex_service import MOEXService, StockData


class TestMOEXService:
    """Тесты для сервиса MOEX"""

    @pytest.fixture
    def moex_service(self):
        """Фикстура для создания экземпляра сервиса"""
        return MOEXService()

    @pytest.fixture
    def mock_moex_response(self):
        """Фикстура с мок данными от API MOEX"""
        return {
            "marketdata": {
                "columns": ["SECID", "LAST", "OPEN"],
                "data": [
                    ["SBER", 280.5, 279.0],
                    ["GAZP", 165.3, 166.0],
                    ["VTBR", 0.025, 0.024],
                ],
            }
        }

    def test_stock_data_model(self):
        """Тестирование модели StockData"""
        timestamp = datetime.now()
        stock_data = StockData(
            ticker="SBER",
            price=280.5,
            change_percent=1.5,
            volume=1000000.0,
            timestamp=timestamp,
        )

        assert stock_data.ticker == "SBER"
        assert stock_data.price == 280.5
        assert stock_data.change_percent == 1.5
        assert stock_data.volume == 1000000.0
        assert stock_data.timestamp == timestamp

    @pytest.mark.asyncio
    async def test_get_stock_prices_success(self, moex_service, mock_moex_response):
        """Тестирование успешного получения данных по акциям"""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json.return_value = mock_moex_response
            mock_get.return_value.__aenter__.return_value = mock_response

            stocks = await moex_service.get_stock_prices()

            assert isinstance(stocks, dict)
            assert "SBER" in stocks
            assert stocks["SBER"].ticker == "SBER"
            assert stocks["SBER"].price == 280.5
            # Проверяем расчёт процента изменения
            expected_change = ((280.5 - 279.0) / 279.0) * 100
            assert stocks["SBER"].change_percent == round(expected_change, 2)

    @pytest.mark.asyncio
    async def test_get_stock_prices_network_error(self, moex_service):
        """Тестирование обработки сетевой ошибки"""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.side_effect = Exception("Network error")

            stocks = await moex_service.get_stock_prices()
            assert stocks == {}

    @pytest.mark.asyncio
    async def test_get_specific_stock(self, moex_service, mock_moex_response):
        """Тестирование получения конкретной акции"""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json.return_value = mock_moex_response
            mock_get.return_value.__aenter__.return_value = mock_response

            stock = await moex_service.get_specific_stock("SBER")

            assert stock is not None
            assert stock.ticker == "SBER"
            assert stock.price == 280.5

    @pytest.mark.asyncio
    async def test_get_specific_stock_not_found(self, moex_service, mock_moex_response):
        """Тестирование случая, когда акция не найдена"""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json.return_value = mock_moex_response
            mock_get.return_value.__aenter__.return_value = mock_response

            stock = await moex_service.get_specific_stock("UNKNOWN")

            assert stock is None

    def test_supported_tickers(self, moex_service):
        """Тестирование списка поддерживаемых тикеров"""
        expected_tickers = ["SBER", "GAZP", "VTBR", "YNDX", "ROSN", "LKOH", "MGNT"]
        assert moex_service.get_supported_tickers() == expected_tickers
