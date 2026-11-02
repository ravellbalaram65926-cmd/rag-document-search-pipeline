import zipfile

import pytest

from scripts.download_kaggle import extract_archives


def test_extracts_dataset_archives(tmp_path):
    with zipfile.ZipFile(tmp_path / "dataset.zip", "w") as archive:
        archive.writestr("papers.json", '{"id":"demo"}')

    extract_archives(tmp_path)

    assert (tmp_path / "papers.json").read_text(encoding="utf-8") == '{"id":"demo"}'


def test_rejects_archive_path_traversal(tmp_path):
    with zipfile.ZipFile(tmp_path / "unsafe.zip", "w") as archive:
        archive.writestr("../outside.txt", "unsafe")

    with pytest.raises(ValueError, match="Unsafe archive path"):
        extract_archives(tmp_path)
