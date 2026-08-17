from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

required_columns = {
    "TradDt",
    "FinInstrmTp",
    "FinInstrmId",
    "TckrSymb",
    "XpryDt",
    "StrkPric",
    "OptnTp",
    "FinInstrmNm",
    "OpnPric",
    "HghPric",
    "LwPric",
    "ClsPric",
    "PrvsClsgPric",
    "UndrlygPric",
    "OpnIntrst",
    "ChngInOpnIntrst",
    "TtlTradgVol",
    "TtlTrfVal",
    "TtlNbOfTxsExctd",
}

option_instrument_types = {"STO", "IDO"}


def parse_udiff_options(
    path: str | Path,
    trade_date: datetime,
) -> pd.DataFrame:
    """Parse an NSE UDiff Common Bhavcopy file into normalized options data."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"UDiff file not found:{path}")

    df = pd.read_csv(path, low_memory=False)

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"missing required UDiff options columns:{sorted(missing)}")

    # keep only index and stock options.

    df = df[df["FinInstrmTp"].isin(option_instrument_types)].copy()

    # keep only CE / PE options.

    df = df[df["OptnTp"].isin(["CE", "PE"])].copy()

    result = pd.DataFrame(
        {
            "trade_date": pd.Timestamp(trade_date),
            "contract": df["FinInstrmNm"].astype("string"),
            "underlying": df["TckrSymb"].astype("string"),
            "expiry_date": pd.to_datetime(df["XpryDt"], errors="coerce"),
            "option_type": df["OptnTp"].astype("string"),
            "strike_price": pd.to_numeric(
                df["StrkPric"],
                errors="coerce",
            ),
            "previous_close": pd.to_numeric(
                df["PrvsClsgPric"],
                errors="coerce",
            ),
            "open": pd.to_numeric(df["OpnPric"], errors="coerce"),
            "high": pd.to_numeric(df["HghPric"], errors="coerce"),
            "low": pd.to_numeric(df["LwPric"], errors="coerce"),
            "close": pd.to_numeric(df["ClsPric"], errors="coerce"),
            "settlement": pd.to_numeric(
                df["SttlmPric"],
                errors="coerce",
            ),
            "open_interest": pd.to_numeric(df["OpnIntrst"], errors="coerce"),
            "volume": pd.to_numeric(
                df["TtlTradgVol"],
                errors="coerce",
            ),
            "trade_count": pd.to_numeric(
                df["TtlTradgVol"],
                errors="coerce",
            ),
            "underlying_price": pd.to_numeric(
                df["UndrlygPric"],
                errors="coerce",
            ),
            "notional_value": pd.to_numeric(
                df["TtlTrfVal"],
                errors="coerce",
            ),
            "change_in_open_interest": pd.to_numeric(
                df["ChngInOpnIntrst"],
                errors="coerce",
            ),
        }
    )

    # UDiff does not provide a direct legacy NET_CHANGE field.
    # The legacy value corresponds to current close minus previous close.
    result["net_change"] = result["close"] - result["previous_close"]

    # UDiff doesn't expose a direct equivalent of legacy PREMIUM_TR.
    # keep the column so the normalized schema remains compatible.
    result["premium_turnover"] = pd.NA

    result["trade_date"] = pd.to_datetime(result["trade_date"]).dt.normalize()

    result["expiry_date"] = pd.to_datetime(
        result["expiry_date"],
        errors="coerce",
    ).dt.normalize()

    return result.reset_index(drop=True)
