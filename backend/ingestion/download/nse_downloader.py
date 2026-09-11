from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path

import httpx

from backend.ingestion.base import DataSource
from backend.ingestion.exceptions import DataSourceError


class NSEFOSource(StrEnum):
    """NSe f&o Bhavcopy source format."""

    LEGACY = "legacy"
    UDIFF = "udiff"


# NSE changed from the legacy F&O bhavcopy to UDIFF in July 2024.
# We'll keep this date explicit so the transition rule is easy to audit.

UDIFF_START_DATE = date(2024, 7, 8)


@dataclass(frozen=True)
class NSEFileSpec:
    """Metadata describing one NSE F&O Bhavcopy."""

    trade_date: date
    source: NSEFOSource
    zip_name: str
    csv_name: str


def resolve_file_spec(trade_date: date) -> NSEFileSpec:
    """Return the expected ZIP and CSV names for an NSE F&O Bhavcopy."""

    if trade_date < UDIFF_START_DATE:
        ddmmyy = trade_date.strftime("%d%m%y")

        return NSEFileSpec(
            trade_date=trade_date,
            source=NSEFOSource.LEGACY,
            zip_name=f"fo{ddmmyy}.zip",
            csv_name=f"fo{ddmmyy}.csv",
        )

    yyyymmdd = trade_date.strftime("%Y%m%d")

    return NSEFileSpec(
        trade_date=trade_date,
        source=NSEFOSource.UDIFF,
        zip_name=f"BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
        csv_name=f"BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv",
    )


def resolve_raw_zip_path(
    trade_date: date,
    raw_root: str | Path,
) -> Path:
    """Return the local raw ZIP path for an NSE F&O trading date."""

    raw_root = Path(raw_root)
    file_spec = resolve_file_spec(trade_date)

    return raw_root / file_spec.source.value / str(trade_date.year) / file_spec.zip_name


class NSEDownloader(DataSource):
    """Downloader for NSE F&O BhavCopy files..."""

    def __init__(
        self,
        raw_root: str | Path = "data/raw/nse/fo",
        timeout: float = 30.0,
    ) -> None:
        self.raw_root = Path(raw_root)
        self.timeout = timeout

    def fetch(self, **kwargs: object) -> Path:
        """Download an NSE F&O ZIP file and return its local path."""

        trade_date = kwargs.get("trade_date")
        url = kwargs.get("url")

        if not isinstance(trade_date, date):
            raise ValueError("trade_date must be a datetime.date")

        if not isinstance(url, str):
            raise ValueError("url must be a string")

        destination = resolve_raw_zip_path(
            trade_date,
            self.raw_root,
        )

        if destination.exists():
            return destination

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            with httpx.Client(
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                response = client.get(url)
                response.raise_for_status()

        except httpx.HTTPError as exc:
            raise DataSourceError(f"Failed to download NSE F&O file:{url}") from exc

        temporary_path = destination.with_suffix(destination.suffix + ".tmp")

        try:
            temporary_path.write_bytes(response.content)
            temporary_path.replace(destination)

        except OSError as exc:
            temporary_path.unlink(missing_ok=True)
            raise DataSourceError(f"Failed to save NSE F&O file:{destination}") from exc

        return destination
