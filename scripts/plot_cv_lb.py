from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = ["version", "cv", "public_lb"]


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


def plot_cv_lb(records: pd.DataFrame, output_path: Path) -> None:
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

    if len(records) >= 2:
        correlation = records["cv"].corr(records["public_lb"])
        ax.text(
            0.02,
            0.98,
            f"corr = {correlation:.4f}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, default=Path("submit/submissions.csv"))
    parser.add_argument("--output", type=Path, default=Path("docs/figures/cv_lb_correlation.png"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_cv_lb_records(args.log)
    plot_cv_lb(records, args.output)
    print(f"saved: {args.output}")


if __name__ == "__main__":
    main()
