from datetime import date

from backend.ingestion.download.nse_downloader import (
    UDIFF_START_DATE,
    NSEFOSource,
    resolve_file_spec,
)


def test_legacy_file_spec() -> None:
    result = resolve_file_spec(date(2024, 7, 5))

    assert result.source == NSEFOSource.LEGACY
    assert result.zip_name == "fo050724.zip"
    assert result.csv_name == "fo050724.csv"


def test_udiff_transition_day() -> None:
    result = resolve_file_spec(UDIFF_START_DATE)

    assert result.source == NSEFOSource.UDIFF
    assert result.zip_name == "BhavCopy_NSE_FO_0_0_0_20240708_F_0000.csv.zip"
    assert result.csv_name == "BhavCopy_NSE_FO_0_0_0_20240708_F_0000.csv"


def test_udiff_file_spec_2025() -> None:
    result = resolve_file_spec(date(2025, 8, 20))

    assert result.source == NSEFOSource.UDIFF
    assert result.zip_name == "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv.zip"
    assert result.csv_name == "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"


def test_year_2026_file_spec() -> None:
    result = resolve_file_spec(date(2026, 9, 11))

    assert result.source == NSEFOSource.UDIFF
    assert result.zip_name == "BhavCopy_NSE_FO_0_0_0_20260911_F_0000.csv.zip"
    assert result.csv_name == "BhavCopy_NSE_FO_0_0_0_20260911_F_0000.csv"
