import math

import pandas as pd
import pytest

from backend.quant.volatility import (
    calculate_historical_volatality,
    calculate_log_returns,
    calculate_rolling_historical_volatility,
)


def test_log_returns() -> None:
    prices = pd.Series([100.0, 110.0, 121.0])

    returns = calculate_log_returns(prices)

    assert pd.isna(returns.iloc[0])
    assert returns.iloc[1] == pytest.approx(math.log(1.10))
    assert returns.iloc[2] == pytest.approx(math.log(1.10))


def test_historical_volatility() -> None:
    prices = pd.Series(
        [
            100.0,
            101.0,
            99.0,
            102.0,
            101.5,
            103.0,
            104.0,
            102.0,
            105.0,
            106.0,
            104.0,
            107.0,
            108.0,
            106.0,
            109.0,
            110.0,
            108.0,
            111.0,
            112.0,
            110.0,
            113.0,
        ]
    )

    hv = calculate_historical_volatality(
        prices,
        window=20,
    )

    assert hv > 0
    assert isinstance(hv, float)


def test_rolling_historical_volatility() -> None:
    prices = pd.Series(
        [
            100.0,
            101.0,
            102.0,
            101.0,
            103.0,
            104.0,
            105.0,
            104.0,
            106.0,
            107.0,
        ]
    )

    hv = calculate_rolling_historical_volatility(
        prices,
        window=5,
    )

    assert len(hv) == len(prices)
    assert pd.isna(hv.iloc[0])
    assert pd.isna(hv.iloc[4])
    assert pd.notna(hv.iloc[5])
    assert hv.iloc[5] > 0


def test_negative_prices_are_rejected() -> None:
    prices = pd.Series(
        [
            100.0,
            101.0,
            -10.0,
        ]
    )

    with pytest.raises(ValueError):
        calculate_log_returns(prices)


def test_empty_prices_are_rejected() -> None:
    prices = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        calculate_log_returns(prices)


def test_invalid_window_is_rejected() -> None:
    prices = pd.Series(
        [
            100.0,
            101.0,
            102.0,
        ]
    )

    with pytest.raises(ValueError):
        calculate_historical_volatality(
            prices,
            window=1,
        )


def test_insufficient_prices_are_rejected() -> None:
    prices = pd.Series(
        [
            100.0,
            101.0,
            102.0,
        ]
    )

    with pytest.raises(ValueError):
        calculate_historical_volatality(
            prices,
            window=5,
        )
