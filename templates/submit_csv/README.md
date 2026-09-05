# CSV Submission Template

CSV 直接提出用の最小テンプレート。

```text
submit/v001_exp001_baseline/
├─ README.md
├─ predict.py
└─ model/              # git 管理外
```

## Before Submit

- [ ] 元実験、fold、config、CV を記録した
- [ ] 行数が sample submission と一致する
- [ ] required columns が一致する
- [ ] ID の順序が一致する
- [ ] 欠損がない
- [ ] 数値予測に `NaN` / `inf` がない
- [ ] 値域が metric / rules に合っている
- [ ] `scripts/validate_submission.py` を通した
- [ ] 外部知識、外部データ、public notebook を使った場合は出典を記録した
- [ ] `submit/submissions.csv` に提出値とファイルhashを記録した
- [ ] 重要な判断がある場合は `submit/SUBMISSIONS.md` に要約した

## Reproduction

- Code revision / config:
- Environment / hardware / precision:
- Input data / external sources / checkpoints:
- Prediction columns / class order / postprocessing:
- Reproduction command (from repository root):
- Output path / SHA-256:

再現コマンドを実行して提出物を再生成し、形式・保存済みtest予測との対応を確認する。
コンペ固有の確率和・クラス順・実行時間も確認する（汎用CSV検証だけでは検出できない）。
実提出・アップロードはユーザーの承認後に行う。
