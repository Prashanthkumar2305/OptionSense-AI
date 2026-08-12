from datetime import date

from backend.database.models import Company, MarketPrice


def test_company_model() -> None:
    company = Company(
        symbol="RELIANCE",
        company_name="Reliance Industries",
        sector="Energy",
        exchange="NSE",
        is_active=True,
    )

    assert company.symbol == "RELIANCE"
    assert company.company_name == "Reliance Industries"
    assert company.sector == "Energy"
    assert company.exchange == "NSE"
    assert company.is_active is True


def test_market_price_model() -> None:
    market_price = MarketPrice(
        company_id=1,
        trade_date=date(2026, 8, 12),
        open_price=2500.0,
        high_price=2530.0,
        low_price=2485.0,
        close_price=2515.0,
        volume=1_500_000,
    )

    assert market_price.company_id == 1
    assert market_price.trade_date == date(2026, 8, 12)
    assert market_price.open_price == 2500.0
    assert market_price.high_price == 2530.0
    assert market_price.low_price == 2485.0
    assert market_price.close_price == 2515.0
    assert market_price.volume == 1_500_000
