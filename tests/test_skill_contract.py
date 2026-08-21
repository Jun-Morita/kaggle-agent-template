from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

SKILL_DIR = Path(".claude/skills/nvidia-kaggle-skill")
SKILL_PATH = SKILL_DIR / "SKILL.md"


def read_skill() -> tuple[dict[str, object], str]:
    _, frontmatter, body = SKILL_PATH.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(frontmatter), body


def test_skill_discovery_metadata() -> None:
    metadata, _ = read_skill()
    name = str(metadata["name"])
    description = str(metadata["description"])
    serialized_metadata = json.dumps(metadata)

    assert name == SKILL_DIR.name
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
    assert len(description) <= 1024
    assert "Use " in description and "Not " in description
    assert "<" not in serialized_metadata and ">" not in serialized_metadata
    assert not (SKILL_DIR / "README.md").exists()


def test_linked_workflows_exist() -> None:
    _, body = read_skill()
    linked_files = re.findall(r"`\./([^`]+\.md)`", body)

    assert linked_files
    assert all((SKILL_DIR / path).is_file() for path in linked_files)


def test_submission_history_components_exist() -> None:
    submission_workflow = (SKILL_DIR / "submission.md").read_text(encoding="utf-8")

    assert (SKILL_DIR / "scripts/submission_history.py").is_file()
    assert (SKILL_DIR / "scripts/submission_log.py").is_file()
    assert "submission_history.py" in submission_workflow


def test_evals_cover_triggering_and_non_triggering_queries() -> None:
    evals = json.loads((SKILL_DIR / "evals/evals.json").read_text(encoding="utf-8"))
    ids = [case["id"] for case in evals]

    assert len(ids) == len(set(ids))
    assert any(case["expected_skill"] == SKILL_DIR.name for case in evals)
    assert any(case["expected_skill"] is None for case in evals)
