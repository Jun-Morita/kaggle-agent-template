from __future__ import annotations

import math

import numpy as np
import pytest

from kaggle_agent_template.metrics import (
    accuracy,
    binary_log_loss,
    binary_roc_auc,
    log_rmse,
    mae,
    rmse,
    rmsle,
)


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ([0.1, 0.2, 0.8, 0.9], 1.0),
        ([0.9, 0.8, 0.2, 0.1], 0.0),
        ([0.5, 0.5, 0.5, 0.5], 0.5),
        ([0.1, 0.4, 0.4, 0.8], 0.875),
    ],
)
def test_binary_roc_auc_pairwise_ranking(scores: list[float], expected: float) -> None:
    # Four positive-negative pairs; a tied pair contributes one half.
    assert binary_roc_auc(np.array([0, 0, 1, 1]), np.array(scores)) == expected


@pytest.mark.parametrize(
    ("targets", "scores"),
    [
        ([0, 0], [0.1, 0.2]),
        ([1, 1], [0.1, 0.2]),
        ([], []),
        ([0, 2], [0.1, 0.2]),
        ([0, 1], [0.1]),
        ([0, 1], [[0.1, 0.9], [0.8, 0.2]]),
        ([0, 1], [0.1, float("nan")]),
        ([0, 1], [0.1, float("inf")]),
    ],
)
def test_binary_roc_auc_rejects_invalid_inputs(targets: list, scores: list) -> None:
    with pytest.raises(ValueError):
        binary_roc_auc(np.array(targets), np.array(scores))


def test_rmse_uses_hand_checked_case() -> None:
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 4.0, 3.0])

    assert rmse(y_true, y_pred) == math.sqrt(4.0 / 3.0)


def test_mae_uses_hand_checked_case() -> None:
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([2.0, 2.0, 5.0])

    assert mae(y_true, y_pred) == 1.0


def test_binary_log_loss_uses_hand_checked_case() -> None:
    y_true = np.array([1.0, 0.0])
    y_pred = np.array([0.8, 0.25])
    expected = -0.5 * (math.log(0.8) + math.log(0.75))

    assert binary_log_loss(y_true, y_pred) == expected


@pytest.mark.parametrize(
    ("targets", "predictions", "expected"),
    [([True, False], [True, True], 0.5), ([0, 2, 9], [0, 3, 9], 2 / 3)],
)
def test_accuracy_binary_and_multiclass(targets, predictions, expected) -> None:
    assert accuracy(targets, predictions) == expected


def test_accuracy_rejects_probabilities_and_broadcasting() -> None:
    for targets, predictions in [([0, 1], [0.2, 0.8]), ([0, 1], [[0], [1]]), ([], [])]:
        with pytest.raises(ValueError):
            accuracy(targets, predictions)


def test_log_metrics_use_distinct_transforms() -> None:
    assert rmsle([0, 3], [1, 3]) == pytest.approx(math.log(2) / math.sqrt(2))
    assert log_rmse([1, 4], [2, 4]) == pytest.approx(math.log(2) / math.sqrt(2))
    assert rmsle([1, 4], [2, 4]) != log_rmse([1, 4], [2, 4])
    assert rmsle([0], [0]) == 0


@pytest.mark.parametrize("metric", [rmsle, log_rmse])
@pytest.mark.parametrize(
    ("targets", "predictions"),
    [
        ([], []),
        ([1, 2], [1]),
        ([[1]], [[1]]),
        ([-1], [1]),
        ([1], [-1]),
        ([float("nan")], [1]),
        ([1], [float("inf")]),
    ],
)
def test_log_metrics_reject_invalid_inputs(metric, targets, predictions) -> None:
    with pytest.raises(ValueError):
        metric(targets, predictions)


@pytest.mark.parametrize(("targets", "predictions"), [([0], [1]), ([1], [0])])
def test_log_rmse_requires_positive_values(targets, predictions) -> None:
    with pytest.raises(ValueError):
        log_rmse(targets, predictions)
