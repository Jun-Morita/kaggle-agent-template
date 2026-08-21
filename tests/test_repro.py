from __future__ import annotations

import json

from kaggle_agent_template import repro


def test_write_run_metadata_is_unique_and_records_git_state(tmp_path, monkeypatch) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("experiment:\n  seed: 42\n", encoding="utf-8")
    output_dir = tmp_path / "results"

    monkeypatch.setattr(repro, "git_sha", lambda cwd=None: "abc1234")
    monkeypatch.setattr(repro, "git_is_dirty", lambda cwd=None: True)

    first_path = repro.write_run_metadata(output_dir, config_path)
    second_path = repro.write_run_metadata(output_dir, config_path)

    assert first_path != second_path
    assert first_path.name.startswith("run_metadata_")
    metadata = json.loads(first_path.read_text(encoding="utf-8"))
    assert metadata["git_sha"] == "abc1234"
    assert metadata["git_dirty"] is True
    assert metadata["config_hash"] == repro.short_file_sha256(config_path)
