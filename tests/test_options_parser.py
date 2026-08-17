from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from backend.ingestion.legacy.options_parser import parse_legacy_options

fixture_dir = (
    Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "nse" / "fo" / "legacy"
)


def test_parse_legacy_options_05_july() -> None:
    path = fixture_dir / "op050724.csv"

    result = parse_legacy_options(path, datetime(2024, 7, 5))

    assert len(result) == 10
    assert result["trade_date"].iloc[0] == pd.Timestamp("2024-07-05")
    assert result["underlying"].notna().all()
    assert result["expiry_date"].notna().all()
    assert result["option_type"].isin(["CE", "PE"]).all()
    assert result["strike_price"].notna().all()
    assert "open_interest" in result.columns
    assert "volume" in result.columns
    assert "underlying_price" in result.columns


def test_missing_column_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("CONTRACT_D,OPEN_PRICE\nTEST,100\n")

    with pytest.raises(
        ValueError,
        match="missing required options columns",
    ):

        parse_legacy_options(path, datetime(2024, 7, 5))
