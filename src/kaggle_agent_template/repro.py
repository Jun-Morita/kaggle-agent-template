from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import random
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np


def set_seed(seed: int, deterministic_torch: bool = False) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)

    try:
        import torch
    except ImportError:
        return

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    if deterministic_torch:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def short_file_sha256(path: Path, length: int = 12) -> str:
    return file_sha256(path)[:length]


def git_sha(cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def git_is_dirty(cwd: Path | None = None) -> bool | None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return bool(result.stdout.strip())


def package_versions(packages: list[str] | None = None) -> dict[str, str]:
    packages = packages or ["numpy", "pandas", "scikit-learn"]
    versions: dict[str, str] = {}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = ""
    return versions


def write_run_metadata(
    output_dir: Path,
    config_path: Path | None = None,
    extra: dict[str, Any] | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    run_timestamp = datetime.now(UTC)
    config_hash = short_file_sha256(config_path) if config_path else ""
    metadata = {
        "timestamp": run_timestamp.isoformat(timespec="microseconds"),
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "git_sha": git_sha(),
        "git_dirty": git_is_dirty(),
        "config_path": str(config_path) if config_path else "",
        "config_hash": config_hash,
        "packages": package_versions(),
        "extra": extra or {},
    }

    run_id = run_timestamp.strftime("%Y%m%dT%H%M%S%fZ")
    output_path = output_dir / f"run_metadata_{run_id}_{config_hash or 'no-config'}.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return output_path
