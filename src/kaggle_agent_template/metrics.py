from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score


def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Fraction of correct labels (not probabilities); higher is better."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    if y_true.ndim != 1 or y_true.shape != y_pred.shape or y_true.size == 0:
        raise ValueError("Labels must be nonempty matching one-dimensional arrays")
    return float(accuracy_score(y_true, y_pred))


def _log_inputs(y_true: np.ndarray, y_pred: np.ndarray, *, allow_zero: bool):
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    if y_true.ndim != 1 or y_true.shape != y_pred.shape or y_true.size == 0:
        raise ValueError("Values must be nonempty matching one-dimensional arrays")
    for values in (y_true, y_pred):
        if not np.isfinite(values).all():
            raise ValueError("Log metrics require finite values")
        if np.any(values < 0) or (not allow_zero and np.any(values == 0)):
            raise ValueError("Values must be nonnegative for RMSLE and positive for log RMSE")
    return y_true, y_pred


def rmsle(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """RMSE of natural log1p values; inputs are nonnegative original-scale values."""
    y_true, y_pred = _log_inputs(y_true, y_pred, allow_zero=True)
    return rmse(np.log1p(y_true), np.log1p(y_pred))


def log_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """RMSE of natural logs; inputs are strictly positive original-scale values."""
    y_true, y_pred = _log_inputs(y_true, y_pred, allow_zero=False)
    return rmse(np.log(y_true), np.log(y_pred))


def binary_roc_auc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """ROC AUC for 0/1 targets and finite scores for class 1; higher is better."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.ndim != 1 or y_pred.ndim != 1 or y_true.shape != y_pred.shape:
        raise ValueError("Targets and scores must be matching one-dimensional arrays")
    if not np.isin(y_true, [0, 1]).all() or not np.array_equal(np.unique(y_true), [0, 1]):
        raise ValueError("ROC AUC requires both classes, encoded as 0 and 1")
    if not np.isfinite(y_pred).all():
        raise ValueError("ROC AUC requires finite scores")
    return float(roc_auc_score(y_true, y_pred))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean(np.abs(y_true - y_pred)))


def binary_log_loss(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-15) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    y_pred = np.clip(y_pred, eps, 1.0 - eps)
    loss = -(y_true * np.log(y_pred) + (1.0 - y_true) * np.log(1.0 - y_pred))
    return float(np.mean(loss))
