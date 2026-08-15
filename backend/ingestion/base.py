from abc import ABC, abstractmethod
from typing import Any


class DataSource(ABC):
    """Base interface for market-data sources."""

    @abstractmethod
    def fetch(self, **kwargs: Any) -> Any:
        """Fetch data from the source."""
        raise NotImplementedError
