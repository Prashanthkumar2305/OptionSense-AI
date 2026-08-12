from datetime import datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models"""


class Company(Base):
    """represents a stock/company in our trading universe"""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(150), nullable=False)
    sector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    exchange: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="NSE",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


class MarketPrice(Base):
    """Represents daily OHLCV market data for a company."""

    __tablename__ = "market_prices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    trade_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    open_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    high_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    low_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    close_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    volume: Mapped[int] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        Index(
            "ix_market_prices_company_id",
            "company_id",
        ),
        Index(
            "ix_market_prices_trade_date",
            "trade_date",
        ),
        Index(
            "ix_market_prices_company_date",
            "company_id",
            "trade_date",
        ),
    )
