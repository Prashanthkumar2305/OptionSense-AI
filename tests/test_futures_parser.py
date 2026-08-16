from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from backend.ingestion.legacy.futures_parser import parse_legacy_futures

fixture_dir = (
    Path(__file__).resolve().parents[1]
    / "tests"
    / "fixtures"
    / "nse"
    / "fo"
    / "legacy"
)


def test_parse_legacy_futures_05_july() -> None:
    path = fixture_dir / "fo050724.csv"

    result = parse_legacy_futures(
        path,
        date(2024, 7, 5),
    )

    assert len(result) == 5
    assert result["trade_date"].iloc[0] == pd.Timestamp("2024-07-05")
    assert result["contract"].notna().all()
    assert "open_interest" in result.columns
    assert "volume" in result.columns


def test_parse_legacy_futures_04_july() -> None:
    path = fixture_dir / "fo040724.csv"

    result = parse_legacy_futures(
        path,
        date(2024, 7, 4),
    )

    assert len(result) == 5
    assert result["trade_date"].iloc[0] == pd.Timestamp("2024-07-04")


def test_missing_column_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("CONTRACT_D,OPEN_PRICE\nTEST,100\n")

    with pytest.raises(ValueError, match="Missing required futures columns"):
        parse_legacy_futures(path, date(2024, 7, 5))
