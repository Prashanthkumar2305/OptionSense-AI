from pathlib import Path
from zipfile import ZipFile

import pytest

from backend.ingestion.download.extractor import extract_csv
from backend.ingestion.exceptions import DataSourceError


def create_zip(
    zip_path: Path,
    filename: str,
    content: str,
) -> None:

    with ZipFile(zip_path, "w") as archive:
        archive.writestr(filename, content)


def test_extract_csv(tmp_path: Path) -> None:
    zip_path = tmp_path / "sample.zip"

    create_zip(
        zip_path,
        "sample.csv",
        "symbol,close\nNIFTY,25000\n",
    )

    result = extract_csv(zip_path)

    expected = tmp_path / "sample.csv"
    assert result == expected
    assert result.exists()
    assert result.read_text() == "symbol,close\nNIFTY,25000\n"


def test_extract_expected_csv_from_zip_with_other_files(
    tmp_path: Path,
) -> None:

    zip_path = tmp_path / "sample.zip"

    with ZipFile(zip_path, "w") as archive:
        archive.writestr("README.txt", "test")
        archive.writestr(
            "sample.csv",
            "symbol,close\nNIFTY,25000\n",
        )

    result = extract_csv(zip_path)

    assert result == tmp_path / "sample.csv"


def test_missing_zip_raises_error(tmp_path: Path) -> None:
    zip_path = tmp_path / "missing.zip"

    with pytest.raises(DataSourceError):
        extract_csv(zip_path)


def test_invalid_zip_raises_error(tmp_path: Path) -> None:
    zip_path = tmp_path / "invalid.zip"
    zip_path.write_text("this is not a zip file.")

    with pytest.raises(DataSourceError):
        extract_csv(zip_path)


def test_zip_without_csv_raises_error(tmp_path: Path) -> None:
    zip_path = tmp_path / "sample.zip"

    with ZipFile(zip_path, "w") as archive:
        archive.writestr("README.txt", "test")

    with pytest.raises(DataSourceError):
        extract_csv(zip_path)


def test_path_traversal_is_rejected(tmp_path: Path) -> None:
    zip_path = tmp_path / "malicious.zip"

    with ZipFile(zip_path, "w") as archive:
        archive.writestr(
            "../../malicious.csv",
            "malicious,data\n",
        )

    with pytest.raises(DataSourceError):
        extract_csv(zip_path)


def test_absolute_zip_path_is_rejected(tmp_path: Path) -> None:
    zip_path = tmp_path / "absolute.zip"

    with ZipFile(zip_path, "w") as archive:
        archive.writestr(
            "/malicious.csv",
            "malicious,data\n",
        )

    with pytest.raises(DataSourceError):
        extract_csv(zip_path)
