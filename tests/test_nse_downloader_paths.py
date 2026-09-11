from datetime import date
from pathlib import Path

from backend.ingestion.download.nse_downloader import (
    NSEFOSource,
    resolve_raw_zip_path,
)


def test_legacy_raw_zip_path() -> None:
    result = resolve_raw_zip_path(
        date(2024, 7, 5),
        Path("data/raw/nse/fo"),
    )

    assert result == Path("data/raw/nse/fo/legacy/2024/fo050724.zip")


def test_udiff_raw_zip_path() -> None:
    result = resolve_raw_zip_path(
        date(2025, 8, 20),
        Path("data/raw/nse/fo"),
    )

    assert result == Path(
        "data/raw/nse/fo/udiff/2025/" "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv.zip"
    )


def test_legacy_source_path_component() -> None:
    result = resolve_raw_zip_path(
        date(2024, 7, 5),
        Path("D:/OptionSense/raw"),
    )

    assert result.parts[-3:] == (
        NSEFOSource.LEGACY.value,
        "2024",
        "fo050724.zip",
    )


def test_udiff_source_path_component() -> None:
    result = resolve_raw_zip_path(
        date(2025, 8, 20),
        Path("D:/OptionSense/raw"),
    )

    assert result.parts[-3:] == (
        NSEFOSource.UDIFF.value,
        "2025",
        "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv.zip",
    )
