from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from backend.ingestion.udiff.options_parser import parse_udiff_options

fixture_dir = Path(__file__).resolve().parent / "fixtures" / "nse" / "fo" / "udiff"


def test_parse_udiff_options() -> None:
    path = fixture_dir / "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"

    result = parse_udiff_options(
        path,
        datetime(2025, 8, 20),
    )

    assert len(result) == 32049
    assert result["trade_date"].iloc[0] == pd.Timestamp("2025-08-20")
    assert result["contract"].notna().all()
    assert result["underlying"].notna().all()
    assert result["expiry_date"].notna().all()
    assert result["option_type"].isin(["CE", "PE"]).all()
    assert result["strike_price"].notna().all()
    assert result["underlying_price"].notna().all()
    assert "open_interest" in result.columns
    assert "volume" in result.columns
    assert "trade_count" in result.columns
    assert "notional_value" in result.columns
    assert "change_in_open_interest" in result.columns
    assert set(result["option_type"].unique()) == {"CE", "PE"}


def test_udiff_options_instrument_types() -> None:
    path = fixture_dir / "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"

    result = parse_udiff_options(
        path,
        datetime(2025, 8, 20),
    )

    assert len(result) > 0
    assert (
        result["contract"]
        .str.startswith(
            ("NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"),
            na=False,
        )
        .any()
    )


def test_missing_column_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"

    path.write_text("TradDt,FinInstrmTp,TckrsSymb\n" "2025-08-20,STO,NIFTY\n")

    with pytest.raises(
        ValueError,
        match="missing required UDiff options columns",
    ):

        parse_udiff_options(
            path,
            datetime(2025, 8, 20),
        )
