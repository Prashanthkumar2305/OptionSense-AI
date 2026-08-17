from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from backend.ingestion.legacy.contract_parser import parse_pattern_contract

required_options_columns = {
    "CONTRACT_D",
    "PREVIOUS_S",
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRIC",
    "SETTLEMENT",
    "NET_CHANGE",
    "OI_NO_CON",
    "TRADED_QUA",
    "TRD_NO_CON",
    "UNDRLNG_ST",
    "NOTIONAL_V",
    "PREMIUM_TR",
}


def parse_legacy_options(
    path: Path,
    trade_date: datetime,
) -> pd.DataFrame:
    """Parse a legacy NSE options bhavcopy CSV."""

    df = pd.read_csv(path)

    missing = required_options_columns - set(df.columns)

    if missing:
        raise ValueError(f"missing required options columns:{sorted(missing)}")

    contracts = df["CONTRACT_D"].map(parse_pattern_contract)

    result = pd.DataFrame(
        {
            "trade_date": trade_date,
            "contract": df["CONTRACT_D"],
            "underlying": [contract.underlying for contract in contracts],
            "expiry_date": [contract.expiry_date for contract in contracts],
            "option_type": [contract.option_type for contract in contracts],
            "strike_price": [contract.strike_price for contract in contracts],
            "previous_close": df["PREVIOUS_S"],
            "open": df["OPEN_PRICE"],
            "high": df["HIGH_PRICE"],
            "low": df["LOW_PRICE"],
            "close": df["CLOSE_PRIC"],
            "settlement": df["SETTLEMENT"],
            "net_change": df["NET_CHANGE"],
            "open_interest": df["OI_NO_CON"],
            "volume": df["TRADED_QUA"],
            "trade_count": df["TRD_NO_CON"],
            "underlying_price": df["UNDRLNG_ST"],
            "notional_value": df["NOTIONAL_V"],
            "premium_turnover": df["PREMIUM_TR"],
        }
    )

    return result
