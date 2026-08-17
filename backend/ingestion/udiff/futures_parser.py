from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

required_columns = {
    "TradDt",
    "BizDt",
    "FinInstrmTp",
    "TckrSymb",
    "XpryDt",
    "FinInstrmNm",
    "OpnPric",
    "HghPric",
    "LwPric",
    "ClsPric",
    "LastPric",
    "PrvsClsgPric",
    "UndrlygPric",
    "SttlmPric",
    "OpnIntrst",
    "ChngInOpnIntrst",
    "TtlTradgVol",
    "TtlTrfVal",
    "TtlNbOfTxsExctd",
}


def parse_udiff_futures(
    path: str | Path,
    trade_date: datetime,
) -> pd.DataFrame:
    """Parse an NSE UDiff common Bhavcopy futures file."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"UDiff futures file not found:{path}")

    df = pd.read_csv(path, low_memory=False)

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"missing required UDiff futures columns:{sorted(missing)}")

    # keep only futures instruments.
    df = df[df["FinInstrmTp"].isin(["STF", "IDF"])].copy()

    result = pd.DataFrame(
        {
            "trade_date": trade_date,
            "contract": df["FinInstrmNm"],
            "underlying": df["TckrSymb"],
            "expiry_date": pd.to_datetime(df["XpryDt"]),
            "previous_close": df["PrvsClsgPric"],
            "open": df["OpnPric"],
            "high": df["HghPric"],
            "low": df["LwPric"],
            "close": df["ClsPric"],
            "last_price": df["LastPric"],
            "underlying_price": df["UndrlygPric"],
            "settlement": df["SttlmPric"],
            "open_interest": df["OpnIntrst"],
            "change_in_open_interest": df["ChngInOpnIntrst"],
            "volume": df["TtlTradgVol"],
            "turnover": df["TtlTrfVal"],
            "trade_count": df["TtlNbOfTxsExctd"],
            "instrument_type": df["FinInstrmTp"],
        }
    )

    result["trade_date"] = pd.to_datetime(result["trade_date"])

    return result.reset_index(drop=True)
