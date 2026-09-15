from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from backend.ingestion.download.extractor import (
    extract_csv,
    extract_member,
)
from backend.ingestion.download.nse_downloader import (
    NSEDownloader,
    NSEFOSource,
    resolve_download_url,
    resolve_file_spec,
)


@dataclass(frozen=True)
class NSEDownloadResult:
    """Result of downloading and extracting one NSE F&O file..."""

    trade_date: date
    source: NSEFOSource
    zip_path: Path
    csv_path: Path | None = None
    futures_csv_path: Path | None = None
    options_csv_path: Path | None = None


class NSEDownloadPipeline:
    """Orchestrate NSE F&O download and extraction..."""

    def __init__(
        self,
        raw_root: str | Path = "data/raw/nse/fo",
        timeout: float = 30.0,
    ) -> None:
        self.downloader = NSEDownloader(
            raw_root=raw_root,
            timeout=timeout,
        )

    def run(
        self,
        trade_date: date,
    ) -> NSEDownloadResult:
        """Download and extract the NSE F&O file for a trading date..."""

        file_spec = resolve_file_spec(trade_date)

        url = resolve_download_url(trade_date)

        zip_path = self.downloader.fetch(
            trade_date=trade_date,
            url=url,
        )

        if file_spec.source is NSEFOSource.UDIFF:
            csv_path = extract_csv(zip_path)

            return NSEDownloadResult(
                trade_date=trade_date,
                source=file_spec.source,
                zip_path=zip_path,
                csv_path=csv_path,
            )

        if file_spec.futures_csv_name is None or file_spec.options_csv_name is None:
            raise ValueError("Legacy NSE file specification is incomplete..")

        future_csv_path = extract_member(
            zip_path,
            file_spec.futures_csv_name,
        )

        options_csv_path = extract_member(
            zip_path,
            file_spec.options_csv_name,
        )

        return NSEDownloadResult(
            trade_date=trade_date,
            source=file_spec.source,
            zip_path=zip_path,
            futures_csv_path=future_csv_path,
            options_csv_path=options_csv_path,
        )
