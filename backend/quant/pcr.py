from dataclasses import dataclass


@dataclass(frozen=True)
class PCR:
    """Put / Call ratio metrics."""

    oi_pcr: float
    volume_pcr: float


def calculate_pcr(
    put_open_interest: float,
    call_open_interest: float,
    put_volume: float,
    call_volume: float,
) -> PCR:
    """Calculate OI PCR and volume PCR."""

    if put_open_interest < 0:
        raise ValueError("put_open_interest cannot be negative.")

    if call_open_interest < 0:
        raise ValueError("call_open_interest cannot be negative.")

    if put_volume < 0:
        raise ValueError("put_volume cannot be negative.")

    if call_volume < 0:
        raise ValueError("call_volume cannot be negative.")

    if call_open_interest == 0:
        raise ValueError("call_open_interest cannot be zero.")

    if call_volume == 0:
        raise ValueError("Call_volume cannot be zero.")

    return PCR(
        oi_pcr=put_open_interest / call_open_interest,
        volume_pcr=put_volume / call_volume,
    )
