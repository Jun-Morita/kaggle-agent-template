# Kaggle Kernel Submission Template

Kaggle kernel 提出用の最小テンプレート。`.py` を正本にして Kaggle script kernel として扱う。

```text
submit/v001_exp001_baseline/
├─ README.md
├─ inference.py
├─ kernel-metadata.json
└─ model/                  # git 管理外
```

## Before Submit

- [ ] CSV Competition か Code Competition か確認した
- [ ] Kaggle kernel の internet 設定を確認した
- [ ] input dataset と model path を確認した
- [ ] `submission.csv` の形式 assert を入れた
- [ ] 提出環境で、梱包したコード・モデル・設定を使い、保存済みセル状態に頼らず最初から最後まで実行した
- [ ] 提出時のinternet・accelerator・入力条件で、必要な資産のロードと出力を確認した
- [ ] 提出全量の実行時間・最大メモリ使用量が制限内であることを確認した（小規模smokeだけでは完了としない）
- [ ] `scripts/validate_submission.py` を通した
- [ ] 外部知識、外部データ、public notebook を使った場合は出典を記録した
- [ ] `submit/submissions.csv` に提出値と提出物情報を記録した
- [ ] 重要な判断がある場合は `submit/SUBMISSIONS.md` に要約した

## Reproduction

- Code revision / config:
- Environment / hardware / precision:
- Submission environment check: passed / failed / not run; date / kernel version / log:
- Runtime / peak memory / limits (unmeasured items and reason):
- Input data / external sources / checkpoints:
- Prediction columns / class order / postprocessing:
- Reproduction command (from repository root):
- Output path / SHA-256:

ローカルの`uv.lock`と提出環境のPython・ライブラリ・CUDA等は一致するとは限らない。提出環境で必要な依存と資産を確認する。
再現コマンドで出力を生成し、形式・保存済みtest予測との対応を確認する。提出環境で未実施・失敗・計測不能なら理由と未確認事項を残し、ローカル実行の成功と区別する。
コンペ固有の確率和・クラス順・実行時間も確認する（汎用CSV検証だけでは検出できない）。
実提出・アップロードはユーザーの承認後に行う。
