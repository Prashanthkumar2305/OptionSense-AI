from math import sqrt

import numpy as np
import pandas as pd

trading_days_per_year = 252


def calculate_log_returns(prices: pd.Series) -> pd.Series:
    """calculate continuously compounded returns from closing prices."""

    if prices.empty:
        raise ValueError("prices must not be empty.")

    if (prices <= 0).any():
        raise ValueError("Prices must contain only positve values.")

    return pd.Series(
        np.log(prices / prices.shift(1)),
        index=prices.index,
        dtype=float,
    )


def calculate_historical_volatality(
    prices: pd.Series,
    window: int = 20,
) -> float:
    """Calculate annualized historical volatility."""

    if window < 2:
        raise ValueError("Window must be at least 2.")

    if len(prices) < window + 1:
        raise ValueError("Prices must contain at least window + 1 observations.")

    returns = calculate_log_returns(prices).dropna()

    return float(returns.tail(window).std(ddof=1) * sqrt(trading_days_per_year))


def calculate_rolling_historical_volatility(
    prices: pd.Series,
    window: int = 20,
) -> pd.Series:
    """calculate rolling annualized historical volatility."""

    if window < 2:
        raise ValueError("Window must be at least 2.")

    if len(prices) < window + 1:
        raise ValueError("prices must contain at least window + 1 observations.")

    returns = calculate_log_returns(prices)

    return returns.rolling(window).std(ddof=1) * (sqrt(trading_days_per_year))
