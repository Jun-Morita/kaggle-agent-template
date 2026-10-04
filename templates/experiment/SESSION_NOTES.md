# Experiment Notes

仮説・実行結果・判断をここに集約する。該当しない欄は省略可。詳細な検査は`docs/validation_checklist.md`を参照し、指摘と確認結果だけ残す。

## Plan（実行前）

- Experiment / started:
- Parent / anchor experiment and config:
- Hypothesis / mechanism / evidence and sources:
- Change / leakage or rule risk:
- Budget (runtime / cost / max trials) / stop condition:
- Acceptance criterion / stability constraint:
- Selection vs confirmation data / seeds:

## Validation

- Fold file and version / reason (or evaluation conditions):
- Metric implementation / version / sanity check:
- Evaluation source / date / selection bias:
- Audit findings / impact / fix / verification:

## Run Log

smoke / full評価、完了・失敗・中断を区別する。run IDは一意にし、既存の成果物を上書きしない。config・metadata・成果物は参照先を記載する。

| Run ID | Config / metadata | Runtime | Status | Artifacts / failure reason |
|---|---|---|---|---|

- Reproduction command:
- Smoke: loaded artifact / executed path / fallback count / expected output:
- Predictions: OOF / test paths, ID / fold / target / prediction columns:
- Coverage / excluded rows / class order / scale / postprocessing:

## Results

| Run ID | Fold scores | CV mean ± std | Overall OOF score | Delta vs anchor |
|---|---|---|---|---|

同じ条件・metric・集計方法で比較する。CVを使わない課題では表の列をローカル評価に合わせる。

- Error patterns / important subgroup / supporting artifacts:
- Learned / conditions where this may transfer:

## Decision

- Keep / reject / inconclusive and reason:
- Major rejection only: incumbent advantage / independent evidence and source / contradictions:
- Deferred only: missing evidence or measured bottleneck (GPU / CPU / I/O / effort estimate) / revisit condition:
- Next action:
