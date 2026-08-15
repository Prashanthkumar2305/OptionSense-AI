from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OHLCVRecord:
    """Normalized OHLCV market -data record ."""

    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
