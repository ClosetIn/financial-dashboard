import logging
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
from aiohttp import ClientTimeout
from pydantic import BaseModel, Field

# Настраиваем логирование
logger = logging.getLogger(__name__)


class StockData(BaseModel):
    """Модель для хранения данных об акции"""

    ticker: str
    price: float = Field(ge=0)
    change_percent: float
    volume: float = Field(ge=0)
    timestamp: datetime


class MOEXService:
    """Сервис для работы с API Московской биржи"""

    def __init__(self) -> None:
        self.base_url = "https://iss.moex.com/iss"
        self.popular_tickers = ["SBER", "GAZP", "VTBR", "YNDX", "ROSN", "LKOH", "MGNT"]
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)
        self.timeout = ClientTimeout(total=10)

    async def get_stock_prices(self) -> Dict[str, StockData]:
        """
        Получает актуальные котировки акций с Московской биржи.

        Returns:
            Dict[str, StockData]: Словарь с данными по акциям
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Получаем данные по акциям
                stocks_data = await self._fetch_stocks_data(session)
                return stocks_data
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error while fetching MOEX data: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error in MOEX service: {e}")
            return {}

    async def _fetch_stocks_data(
        self, session: aiohttp.ClientSession
    ) -> Dict[str, StockData]:
        """Получает и парсит данные по акциям"""
        try:
            url = f"{self.base_url}/engines/stock/markets/shares/boards/TQBR/securities.json"
            params = {
                "securities.columns": "SECID,SHORTNAME",
                "marketdata.columns": "SECID,LAST,OPEN",
            }

            self.logger.info(f"Feching MOEX data from: {url}")

            async with session.get(
                url, params=params, timeout=self.timeout
            ) as response:
                if response.status != 200:
                    self.logger.error(f"MOEX API returned status {response.status}")
                    return {}

                data = await response.json()

                # Логируем структуру ответа для отладки
                self.logger.info(f"MOEX response keys: {list(data.keys())}")
                if "marketdata" in data:
                    marketdata = data["marketdata"]
                    self.logger.info(
                        f"Marketdata columns: {marketdata.get('columns', [])}"
                    )
                    self.logger.info(
                        f"Marketdata entries: {len(marketdata.get('data', []))}"
                    )

                return await self._parse_stocks_response(data)
        except Exception as e:
            self.logger.error(f"Error fetching stocks data: {e}")
            return {}

    async def _parse_stocks_response(self, data: dict) -> Dict[str, StockData]:
        """Парсит ответ от MOEX API"""
        stocks = {}

        try:

            # Парсинг структуры MOEX
            marketdata = data.get("marketdata", {})
            columns = marketdata.get("columns", [])
            market_data_list = marketdata.get("data", [])

            # Находим индексы нужных колонок
            try:
                secid_idx = columns.index("SECID")
                last_idx = columns.index("LAST")
                open_idx = columns.index("OPEN")
            except ValueError as e:
                self.logger.error(f"Required column not found in MOEX response: {e}")
                self.logger.info(f"Available columns: {columns}")
                return {}

            # Обрабатываем данные
            processed_count = 0
            for item in market_data_list:
                try:
                    if len(item) > max(secid_idx, last_idx, open_idx):
                        ticker = item[secid_idx]
                        last_price = item[last_idx]
                        open_price = item[open_idx]

                        # Фильтруем только популярные тикеры
                        if (
                            ticker in self.popular_tickers
                            and last_price is not None
                            and open_price is not None
                            and last_price > 0
                        ):

                            # Рассчитываем процент изменения
                            change_percent = 0.0
                            if open_price > 0:
                                change_percent = (
                                    (last_price - open_price) / open_price
                                ) * 100

                            stocks[ticker] = StockData(
                                ticker=ticker,
                                price=float(last_price),
                                change_percent=round(change_percent, 2),
                                volume=0.0,  # MOEX требует отдельный запрос для объёма
                                timestamp=datetime.now(),
                            )
                            processed_count += 1
                except Exception as e:
                    self.logger.warning(f"Error processing item {item}: {e}")
                    continue

            self.logger.info(
                f"Successfully parsed data for {processed_count} stocks: {list(stocks.keys())}"
            )
            return stocks
        except KeyError as e:
            self.logger.error(f"Missing expected key in MOEX response: {e}")
            return {}
        except ValueError as e:
            self.logger.error(f"Error parsing numeric values: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error in parsing: {e}")
            return {}

    async def get_specific_stock(self, ticker: str) -> Optional[StockData]:
        """
        Получает данные по конкретной акции

        Args:
            ticker: Тикер акции (SBER, GAZP, etc.)

        Returns:
            Optional[StockData]: Данные по акции или None
        """
        stocks = await self.get_stock_prices()
        return stocks.get(ticker.upper())

    def get_supported_tickers(self) -> List[str]:
        """
        Возвращает список поддерживаемых тикеров.

        Returns:
            List[str]: Список тикеров
        """
        return self.popular_tickers.copy()


# Создаём глобальный экземпляр сервиса
moex_service = MOEXService()
