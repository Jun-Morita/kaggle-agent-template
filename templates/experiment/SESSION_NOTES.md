# Experiment Notes

## Metadata

- Experiment:
- Parent / anchor experiment and config:
- Started:
- Notebook:
- Script:
- Config:
- Fold version:
- Metric version:

## Hypothesis

- Expected mechanism / why the current model misses it:
- Leakage risk:

## Priority and Budget

- Evidence:
- Expected value: high / medium / low
- Estimated runtime / cost / max trials:
- Stop condition:

## Acceptance Gate

- Primary metric minimum improvement:
- Stability constraint (fold / time / group, if needed):
- Fixed before run: yes / no

## Validation Setup

- Fold file:
- Fold reason:
- Metric implementation:
- Metric sanity check:
- Fold-safe feature checklist completed: yes / no
- Audit evidence / CV impact / fix / verification (or no findings):

## Changes

-

## Notebook Notes

- EDA / quick checks:
- Reusable code moved to `.py`: yes / no

## Knowledge Sources

- Used references:
- New notes added to `references/knowledge/`:
- Rule concerns:

## Artifacts

- Artifact paths:
- OOF (`results/<run-id>/oof.csv`; ID, fold, target, prediction):
- Validation coverage / excluded rows and reason:
- Prediction column meaning / class order:
- Test predictions (ID and prediction columns):
- Findings from artifacts:

## Run

```bash
./run.sh
# or
./run.sh configs/variant.yaml
```

- Run metadata (`<output.dir>/run_metadata_*.json`):

## Results

| Run ID | Fold scores | CV mean ± std | Overall OOF score | Delta vs anchor |
|---|---|---|---|---|

同じfold・metric・集計方法で比較する。改善方向はmetricの定義に従う。

## Run Log

| Run ID | Config / metadata | Runtime | Status | Artifacts / failure reason |
|---|---|---|---|---|

smoke / full CVを区別し、失敗・中断も残す。再実行では新しいrun IDを使う。

## Error Analysis

- Checked samples:
- Error patterns:
- Next fix:

## Decision

- Keep / reject / inconclusive:
- Reason:
- Next action:
