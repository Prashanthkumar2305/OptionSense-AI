from backend.ingestion.exceptions import DataValidationError
from backend.ingestion.models import OHLCVRecord


def validate_ohlcv(record: OHLCVRecord) -> None:
    """Validate a normalized OHLCV record."""

    if not record.symbol.strip():
        raise DataValidationError("symbol cannot be empty.")

    if record.open <= 0:
        raise DataValidationError("open price must be greater than zero.")

    if record.high <= 0:
        raise DataValidationError("high price must be greater than zero.")

    if record.low <= 0:
        raise DataValidationError("low price must be greater than zero.")

    if record.close <= 0:
        raise DataValidationError("close price must be greater than zero.")

    if record.volume < 0:
        raise DataValidationError("volume cannot be negative.")

    if record.high < record.open:
        raise DataValidationError("high price cannot be below open price.")

    if record.high < record.close:
        raise DataValidationError("high price cannot be below close price.")

    if record.low > record.open:
        raise DataValidationError("low price cannot be above open price.")

    if record.low > record.close:
        raise DataValidationError("low price cannot be above close price.")
