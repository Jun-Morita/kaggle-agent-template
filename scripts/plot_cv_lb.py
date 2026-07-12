from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = ["version", "cv", "public_lb"]
MIN_CORRELATION_RECORDS = 3


def _correlation(records: pd.DataFrame) -> float | None:
    if len(records) < MIN_CORRELATION_RECORDS:
        return None
    correlation = records["cv"].corr(records["public_lb"])
    return None if pd.isna(correlation) else float(correlation)


def summarize_correlations(
    records: pd.DataFrame, recent_window: int = 5
) -> tuple[float | None, float | None]:
    if recent_window < MIN_CORRELATION_RECORDS:
        raise ValueError(f"recent_window must be at least {MIN_CORRELATION_RECORDS}")

    return _correlation(records), _correlation(records.tail(recent_window))


def load_cv_lb_records(log_path: Path) -> pd.DataFrame:
    submissions = pd.read_csv(log_path)
    missing = [column for column in REQUIRED_COLUMNS if column not in submissions.columns]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"missing required columns: {joined}")

    records = submissions.copy()
    records["cv"] = pd.to_numeric(records["cv"], errors="coerce")
    records["public_lb"] = pd.to_numeric(records["public_lb"], errors="coerce")
    records = records.dropna(subset=["cv", "public_lb"]).reset_index(drop=True)
    return records


def plot_cv_lb(
    records: pd.DataFrame,
    output_path: Path,
    recent_window: int = 5,
) -> tuple[float | None, float | None]:
    if records.empty:
        raise ValueError("no rows with both cv and public_lb were found")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(records["cv"], records["public_lb"], color="#2563eb", alpha=0.85)

    for _, row in records.iterrows():
        ax.annotate(
            str(row["version"]),
            (row["cv"], row["public_lb"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )

    ax.set_xlabel("CV")
    ax.set_ylabel("Public LB")
    ax.set_title("CV vs Public LB")
    ax.grid(True, alpha=0.25)

    overall_correlation, recent_correlation = summarize_correlations(records, recent_window)
    labels = []
    if overall_correlation is not None:
        labels.append(f"all corr = {overall_correlation:.4f} (n={len(records)})")
    if recent_correlation is not None and len(records) > recent_window:
        labels.append(f"recent corr = {recent_correlation:.4f} (n={recent_window})")
    if labels:
        ax.text(
            0.02,
            0.98,
            "\n".join(labels),
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    return overall_correlation, recent_correlation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, default=Path("submit/submissions.csv"))
    parser.add_argument("--output", type=Path, default=Path("docs/figures/cv_lb_correlation.png"))
    parser.add_argument("--recent-window", type=int, default=5)
    parser.add_argument("--warn-below", type=float, default=0.3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_cv_lb_records(args.log)
    overall_correlation, recent_correlation = plot_cv_lb(records, args.output, args.recent_window)
    print(f"saved: {args.output}")
    if len(records) < MIN_CORRELATION_RECORDS:
        print(f"diagnostic: insufficient data (need {MIN_CORRELATION_RECORDS} submissions)")
        return
    if overall_correlation is None:
        print("diagnostic: correlation is undefined (CV or Public LB may be constant)")
        return

    recent = "n/a" if recent_correlation is None else f"{recent_correlation:.4f}"
    print(f"correlation: overall={overall_correlation:.4f}, recent={recent}")
    active_correlation = overall_correlation if recent_correlation is None else recent_correlation
    if active_correlation < args.warn_below:
        print(
            "warning: CV/LB correlation is weak; audit validation before increasing "
            "submission frequency"
        )


if __name__ == "__main__":
    main()
