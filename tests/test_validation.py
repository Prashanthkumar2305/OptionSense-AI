from datetime import datetime

import pytest

from backend.ingestion.exceptions import DataValidationError
from backend.ingestion.models import OHLCVRecord
from backend.ingestion.validation import validate_ohlcv


def make_valid_record() -> OHLCVRecord:
    return OHLCVRecord(
        timestamp=datetime(2026, 8, 15, 10, 0),
        symbol="RELIANCE",
        open=1500.0,
        high=1520.0,
        low=1490.0,
        close=1510.0,
        volume=100_000,
    )


def test_valid_ohlcv_record() -> None:
    record = make_valid_record()

    validate_ohlcv(record)


@pytest.mark.parametrize(
    "field,value",
    [
        ("open", 0),
        ("open", -1),
        ("high", 0),
        ("high", -1),
        ("low", 0),
        ("low", -1),
        ("close", 0),
        ("close", -1),
    ],
)
def test_prices_must_be_positive(
    field: str,
    value: float,
) -> None:

    record = make_valid_record()
    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol=record.symbol,
        open=value if field == "open" else record.open,
        high=value if field == "high" else record.high,
        low=value if field == "low" else record.low,
        close=value if field == "close" else record.close,
        volume=record.volume,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)


def test_negative_volume_is_rejected() -> None:
    record = make_valid_record()

    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol=record.symbol,
        open=record.open,
        high=record.high,
        low=record.low,
        close=record.close,
        volume=-1,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)


def test_empty_symbol_is_rejected() -> None:
    record = make_valid_record()

    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol="  ",
        open=record.high,
        close=record.close,
        high=record.high,
        low=record.low,
        volume=record.volume,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)


def test_high_below_open_is_rejected() -> None:
    record = make_valid_record()

    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol=record.symbol,
        open=1500,
        high=1499,
        low=1480,
        close=1485,
        volume=record.volume,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)


def test_high_below_close_is_rejected() -> None:
    record = make_valid_record()

    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol=record.symbol,
        open=1500,
        high=1505,
        low=1490,
        close=1510,
        volume=record.volume,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)


def test_low_above_open_is_rejected() -> None:
    record = make_valid_record()

    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol=record.symbol,
        open=1500,
        high=1520,
        low=1510,
        close=1515,
        volume=record.volume,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)


def test_low_above_close_is_rejected() -> None:
    record = make_valid_record()

    record = OHLCVRecord(
        timestamp=record.timestamp,
        symbol=record.symbol,
        open=1500,
        high=1520,
        low=1515,
        close=1510,
        volume=record.volume,
    )

    with pytest.raises(DataValidationError):
        validate_ohlcv(record)
