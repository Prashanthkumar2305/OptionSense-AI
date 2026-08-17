from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from backend.ingestion.udiff.futures_parser import parse_udiff_futures

fixture_dir = Path(__file__).parent / "fixtures" / "nse" / "fo" / "udiff"


def test_parse_udiff_futures() -> None:
    path = fixture_dir / "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"

    result = parse_udiff_futures(
        path,
        datetime(2025, 8, 20),
    )

    assert len(result) == 646

    assert result["trade_date"].iloc[0] == pd.Timestamp("2025-08-20")

    assert {
        "STF",
        "IDF",
    }.issubset(set(result["instrument_type"]))


def test_udiff_futures_values() -> None:
    path = fixture_dir / "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"

    result = parse_udiff_futures(
        path,
        datetime(2025, 8, 20),
    )

    abcapital = result[result["contract"] == "ABCAPITAL25AUGFUT"].iloc[0]

    assert abcapital["underlying"] == "ABCAPITAL"
    assert abcapital["expiry_date"] == pd.Timestamp("2025-08-28")
    assert abcapital["open"] == pytest.approx(288.10)
    assert abcapital["high"] == pytest.approx(288.10)
    assert abcapital["low"] == pytest.approx(283.70)
    assert abcapital["close"] == pytest.approx(284.15)
    assert abcapital["previous_close"] == pytest.approx(288.25)
    assert abcapital["underlying_price"] == pytest.approx(283.45)


def test_missing_column_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"

    path.write_text("TradDt,FinInstrmTp,TckrSymb\n" "2025-08-20,STF,TEST\n")

    with pytest.raises(
        ValueError,
        match="missing required UDiff futures columns",
    ):
        parse_udiff_futures(
            path,
            datetime(2025, 8, 20),
        )
