from __future__ import annotations

import pandas as pd
import pytest

from scripts.plot_cv_lb import load_cv_lb_records


def test_load_cv_lb_records_keeps_numeric_rows(tmp_path) -> None:
    log_path = tmp_path / "submissions.csv"
    pd.DataFrame(
        {
            "version": ["v001", "v002", "v003"],
            "cv": ["0.60", "", "0.55"],
            "public_lb": ["0.58", "0.57", "0.54"],
        }
    ).to_csv(log_path, index=False)

    records = load_cv_lb_records(log_path)

    assert list(records["version"]) == ["v001", "v003"]
    assert list(records["cv"]) == [0.60, 0.55]
    assert list(records["public_lb"]) == [0.58, 0.54]


def test_load_cv_lb_records_requires_columns(tmp_path) -> None:
    log_path = tmp_path / "submissions.csv"
    pd.DataFrame({"version": ["v001"], "cv": [0.1]}).to_csv(log_path, index=False)

    with pytest.raises(ValueError, match="missing required columns: public_lb"):
        load_cv_lb_records(log_path)
