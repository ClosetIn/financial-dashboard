from datetime import datetime

from sqlalchemy import DateTime, Float, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""

    pass


class ExchangeRate(Base):
    """Модель для хранения курсов валют"""

    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    currency_pair: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True
    )  # USD/RUB, EUR/RUB
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    change: Mapped[float] = mapped_column(Float, default=0.0)
    change_percent: Mapped[float] = mapped_column(Float, default=0.0)
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="cbr"
    )  # cbr, moex, binance
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    # Индексы для оптимизации запросов
    __table_args__ = (
        Index("ix_exchange_rates_currency_timestamp", "currency_pair", "timestamp"),
        Index("ix_exchange_rates_source_timestamp", "source", "timestamp"),
    )


class StockPrice(Base):
    """Модель для хранения цен акций"""

    __tablename__ = "stock_prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(
        String, primary_key=True, index=True
    )  # SBER, GAZP, VTBR
    price: Mapped[float] = mapped_column(Float, nullable=False)
    change_percent: Mapped[float] = mapped_column(Float, default=0.0)
    volume: Mapped[float] = mapped_column(Float, default=0.0)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="moex")
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    # Индексы для оптимизации запросов
    __table_args__ = (
        Index("ix_stock_prices_ticker_timestamp", "ticker", "timestamp"),
        Index("ix_stock_prices_sources_timestamp", "source", "timestamp"),
    )


class CryptoPrice(Base):
    """Модель для хранения цен криптовалют"""

    __tablename__ = "crypto_prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(
        String(10), nullable=False, index=True
    )  # BTCRUB, ETHRUB
    price: Mapped[float] = mapped_column(Float, nullable=False)
    change_percent: Mapped[float] = mapped_column(Float, default=0.0)
    volume: Mapped[float] = mapped_column(Float, default=0.0)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="binance")
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    # Индексы для оптимизации запросов
    __table_args__ = (
        Index("ix_crypto_prices_symbol_timestamp", "symbol", "timestamp"),
        Index("ix_crypto_prices_source_timestamp", "source", "timestamp"),
    )
