from datetime import date
from pathlib import Path
from zipfile import ZipFile

import pytest

from backend.ingestion.download.extractor import (
    extract_csv,
)
from backend.ingestion.download.nse_downloader import resolve_raw_zip_path
from backend.ingestion.download.pipeline import NSEDownloadPipeline
from backend.ingestion.exceptions import DataSourceError


def test_downloaded_zip_can_be_extracted(tmp_path:Path)->None:
    trade_date = date(2025,8,20)

    zip_path = resolve_raw_zip_path(
        trade_date,
        tmp_path,
    )

    zip_path.parent.mkdir(parents=True,exist_ok=True,)

    csv_name = "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"
    csv_content = "symbol,close,volume\nNIFTY,25000,1000\n"

    with ZipFile(zip_path,'w') as archive:
        archive.writestr(csv_name,csv_content)

    extracted_csv = extract_csv(zip_path)

    assert extracted_csv == zip_path.parent / csv_name
    assert extracted_csv.exists()
    assert extracted_csv.read_text() == csv_content



def test_pipeline_extracts_udiff_csv(
        tmp_path:Path,
        monkeypatch,
)->None:
    trade_date = date(2025,8,20)

    zip_path = resolve_raw_zip_path(
        trade_date,
        tmp_path,
    )

    zip_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_name = "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv"
    csv_content = "symbol,close,volume\nNIFTY,25000,1000\n"

    with ZipFile(zip_path,'w') as archive:
        archive.writestr(
            csv_name,
            csv_content,
        )


    pipeline = NSEDownloadPipeline(raw_root = tmp_path)

    result = pipeline.run(
        trade_date = trade_date,
        url = 'https://example.com/test.zip',
    )

    assert result.trade_date == trade_date
    assert result.source.value == 'udiff'
    assert result.csv_path == zip_path.parent/csv_name
    assert result.csv_path.exists()


def test_pipeline_extracts_legacy_futures_and_options(
        tmp_path:Path,
)->None:
    trade_date = date(2024,7,5)

    zip_path = resolve_raw_zip_path(
        trade_date,
        tmp_path,
    )

    zip_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    futures_csv = 'fo050724.csv'
    options_csv = 'op050724.csv'

    futures_content = "contract,close\nNIFTY,25000\n"
    options_content = "contract,close\nOPTNIFTY,100\n"

    with ZipFile(zip_path, 'w') as archive:
        archive.writestr(
            futures_csv,
            futures_content,
        )

        archive.writestr(
            options_csv,
            options_content,
        )

    pipeline = NSEDownloadPipeline(
        raw_root=tmp_path,
    )

    result = pipeline.run(
        trade_date = trade_date,
        url = "https://example.com/test.zip",
    )

    assert result.trade_date == trade_date
    assert result.source.value == 'legacy'
    assert result.zip_path == zip_path
    assert result.futures_csv_path == zip_path.parent / futures_csv
    assert result.options_csv_path == zip_path.parent / options_csv


def test_pipeline_raises_when_legacy_options_csv_is_missing(
        tmp_path:Path,
)-> None:
    trade_date = date(2024,7,5)

    zip_path = resolve_raw_zip_path(
        trade_date,
        tmp_path,
    )


    zip_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ZipFile(zip_path,'w') as archive:
        archive.writestr(
            "fo050724.csv",
            "contract,close\nNIFTY,25000\n",
        )

    pipeline = NSEDownloadPipeline(
        raw_root=tmp_path,
    )

    with pytest.raises(DataSourceError):
        pipeline.run(
            trade_date=trade_date,
            url = "https://example.com/test.zip",
        )


def test_pipeline_raises_when_legacy_futures_csv_is_missing(
    tmp_path: Path,
) -> None:
    trade_date = date(2024, 7, 5)

    zip_path = resolve_raw_zip_path(
        trade_date,
        tmp_path,
    )

    zip_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ZipFile(zip_path, "w") as archive:
        archive.writestr(
            "op050724.csv",
            "contract,close\nOPTNIFTY,100\n",
        )

    pipeline = NSEDownloadPipeline(
        raw_root=tmp_path,
    )

    with pytest.raises(DataSourceError):
        pipeline.run(
            trade_date=trade_date,
            url="https://example.com/test.zip",
        )