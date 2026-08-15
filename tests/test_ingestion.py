from datetime import datetime

import pytest

from backend.ingestion.base import DataSource
from backend.ingestion.exceptions import (
    DataSourceError,
    DataValidationError,
    IngestionError,
)
from backend.ingestion.models import OHLCVRecord


def test_ohlcv_record() -> None:
    record = OHLCVRecord(
        timestamp=datetime(2026, 8, 10, 10, 0),
        symbol="RELIANCE",
        open=1_500.0,
        high=1_520.0,
        low=1_490.0,
        close=1_510.0,
        volume=100_000,
    )

    assert record.symbol == "RELIANCE"
    assert record.close == 1_510.0
    assert record.volume == 100_000


def test_ingestion_exception_hierarchy() -> None:
    assert issubclass(DataValidationError, IngestionError)
    assert issubclass(DataSourceError, IngestionError)


def test_data_source_is_abstract() -> None:
    with pytest.raises(TypeError):
        DataSource()  # type: ignore[abstract]
