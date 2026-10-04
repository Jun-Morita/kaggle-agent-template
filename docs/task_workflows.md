# 課題に合わせた評価・提出

`competition/overview.md`に予測対象・単位・出力形式を記録してから、該当する節だけ使う。表形式の前処理は[tabular_workflow.md](tabular_workflow.md)、共通監査は[validation_checklist.md](validation_checklist.md)を参照する。

## 指標と提出値を分ける

| 課題 | ローカル指標 | 提出する値 |
|---|---|---|
| 二値確率 | `binary_roc_auc`・最大化 | 指定された陽性クラスの確率 |
| 二値・多クラス分類 | `accuracy`・最大化 | boolean、整数、文字列など公式指定のラベル |
| 非負回帰 | `rmsle`・最小化 | 元スケールの非負値。指標内部で`log1p`を取る |
| 正値の対数回帰 | `log_rmse`・最小化 | 元スケールの正値。指標内部で自然対数`log`を取る |

関数は`kaggle_agent_template.metrics`にある。RMSLEとlog RMSEは別の指標であり、ログ変換済みの値を二重に変換しない。`log`で学習したら`exp`、`log1p`なら`expm1`で戻して提出する。負値・ゼロのクリップが必要なら理由と閾値を決め、CVにも同じ処理を適用する。指標関数は不正な値を黙って補正しない。
分類の閾値調整は選別用データで行い、確認用データで再評価する。多クラスは`argmax`の位置を保存したクラス順へ戻す。確率と最終ラベルの両方を残すと、学習なしで後処理を比較できる。

## 時系列・複数系列の予測

- 系列キー・時間列・予測起点・予測期間・利用可能な外生変数を定義する。testの日付範囲と欠損日を実ファイルで確認し、日付で切った複数の過去区間で同じ予測期間を再現する。行のランダム分割や行数だけの分割は使わない。
- 曜日別の過去平均や季節naiveを基準にする。店舗×商品などの系列内で日付を整列し、欠損日をゼロ売上と同一視しない。
- lag・rollingは予測時点で利用可能なtargetだけから作る。複数日を一括予測する評価では、検証期間の実売上を次の日のlagへ入れない。再帰予測なら自身の予測で更新し、直接予測ならhorizonごとの利用可能情報を守る。
- 販促・祝日など事前に分かる値と、取引数など事後に分かる値を分ける。補間・外部表の結合にも利用可能時点を適用し、結合で行が増えないことを検査する。
- 重なるbacktestでは同じIDに複数の予測が出る。`origin, horizon, ID, target, prediction`で保存し、通常の1行1OOFと区別する。評価対象・集計方法を固定して全体と系列別を確認する。

## グループのある分類・小規模回帰

- 家族・旅行グループ・地域などの共有構造を調べ、本番が既知groupの別行か未知groupかを確認する。分割の選択理由を残し、必要なら通常分割とgroup分割の感度を比較する。
- groupをまたぐtarget伝播やtarget集約はリークを監査する。欠損は「不明」と「設備が存在しない」等をデータ辞書で区別する。
- 小規模回帰は正則化した線形モデルと木系から始める。外れ値を除く場合は根拠を残し、検証行は都合よく除外しない。target変換・特徴量追加を別々に比較する。

## CSVに格納された画像・多クラス分類

- 列名の番号で画素順を復元する（`pixel1, pixel10, pixel2`の辞書順にしない）。画像の縦横・channel・値域を確認し、何枚か表示してreshapeを検査する。
- ラベルとIDを画素に含めず、層化分割を基準に重複画像・派生画像の漏洩を調べる。augmentationは分割後の学習側だけに適用する。
- 正規化・reshape・クラス順を学習側と提出側で共有する。augmentationが数字の意味を変えないか確認する。
- 線形分類器等の小さなbaselineから始め、CNNやGPU依存は必要時に追加する。混同行列と誤分類画像から次の仮説を選ぶ。
- 入力にIDがなければ行の対応を固定し、提出IDは公式仕様・sample submissionに合わせる。外部MNIST等の利用はルールと重複を確認し、公開ラベルとの照合で検証・testを汚染しない。

## 公式仕様への適用例（2026-10-04確認）

| コンペ | 指標 / CSV列 | 確認する点 |
|---|---|---|
| [Store Sales](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/overview) | RMSLE / `id,sales` | [データ](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data)：`store_nbr × family`の日次系列。test全期間を再現し、売上の小数を丸めない |
| [Spaceship Titanic](https://www.kaggle.com/competitions/spaceship-titanic/overview) | accuracy / `PassengerId,Transported` | [データ](https://www.kaggle.com/competitions/spaceship-titanic/data)：IDの`gggg_pp`は旅行group。`True` / `False`を提出 |
| [House Prices](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview) | 対数のRMSE / `Id,SalePrice` | [データ](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data)：`data_description.txt`で欠損の意味を確認。提出は価格に戻す |
| [Digit Recognizer](https://www.kaggle.com/competitions/digit-recognizer/overview) | accuracy / `ImageId,Label` | [データ](https://www.kaggle.com/competitions/digit-recognizer/data)：28×28、784画素、0〜255。testの行順に1始まりのID、ラベルは0〜9 |

CSV検証の共通引数`--sample ... --submission ...`に、形式に応じて以下を追加する。

- Store Sales：`--require-numeric --min-value 0`
- Spaceship Titanic：`--allowed-values True False`
- House Prices：`--require-numeric --min-value 0`に加え、推論コードで厳密に正値であることを検査（0は不可）
- Digit Recognizer：`--allowed-values 0 1 2 3 4 5 6 7 8 9`

`--allowed-values`はCSVの文字列を厳密に照合するため、`1.0`と`1`は別扱い。IDの先頭ゼロも保持して検査する。これらは公式説明に基づく適用例であり、実データで学習検証済みのbaselineではない。
