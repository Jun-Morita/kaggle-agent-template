from __future__ import annotations

import csv
import sys

from scripts.record_submission import FIELDS, file_sha256, main, read_rows, upsert_row


def make_row(version: str, **updates: str) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    row.update({"version": version, **updates})
    return row


def test_upsert_row_writes_header_to_empty_log(tmp_path) -> None:
    log_path = tmp_path / "submissions.csv"
    log_path.touch()

    action = upsert_row(log_path, make_row("v001", cv="0.8"))

    assert action == "recorded"
    with log_path.open(encoding="utf-8", newline="") as f:
        assert next(csv.reader(f)) == FIELDS


def test_upsert_row_updates_unique_version_and_preserves_values(tmp_path) -> None:
    log_path = tmp_path / "submissions.csv"
    upsert_row(log_path, make_row("v001", cv="0.8", file="submission.csv"))

    action = upsert_row(log_path, make_row("v001", public_lb="0.79"))
    rows = read_rows(log_path)

    assert action == "updated"
    assert rows == [make_row("v001", cv="0.8", public_lb="0.79", file="submission.csv")]


def test_file_sha256_returns_full_digest(tmp_path) -> None:
    submission_path = tmp_path / "submission.csv"
    submission_path.write_text("id,target\n1,0.5\n", encoding="utf-8")

    assert len(file_sha256(submission_path)) == 64


def test_main_records_file_hash_and_updates_same_version(tmp_path, monkeypatch) -> None:
    submission_path = tmp_path / "submission.csv"
    submission_path.write_text("id,target\n1,0.5\n", encoding="utf-8")
    log_path = tmp_path / "submissions.csv"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "record_submission.py",
            "--version",
            "v001",
            "--source-experiment",
            "exp001_baseline",
            "--file",
            str(submission_path),
            "--log",
            str(log_path),
        ],
    )
    main()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "record_submission.py",
            "--version",
            "v001",
            "--source-experiment",
            "exp001_baseline",
            "--public-lb",
            "0.79",
            "--log",
            str(log_path),
        ],
    )
    main()

    rows = read_rows(log_path)
    assert len(rows) == 1
    assert rows[0]["file"] == str(submission_path)
    assert rows[0]["file_hash"] == file_sha256(submission_path)
    assert rows[0]["public_lb"] == "0.79"
