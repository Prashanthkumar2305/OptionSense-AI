import pytest

from backend.quant.iv_hv import (
    IVHVFeatures,
    calculate_iv_hv_features,
)


def test_iv_hv_features() -> None:
    result = calculate_iv_hv_features(
        implied_volatility=0.30,
        historical_volatility=0.20,
    )

    assert isinstance(result, IVHVFeatures)
    assert result.iv_minus_hv == pytest.approx(0.10)
    assert result.iv_hv_ratio == pytest.approx(1.50)
    assert result.iv_premium_pct == pytest.approx(50.0)


def test_iv_below_hv() -> None:
    result = calculate_iv_hv_features(
        implied_volatility=0.15,
        historical_volatility=0.20,
    )

    assert result.iv_minus_hv == pytest.approx(-0.05)
    assert result.iv_hv_ratio == pytest.approx(0.75)
    assert result.iv_premium_pct == pytest.approx(-25.0)


def test_equal_iv_and_hv() -> None:
    result = calculate_iv_hv_features(
        implied_volatility=0.20,
        historical_volatility=0.20,
    )

    assert result.iv_minus_hv == pytest.approx(0.0)
    assert result.iv_hv_ratio == pytest.approx(1.0)
    assert result.iv_premium_pct == pytest.approx(0.0)


def test_negative_iv_is_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_iv_hv_features(
            implied_volatility=-0.10,
            historical_volatility=0.20,
        )


def test_zero_hv_is_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_iv_hv_features(
            implied_volatility=0.20,
            historical_volatility=0.0,
        )


def test_negative_hv_is_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_iv_hv_features(
            implied_volatility=0.20,
            historical_volatility=-0.10,
        )
