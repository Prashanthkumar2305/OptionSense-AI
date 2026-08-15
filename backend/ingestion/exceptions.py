class IngestionError(Exception):
    """Base exception for ingestion errors."""


class DataValidationError(IngestionError):
    """Raised when incoming market data is invalid."""


class DataSourceError(IngestionError):
    """Raised when a data source cannot be accessed."""
