[1mdiff --git a/backend/ingestion/download/extractor.py b/backend/ingestion/download/extractor.py[m
[1mindex 4d7cb5c..9fa8c98 100644[m
[1m--- a/backend/ingestion/download/extractor.py[m
[1m+++ b/backend/ingestion/download/extractor.py[m
[36m@@ -51,3 +51,47 @@[m [mdef extract_csv(zip_path: str | Path) -> Path:[m
 [m
     except BadZipFile as exc:[m
         raise DataSourceError(f"Invalid ZIP file:{zip_path}") from exc[m
[32m+[m
[32m+[m
[32m+[m[32mdef extract_member([m
[32m+[m[32m    zip_path: str | Path,[m
[32m+[m[32m    member_name: str,[m
[32m+[m[32m) -> Path:[m
[32m+[m[32m    """Extract a specific member from an NSE ZIP archive."""[m
[32m+[m
[32m+[m[32m    zip_path = Path(zip_path)[m
[32m+[m
[32m+[m[32m    if not zip_path.exists():[m
[32m+[m[32m        raise DataSourceError(f"NSE ZIP file not found: {zip_path}")[m
[32m+[m
[32m+[m[32m    try:[m
[32m+[m[32m        with ZipFile(zip_path) as archive:[m
[32m+[m[32m            try:[m
[32m+[m[32m                member = archive.getinfo(member_name)[m
[32m+[m[32m            except KeyError as exc:[m
[32m+[m[32m                raise DataSourceError([m
[32m+[m[32m                    f"ZIP member not found: {member_name}"[m
[32m+[m[32m                ) from exc[m
[32m+[m
[32m+[m[32m            member_path = posixpath.normpath(member.filename)[m
[32m+[m
[32m+[m[32m            if ([m
[32m+[m[32m                member_path.startswith("../")[m
[32m+[m[32m                or member_path == ".."[m
[32m+[m[32m                or posixpath.isabs(member_path)[m
[32m+[m[32m            ):[m
[32m+[m[32m                raise DataSourceError([m
[32m+[m[32m                    f"Unsafe ZIP member path: {member.filename}"[m
[32m+[m[32m                )[m
[32m+[m
[32m+[m[32m            destination = zip_path.parent / Path(member.filename).name[m
[32m+[m
[32m+[m[32m            with archive.open(member) as source:[m
[32m+[m[32m                destination.write_bytes(source.read())[m
[32m+[m
[32m+[m[32m            return destination[m
[32m+[m
[32m+[m[32m    except BadZipFile as exc:[m
[32m+[m[32m        raise DataSourceError([m
[32m+[m[32m            f"Invalid ZIP file: {zip_path}"[m
[32m+[m[32m        ) from exc[m
\ No newline at end of file[m
[1mdiff --git a/tests/test_extractor.py b/tests/test_extractor.py[m
[1mindex 242a77d..29469aa 100644[m
[1m--- a/tests/test_extractor.py[m
[1m+++ b/tests/test_extractor.py[m
[36m@@ -3,7 +3,8 @@[m [mfrom zipfile import ZipFile[m
 [m
 import pytest[m
 [m
[31m-from backend.ingestion.download.extractor import extract_csv[m
[32m+[m[32mfrom backend.ingestion.download.extractor import (extract_csv,[m
[32m+[m[32m                                                  extract_member,)[m
 from backend.ingestion.exceptions import DataSourceError[m
 [m
 [m
[36m@@ -101,3 +102,59 @@[m [mdef test_absolute_zip_path_is_rejected(tmp_path: Path) -> None:[m
 [m
     with pytest.raises(DataSourceError):[m
         extract_csv(zip_path)[m
[32m+[m
[32m+[m[32mdef test_extract_member_from_multi_csv_zip(tmp_path: Path) -> None:[m
[32m+[m[32m    zip_path = tmp_path / "legacy.zip"[m
[32m+[m
[32m+[m[32m    with ZipFile(zip_path, "w") as archive:[m
[32m+[m[32m        archive.writestr([m
[32m+[m[32m            "fo050724.csv",[m
[32m+[m[32m            "contract,close\nNIFTY,25000\n",[m
[32m+[m[32m        )[m
[32m+[m[32m        archive.writestr([m
[32m+[m[32m            "op050724.csv",[m
[32m+[m[32m            "contract,close\nOPTNIFTY,100\n",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    result = extract_member([m
[32m+[m[32m        zip_path,[m
[32m+[m[32m        "op050724.csv",[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    expected = tmp_path / "op050724.csv"[m
[32m+[m
[32m+[m[32m    assert result == expected[m
[32m+[m[32m    assert result.exists()[m
[32m+[m[32m    assert result.read_text() == "contract,close\nOPTNIFTY,100\n"[m
[32m+[m
[32m+[m
[32m+[m[32mdef test_extract_member_not_found_raises_error(tmp_path: Path) -> None:[m
[32m+[m[32m    zip_path = tmp_path / "legacy.zip"[m
[32m+[m
[32m+[m[32m    create_zip([m
[32m+[m[32m        zip_path,[m
[32m+[m[32m        "fo050724.csv",[m
[32m+[m[32m        "contract,close\nNIFTY,25000\n",[m
[32m+[m[32m    )[m
[32m+[m
[32m+[m[32m    with pytest.raises(DataSourceError):[m
[32m+[m[32m        extract_member([m
[32m+[m[32m            zip_path,[m
[32m+[m[32m            "op050724.csv",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m
[32m+[m[32mdef test_extract_member_path_traversal_is_rejected(tmp_path: Path) -> None:[m
[32m+[m[32m    zip_path = tmp_path / "malicious.zip"[m
[32m+[m
[32m+[m[32m    with ZipFile(zip_path, "w") as archive:[m
[32m+[m[32m        archive.writestr([m
[32m+[m[32m            "../../malicious.csv",[m
[32m+[m[32m            "malicious,data\n",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    with pytest.raises(DataSourceError):[m
[32m+[m[32m        extract_member([m
[32m+[m[32m            zip_path,[m
[32m+[m[32m            "../../malicious.csv",[m
[32m+[m[32m        )[m
\ No newline at end of file[m
