from dataclasses import dataclass


@dataclass(frozen=True)
class IVHVFeatures:
    """Features comparing implied and historical volatility."""

    iv_minus_hv: float
    iv_hv_ratio: float
    iv_premium_pct: float


def calculate_iv_hv_features(
    implied_volatility: float,
    historical_volatility: float,
) -> IVHVFeatures:
    """Calculate featurtes comparing IV with historical volatility.

    Both volatility inputs must be supplied as decimals.

    Example:
    0.30 = 30% volatility
    0.20 = 20% volatility
    """

    if implied_volatility < 0:
        raise ValueError("implied_volatility cannot be negative.")

    if historical_volatility <= 0:
        raise ValueError("Historical_volatility must be greater than zero.")

    iv_minus_hv = implied_volatility - historical_volatility

    iv_hv_ratio = implied_volatility / historical_volatility

    iv_premium_pct = (
        (implied_volatility - historical_volatility) / historical_volatility * 100
    )

    return IVHVFeatures(
        iv_minus_hv=iv_minus_hv,
        iv_hv_ratio=iv_hv_ratio,
        iv_premium_pct=iv_premium_pct,
    )
