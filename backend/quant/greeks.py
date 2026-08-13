from dataclasses import dataclass
from math import exp, log, pi, sqrt
from statistics import NormalDist


@dataclass(frozen=True)
class Greeks:
    """Option greeks calculated using the black-scholes model."""

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


def calculate_greeks(
    spot_price: float,
    strike_price: float,
    time_to_expiry: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str,
) -> Greeks:
    """calculate Black-scholes greeks for a european option.

    Parameters:
        spot_price:Current underlying price.
        strike_price: option strike price.
        time_to_expiry : Time to expiry in years.
        risk_free_rate :  Annualized risk-free rate as decimal.
        volatility : Annualized implied volatility as decimal.
        option_type : CE for call or PE for put.

    Returns:
        Greeks containing delta,gamma,theta,vega and rho.

    """

    if spot_price <= 0:
        raise ValueError("Spot_price must be greater than zero.")

    if strike_price <= 0:
        raise ValueError("Strike_price must be greater than zero.")

    if time_to_expiry <= 0:
        raise ValueError("time_to_expiry must be greater than zero.")

    if volatility <= 0:
        raise ValueError("volatility must be greater than zero.")

    option_type = option_type.upper()

    if option_type not in {"CE", "PE"}:
        raise ValueError("Option_type must be in 'CE' or 'PE'.")

    sqrt_t = sqrt(time_to_expiry)

    d1 = (
        log(spot_price / strike_price)
        + (risk_free_rate + (volatility**2 / 2)) * time_to_expiry
    ) / (volatility * sqrt_t)

    d2 = d1 - volatility * sqrt_t

    normal = NormalDist()

    pdf_d1 = exp(-(d1**2) / 2) / sqrt(2 * pi)

    nd1 = normal.cdf(d1)
    nd2 = normal.cdf(d2)

    discount_factor = exp(-risk_free_rate * time_to_expiry)

    gamma = pdf_d1 / (spot_price * volatility * sqrt_t)

    vega = spot_price * pdf_d1 * sqrt_t / 100

    if option_type == "CE":
        delta = nd1

        theta = (
            -(spot_price * pdf_d1 * volatility) / (2 * sqrt_t)
            - risk_free_rate * strike_price * discount_factor * nd2
        ) / 365

        rho = strike_price * time_to_expiry * discount_factor * nd2 / 100

    else:
        delta = nd1 - 1
        theta = (
            -(spot_price * pdf_d1 * volatility) / (2 * sqrt_t)
            + risk_free_rate * strike_price * discount_factor * normal.cdf(-d2)
        ) / 365

        rho = -strike_price * time_to_expiry * discount_factor * normal.cdf(-d2) / 100

    return Greeks(
        delta=delta,
        gamma=gamma,
        theta=theta,
        vega=vega,
        rho=rho,
    )
