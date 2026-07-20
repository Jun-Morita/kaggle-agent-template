# Submissions

| Version | Decision | Summary | References |
|---|---|---|---|

`SUBMISSIONS.md` は重要な提出判断だけを残す人間向けの要約です。CV、LB、提出ファイル、SHA-256など、比較と再現に使う値の正本は `submit/submissions.csv` です。

## Rules

- 提出物は `submit/vNNN_expNNN_name/` に作る。
- 元実験、fold、CV/LB、提出ファイルhashは `scripts/record_submission.py` で記録する。
- 外部知識、外部データ、public notebook を使った場合は出典を記録する。
- 提出前に `scripts/validate_submission.py` で行数、列名、欠損、値域、ID の順序を確認する。
- 提出後に `scripts/record_submission.py` で `submit/submissions.csv` をversion単位で登録する。同じversionで再実行すると既存行を更新する。
- Public LB を記録したら `scripts/plot_cv_lb.py` で `docs/figures/cv_lb_correlation.png` を更新する。
- 実験の詳細は元実験の `SESSION_NOTES.md` に残し、ここには重要な採否理由だけを書く。
- 実アップロードはユーザー承認後に行う。
