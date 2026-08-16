from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OptionContract:
    underylying: str
    expiry_date: datetime
    option_type: str
    strike_price: float


_option_pattern = re.compile(
    r"^OPT(?:STK|IDX)(?P<underlying>.+?)"
    r"(?P<expiry>\d{2}-[A-Z]{3}-\d{4})"
    r"(?P<option_type>CE|PE)"
    r"(?P<strike>\d+(?:\.\d+)?)$"
)


def parse_pattern_contract(contract: str) -> OptionContract:
    """Parse an NSE legacy option contract identifier."""

    match = _option_pattern.match(contract.strip().upper())

    if match is None:
        raise ValueError(f"Invalid option contract:{contract!r}")

    return OptionContract(
        underylying=match.group("underlying"),
        expiry_date=datetime.strptime(
            match.group("expiry"),
            "%d-%b-%Y",
        ),
        option_type=match.group("option_type"),
        strike_price=float(match.group("strike")),
    )
