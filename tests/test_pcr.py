import pytest

from backend.quant.pcr import PCR, calculate_pcr


def test_pcr_calculation() -> None:
    result = calculate_pcr(
        put_open_interest=120_000,
        call_open_interest=100_000,
        put_volume=60_000,
        call_volume=50_000,
    )

    assert isinstance(result, PCR)
    assert result.oi_pcr == pytest.approx(1.20)
    assert result.volume_pcr == pytest.approx(1.20)


def test_pcr_below_one() -> None:
    result = calculate_pcr(
        put_open_interest=80_000,
        call_open_interest=100_000,
        put_volume=40_000,
        call_volume=50_000,
    )

    assert result.oi_pcr == pytest.approx(0.80)
    assert result.volume_pcr == pytest.approx(0.80)


def test_zero_call_oi_is_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_pcr(
            put_open_interest=100_000,
            call_open_interest=0,
            put_volume=50_000,
            call_volume=50_000,
        )


def test_zero_call_volume_is_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_pcr(
            put_open_interest=100_000,
            call_open_interest=100_000,
            put_volume=50_000,
            call_volume=0,
        )


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "put_open_interest": -1,
            "call_open_interest": 100,
            "put_volume": 50,
            "call_volume": 50,
        },
        {
            "put_open_interest": 100,
            "call_open_interest": -1,
            "put_volume": 50,
            "call_volume": 50,
        },
        {
            "put_open_interest": 100,
            "call_open_interest": 100,
            "put_volume": -1,
            "call_volume": 50,
        },
        {
            "put_open_interest": 100,
            "call_open_interest": 100,
            "put_volume": 50,
            "call_volume": -1,
        },
    ],
)
def test_negative_values_are_rejected(
    kwargs: dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        calculate_pcr(**kwargs)
