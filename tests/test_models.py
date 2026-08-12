from backend.database.models import Company


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
