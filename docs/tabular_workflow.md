# 表形式データの予測コンペ

CSVの分類・回帰で使う手順。コンペ固有の列名・評価指標・ルールは`competition/overview.md`へ記録する。学習コードは`templates/experiment/`をコピーして実装する。

## 最初に確認すること

- train / test / sample submissionの列・型・IDの一意性・順序、targetの値と欠損を確認する。testにない列とtargetを特徴量へ混ぜない。
- 数値で保存されたカテゴリ、文字列カテゴリ、高cardinality、未知カテゴリ、欠損を区別する。IDはまず除外し、採用するなら意味と効果を別実験で検証する。
- 二値確率の分類では陽性ラベルと0/1対応を明示する。`predict_proba`の列は`classes_`で確認し、常に2列目が目的の陽性とは仮定しない。
- group・時間・重複の構造がなければ、分類は層化分割を候補にする。各評価foldに必要なクラスがあるか確認し、少数クラス件数に応じて分割数を決める。

ラベル提出・対数回帰・時系列・画像の違いは[課題別の評価・提出](task_workflows.md)を参照する。

## 最小baselineから比較する

1. 定数予測を基準に、単純な線形モデルと木系モデルを同じfoldで比較する。まず既存依存のscikit-learnを使い、追加モデルは必要になってから導入する。
2. 欠損補完・スケーリング・カテゴリ変換はfold内でfitし、未知カテゴリの処理を決める。高cardinalityの無制限なone-hot化は避け、小規模実行で時間とメモリを測る。
3. 公式metricでfold別・overall OOFを測り、ID付きOOF・test予測を保存する。二値AUCには`kaggle_agent_template.metrics.binary_roc_auc`を使える（0/1 target、陽性score、最大化）。片方のクラスしかない場合は失敗させ、0.5等で埋めない。
4. AUC用の確率を0/1に閾値化しない。accuracyやlog lossの改善だけで採用せず、公式metricで比較する。fold平均AUCとoverall OOF AUCは別の値として記録する。
5. 特徴量・モデル・元データ追加は1つずつ比較し、何が効いたかと次に転用できる条件を`SESSION_NOTES.md`へ残す。

## 合成データ・元データを使う場合

元データの存在や類似性は、そのまま結合してよい根拠にはならない。出典・利用ルール・target定義・分布差・重複を確認する。
許可された追加データはsource列で区別し、公式trainの固定した検証行で追加なし／ありを比較する。追加データと検証行の重複・同一entityを学習側へ漏らさない。
元データ由来のtarget集約や事前学習モデルも同じ監査対象にする。target encodingは学習行自身のtargetを使わないcross-fittingを行い、validationのtargetを参照しない。
数値の丸め・桁分解など生成過程に由来する特徴は仮説として試し、他コンペで効いたことだけを根拠に一括採用しない。

## 確率CSVの検証

sample submissionのID順へ合わせ、対応する予測を結合する。二値確率提出では次を使う。

```bash
uv run python scripts/validate_submission.py \
  --sample data/raw/sample_submission.csv \
  --submission submit/v001_exp001_baseline/submission.csv \
  --require-numeric --min-value 0 --max-value 1
```

この検査だけでは陽性クラスの取り違えや誤った学習を検出できない。既知入力の推論検査と、保存したOOFからのmetric再計算も行う。

## 適用例（2026-10-04確認）

| コンペ | target / 提出列（ID列は`id`） | 公式metric | 公式Dataが示す元データ |
|---|---|---|---|
| [S6E9: EV購入](https://www.kaggle.com/competitions/playground-series-s6e9/overview) | `Will_Buy_EV`の確率 | ROC AUC・最大化 | [EV adoption Behavior](https://www.kaggle.com/competitions/playground-series-s6e9/data) |
| [S6E10: 航空満足度](https://www.kaggle.com/competitions/playground-series-s6e10/overview) | `satisfaction`の確率 | ROC AUC・最大化 | [Airline satisfaction](https://www.kaggle.com/competitions/playground-series-s6e10/data) |

公式説明は元データに着想を得たデータで、分布は完全には一致しないとしている。実CSVのラベル値・カテゴリ・欠損・重複、外部データの利用条件は開始時に別途確認する。この例は実データでの学習検証済みbaselineではない。
