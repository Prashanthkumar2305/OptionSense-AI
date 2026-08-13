from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
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


class OptionContract(Base):
    """Represents an individual equity option contract."""

    __tablename__ = "option_contracts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
    )

    underlying_symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    expiry_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    strike_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    option_type: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    contract_symbol: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        CheckConstraint(
            "option_type IN('CE','PE')",
            name="ck_option_contract_type",
        ),
        Index(
            "ix_option_contracts_company_id",
            "company_id",
        ),
        Index(
            "ix_option_contracts_expiry_date",
            "expiry_date",
        ),
        Index(
            "ix_option_contracts_company_expiry",
            "company_id",
            "expiry_date",
        ),
        Index(
            "ix_option_contracts_company_expiry_strike_type",
            "company_id",
            "expiry_date",
            "strike_price",
            "option_type",
        ),
    )


class OptionChainSnapshot(Base):
    """Represents market data for an option contract at a point in time."""

    __tablename__ = "option_chain_snapshots"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    contract_id: Mapped[int] = mapped_column(
        ForeignKey("option_contracts.id"),
        nullable=False,
    )

    snapshot_timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    underlying_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    last_price: Mapped[float] = mapped_column(
        Numeric(15, 4),
        nullable=False,
    )

    bid_price: Mapped[float | None] = mapped_column(
        Numeric(15, 4),
        nullable=True,
    )

    ask_price: Mapped[float | None] = mapped_column(
        Numeric(15, 4),
        nullable=True,
    )

    volume: Mapped[int] = mapped_column(
        nullable=False,
    )

    open_interest: Mapped[int] = mapped_column(
        nullable=False,
    )

    oi_change: Mapped[int] = mapped_column(
        nullable=False,
    )

    implied_volatility: Mapped[float | None] = mapped_column(
        Numeric(10, 6),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        Index(
            "ix_option_snapshots_contract_id",
            "contract_id",
        ),
        Index(
            "ix_option_snapshots_timestamp",
            "snapshot_timestamp",
        ),
        Index(
            "ix_option_snapshots_contract_timestamp",
            "contract_id",
            "snapshot_timestamp",
        ),
    )
