from __future__ import annotations

import posixpath
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from backend.ingestion.exceptions import DataSourceError


def extract_csv(zip_path: str | Path) -> Path:
    """Extract the csv file from an NSE ZIP archive."""

    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise DataSourceError(f"NSE ZIP file not found:{zip_path}")

    try:
        with ZipFile(zip_path) as archive:
            csv_members = [
                member
                for member in archive.infolist()
                if member.filename.lower().endswith(".csv")
            ]

            if not csv_members:
                raise DataSourceError(f"No csv file found in ZIP archive:{zip_path}")

            if len(csv_members) > 1:
                raise DataSourceError(
                    f"Multiple CSV file found in ZIP archive:{zip_path}"
                )

            member = csv_members[0]

            member_path = posixpath.normpath(member.filename)

            if (
                member_path.startswith("../")
                or member_path == ".."
                or posixpath.isabs(member_path)
            ):
                raise DataSourceError(f"Unsafe ZIP member path:{member.filename}")

            destination = zip_path.parent / Path(member.filename).name

            with archive.open(member) as source:
                destination.write_bytes(source.read())

            return destination

    except BadZipFile as exc:
        raise DataSourceError(f"Invalid ZIP file:{zip_path}") from exc
