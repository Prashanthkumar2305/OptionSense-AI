from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

column_map = {
    "CONTRACT_D": "contract",
    "PREVIOUS_S": "previous_close",
    "OPEN_PRICE": "open",
    "HIGH_PRICE": "high",
    "LOW_PRICE": "low",
    "CLOSE_PRIC": "close",
    "SETTLEMENT": "settlement",
    "NET_CHANGE": "net_change",
    "OI_NO_CON": "open_interest",
    "TRADED_QUA": "volume",
    "TRD_NO_CON": "trade_count",
    "TRADED_VAL": "traded_value",
}


def parse_legacy_futures(
    path: str | Path,
    trade_date: date,
) -> pd.DataFrame:
    """Parse one NSE legacy F&O futures CSV."""

    df = pd.read_csv(path)

    missing = set(column_map) - set(df.columns)

    if missing:
        raise ValueError(f"Missing required futures columns: {sorted(missing)}")

    df = df.rename(columns=column_map).copy()

    df["trade_date"] = pd.Timestamp(trade_date)

    df["contract"] = df["contract"].astype("string").str.strip()

    numeric_columns = [
        "previous_close",
        "open",
        "high",
        "low",
        "close",
        "settlement",
        "net_change",
        "open_interest",
        "volume",
        "trade_count",
        "traded_value",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df[
        [
            "trade_date",
            "contract",
            "previous_close",
            "open",
            "high",
            "low",
            "close",
            "settlement",
            "net_change",
            "open_interest",
            "volume",
            "trade_count",
            "traded_value",
        ]
    ]
