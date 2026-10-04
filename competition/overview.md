# Competition Overview

学習コードを書く前に、最低限ここを埋める。`TBD` が残っている項目は実装前に確認する。

## Basic Info

- Competition:
- URL:
- Official rules URL:
- Official data URL:
- Deadline:
- Task type:
- Target:
- Metric:
- Submission limit:

## Data

- Download source:
- Local path:
- Train rows / files:
- Test rows / files:
- Key columns / IDs:

## Metric

- Official definition:
- Local implementation plan:
- Direction: higher is better / lower is better
- Prediction meaning: 確率 / ラベル / 連続値、陽性ラベルと符号化・クラス順
- Sanity check:

## Validation

- Fold method:
- Number of folds:
- Grouping key:
- Stratification key:
- Leakage risks:
- Forecasting only: 系列キー / 時間列 / 予測起点・期間 / 外生変数の利用可能時点
- Fold file:
- CV/LB correlation check:

## Submission

- Type: CSV / Kaggle Notebook / other
- Required file:
- Required columns:
- Required row count:
- ID order:
- Value range:
- Local validation:
- Final selection: 選択期限 / 提出枠数 / 評価・頑健性・多様性の基準

## Format Mapping（CSV / fold の前提が合わない場合のみ）

該当しない既存欄は理由付きで N/A とし、コンペ固有の読み替えをここへ集約する。

- 提出形式: CSV / Notebook / エージェント / その他（Submission の Type と対応）
- 「CV」に当たるローカル評価と固定する比較条件:
- 「Public LB」に当たる本番の信号と性質（ばらつき・収束・最終評価方法）:
- 使わないテンプレート機能と代替手順（metrics.py、CSV検証、fold / OOF保存等）:
- 追加の提出前検査:

## Rules

- External data:
- Pretrained models:
- Internet:
- Runtime / accelerator / memory limits:
- Last checked:
- Notes:
