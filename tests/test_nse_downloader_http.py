from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx

from backend.ingestion.download.nse_downloader import NSEDownloader
from backend.ingestion.exceptions import DataSourceError


def test_download_success(tmp_path: Path) -> None:
    downloader = NSEDownloader(raw_root=tmp_path)

    response = MagicMock()
    response.content = b"fake zip content"
    response.raise_for_status.return_value = None

    with patch("httpx.Client") as client_class:
        client = client_class.return_value.__enter__.return_value
        client.get.return_value = response

        result = downloader.fetch(
            trade_date=date(2025, 8, 20),
            url="https://example.com/test.zip",
        )

    expected = (
        tmp_path / "udiff" / "2025" / "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv.zip"
    )

    assert result == expected
    assert result.exists()
    assert result.read_bytes() == b"fake zip content"

    client.get.assert_called_once_with("https://example.com/test.zip")


def test_existing_file_skips_download(tmp_path: Path) -> None:
    downloader = NSEDownloader(raw_root=tmp_path)

    existing_file = (
        tmp_path / "udiff" / "2025" / "BhavCopy_NSE_FO_0_0_0_20250820_F_0000.csv.zip"
    )

    existing_file.parent.mkdir(parents=True)
    existing_file.write_bytes(b"already downloaded")

    with patch("httpx.Client") as client_class:
        result = downloader.fetch(
            trade_date=date(2025, 8, 20),
            url="https://example.com/test.zip",
        )

    assert result == existing_file
    assert result.read_bytes() == b"already downloaded"
    client_class.assert_not_called()


def test_http_error_raises_data_source_error(tmp_path: Path) -> None:
    downloader = NSEDownloader(raw_root=tmp_path)

    response = MagicMock()

    response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found",
        request=MagicMock(),
        response=MagicMock(),
    )

    with patch("httpx.Client") as client_class:
        client = client_class.return_value.__enter__.return_value
        client.get.return_value = response

        try:
            downloader.fetch(
                trade_date=date(2025, 8, 20),
                url="https://example.com/missing.zip",
            )

        except DataSourceError as exc:
            assert "Failed to download NSE F&O file" in str(exc)
        else:
            raise AssertionError("DataSourceError was not raised")


def test_file_write_error_raises_data_source_error(tmp_path: Path) -> None:
    downloader = NSEDownloader(raw_root=tmp_path)

    response = MagicMock()
    response.content = b"fake zip content"
    response.raise_for_status.return_value = None

    with patch("httpx.Client") as client_class:
        client = client_class.return_value.__enter__.return_value
        client.get.return_value = response

        with patch(
            "pathlib.Path.write_bytes",
            side_effect=OSError("disk write failed"),
        ):

            try:
                downloader.fetch(
                    trade_date=date(2025, 8, 20),
                    url="https://example.com/test.zip",
                )

            except DataSourceError as exc:
                assert "Failed to save NSE F&O file" in str(exc)
            else:
                raise AssertionError("DataSourceError was not raised.")
