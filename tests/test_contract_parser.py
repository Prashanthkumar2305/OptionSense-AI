from datetime import datetime

import pytest

from backend.ingestion.legacy.contract_parser import parse_pattern_contract


def test_parse_stock_call() -> None:
    result = parse_pattern_contract("OPTSTKDLF25-JUL-2024CE890")

    assert result.underlying == "DLF"
    assert result.expiry_date == datetime(2024, 7, 25)
    assert result.option_type == "CE"
    assert result.strike_price == pytest.approx(890.0)


def test_parse_stock_decimal_strike() -> None:
    result = parse_pattern_contract("OPTSTKNATIONALUM25-JUL-2024CE197.5")

    assert result.underlying == "NATIONALUM"
    assert result.expiry_date == datetime(2024, 7, 25)
    assert result.option_type == "CE"
    assert result.strike_price == pytest.approx(197.5)


def test_parse_index_put() -> None:
    result = parse_pattern_contract("OPTIDXNIFTYNXT5026-JUL-2024PE67200")

    assert result.underlying == "NIFTYNXT50"
    assert result.expiry_date == datetime(2024, 7, 26)
    assert result.option_type == "PE"
    assert result.strike_price == pytest.approx(67200.0)


def test_invalid_contract_raises() -> None:
    with pytest.raises(ValueError):
        parse_pattern_contract("INVALID_CONTRACT")
