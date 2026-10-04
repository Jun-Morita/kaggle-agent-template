from __future__ import annotations

import pandas as pd

from scripts.validate_submission import validate_submission


def test_validate_submission_accepts_matching_file(tmp_path) -> None:
    sample_path = tmp_path / "sample_submission.csv"
    submission_path = tmp_path / "submission.csv"

    pd.DataFrame({"id": [1, 2], "target": [0.0, 0.0]}).to_csv(sample_path, index=False)
    pd.DataFrame({"id": [1, 2], "target": [0.2, 0.8]}).to_csv(submission_path, index=False)

    errors = validate_submission(submission_path, sample_path, id_columns=["id"])

    assert errors == []


def test_validate_submission_catches_id_order(tmp_path) -> None:
    sample_path = tmp_path / "sample_submission.csv"
    submission_path = tmp_path / "submission.csv"

    pd.DataFrame({"id": [1, 2], "target": [0.0, 0.0]}).to_csv(sample_path, index=False)
    pd.DataFrame({"id": [2, 1], "target": [0.8, 0.2]}).to_csv(submission_path, index=False)

    errors = validate_submission(submission_path, sample_path, id_columns=["id"])

    assert "id order differs from sample submission" in errors


def test_validate_submission_allows_string_predictions_by_default(tmp_path) -> None:
    sample_path = tmp_path / "sample_submission.csv"
    submission_path = tmp_path / "submission.csv"

    pd.DataFrame({"id": [1, 2], "label": ["cat", "cat"]}).to_csv(sample_path, index=False)
    pd.DataFrame({"id": [1, 2], "label": ["cat", "dog"]}).to_csv(submission_path, index=False)

    errors = validate_submission(submission_path, sample_path, id_columns=["id"])

    assert errors == []


def test_validate_submission_rejects_non_finite_predictions(tmp_path) -> None:
    sample_path = tmp_path / "sample_submission.csv"
    submission_path = tmp_path / "submission.csv"

    pd.DataFrame({"id": [1, 2], "target": [0.0, 0.0]}).to_csv(sample_path, index=False)
    pd.DataFrame({"id": [1, 2], "target": [float("inf"), 0.8]}).to_csv(submission_path, index=False)

    errors = validate_submission(submission_path, sample_path, id_columns=["id"])

    assert "non-finite prediction values found: ['target']" in errors


def test_validate_submission_preserves_identifier_spelling(tmp_path) -> None:
    sample = tmp_path / "sample.csv"
    submission = tmp_path / "submission.csv"
    sample.write_text("id,target\n001,0\n002,0\n")
    submission.write_text("id,target\n1,0.2\n2,0.8\n")
    assert "id order differs from sample submission" in validate_submission(submission, sample)


def test_validate_submission_requires_exact_allowed_labels(tmp_path) -> None:
    sample = tmp_path / "sample.csv"
    submission = tmp_path / "submission.csv"
    for allowed, good, bad in [
        (["True", "False"], ["True", "False"], ["0.8", "false"]),
        ([str(i) for i in range(10)], ["0", "9"], ["1.5", "10"]),
    ]:
        sample.write_text("id,label\n001,0\n002,0\n")
        submission.write_text(f"id,label\n001,{good[0]}\n002,{good[1]}\n")
        assert validate_submission(submission, sample, allowed_values=allowed) == []
        submission.write_text(f"id,label\n001,{bad[0]}\n002,{bad[1]}\n")
        assert "prediction values outside allowed labels: ['label']" in validate_submission(
            submission, sample, allowed_values=allowed
        )
