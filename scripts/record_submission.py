from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path

FIELDS = [
    "timestamp",
    "version",
    "source_experiment",
    "fold_version",
    "cv",
    "public_lb",
    "private_lb",
    "file",
    "file_hash",
    "config_hash",
    "git_sha",
    "references",
    "note",
]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--source-experiment", required=True)
    parser.add_argument("--fold-version", default="")
    parser.add_argument("--cv", default="")
    parser.add_argument("--public-lb", default="")
    parser.add_argument("--private-lb", default="")
    parser.add_argument("--file", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--references", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--log", type=Path, default=Path("submit/submissions.csv"))
    return parser.parse_args()


def read_rows(log_path: Path) -> list[dict[str, str]]:
    if not log_path.exists() or log_path.stat().st_size == 0:
        return []
    with log_path.open(encoding="utf-8", newline="") as f:
        return [{field: row.get(field, "") for field in FIELDS} for row in csv.DictReader(f)]


def upsert_row(log_path: Path, row: dict[str, str]) -> str:
    rows = read_rows(log_path)
    matching = [existing for existing in rows if existing["version"] == row["version"]]
    action = "updated" if matching else "recorded"

    if matching:
        merged = matching[0]
        for existing in matching[1:]:
            merged.update({key: value for key, value in existing.items() if value})
        merged.update({key: value for key, value in row.items() if value})
        updated_rows = []
        inserted = False
        for existing in rows:
            if existing["version"] == row["version"]:
                if not inserted:
                    updated_rows.append(merged)
                    inserted = True
                continue
            updated_rows.append(existing)
        rows = updated_rows
    else:
        rows.append(row)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="", dir=log_path.parent, delete=False
    ) as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        temporary_path = Path(f.name)
    temporary_path.replace(log_path)
    return action


def main() -> None:
    args = parse_args()
    if args.file is not None and not args.file.is_file():
        raise SystemExit(f"submission file not found: {args.file}")

    row = {
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
        "version": args.version,
        "source_experiment": args.source_experiment,
        "fold_version": args.fold_version,
        "cv": args.cv,
        "public_lb": args.public_lb,
        "private_lb": args.private_lb,
        "file": str(args.file) if args.file else "",
        "file_hash": file_sha256(args.file) if args.file else "",
        "config_hash": file_sha256(args.config)[:12] if args.config else "",
        "git_sha": git_sha(),
        "references": args.references,
        "note": args.note,
    }

    action = upsert_row(args.log, row)
    print(f"{action} submission: {args.log}")


if __name__ == "__main__":
    main()
