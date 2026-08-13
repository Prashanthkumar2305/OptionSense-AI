import pytest

from backend.quant.greeks import Greeks, calculate_greeks


def test_call_greeks() -> None:
    greeks = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="CE",
    )

    assert isinstance(greeks, Greeks)
    assert 0 < greeks.delta < 1
    assert greeks.gamma > 0
    assert greeks.vega > 0


def test_put_greeks() -> None:
    greeks = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="PE",
    )

    assert isinstance(greeks, Greeks)
    assert -1 < greeks.delta < 0
    assert greeks.gamma > 0
    assert greeks.vega > 0


@pytest.mark.parametrize(
    "option_type",
    ["CE", "PE"],
)
def test_invalid_spot_price(option_type: str) -> None:
    with pytest.raises(ValueError):
        calculate_greeks(
            spot_price=0,
            strike_price=100,
            time_to_expiry=30 / 365,
            risk_free_rate=0.06,
            volatility=0.20,
            option_type=option_type,
        )


def test_invalid_option_tpe() -> None:
    with pytest.raises(ValueError):
        calculate_greeks(
            spot_price=100,
            strike_price=100,
            time_to_expiry=30 / 365,
            risk_free_rate=0.06,
            volatility=0.20,
            option_type="INVALID",
        )


def test_atm_call_greeks_are_reasonable() -> None:
    greeks = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="CE",
    )

    assert greeks.delta == pytest.approx(0.545, abs=0.01)
    assert greeks.gamma == pytest.approx(0.069, abs=0.005)
    assert greeks.theta == pytest.approx(-0.046, abs=0.005)
    assert greeks.vega == pytest.approx(0.114, abs=0.005)
    assert greeks.rho == pytest.approx(0.040, abs=0.005)


def test_call_put_delta_relationship() -> None:
    call = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="CE",
    )

    put = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="PE",
    )

    assert call.delta - put.delta == pytest.approx(1.0, abs=1e-6)


def test_call_put_gamma_is_same() -> None:
    call = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="CE",
    )

    put = calculate_greeks(
        spot_price=100.0,
        strike_price=100.0,
        time_to_expiry=30 / 365,
        risk_free_rate=0.06,
        volatility=0.20,
        option_type="PE",
    )

    assert call.gamma == pytest.approx(put.gamma, abs=1e-10)
