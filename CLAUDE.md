# Kaggle Agent Template

コンパクトで、実験の再現と学びにつながる運用を保つ。共通ルールを増やす前に、既存の記録・検査で扱えないか確認する。

## 作業開始

- `git status --short`で既存の変更を確認する。コンペの分析・実装では`competition/overview.md`を読む。
- 学習・提出コードを書く前に、公式metricと実装方針、提出形式、validation、外部データ・モデル・internetのルールを明確にする。該当しない欄は理由付きでN/Aとする。
- CSV / foldの前提が合わない場合は`competition/overview.md`の`Format Mapping`で必須欄・コマンド・成果物を読み替える。コンペ固有の例外は本書に追記しない。
- 文書は必要なものの該当節だけ読む。全項目を毎回埋めることを目的にしない。

| 作業 | 参照先 |
|---|---|
| 再開・実験選定 | 現行anchorの`SESSION_NOTES.md`、必要なら最新の日報・`docs/competition_report.md` |
| 課題別の評価・提出 | `docs/task_workflows.md`（表形式の前処理は`docs/tabular_workflow.md`） |
| baseline監査・特徴量・ensemble・採否判断・CV/LB乖離 | `docs/validation_checklist.md` |
| 外部知識の調査 | `references/knowledge/INDEX.md`と関連note |
| 実験構成・予測保存 | `workspace/README.md` |

## 環境と検証

- `uv sync`で環境を準備し、Python・lint・notebookは`uv run`経由で実行する。依存追加は必要時だけ行う。
- GPUが必要なら`uv run python scripts/check_gpu.py`で確認する。モデル選択は計算予算に合わせ、GPUライブラリの導入は公式手順に従う。
- metricを変更したら`src/kaggle_agent_template/metrics.py`と手計算ケース等のテストを更新し、`uv run pytest`で確認する。
- フォールバックを持つコードは、ロードした成果物・実行経路・発生件数を検査する。通常のsmokeでは予期しないフォールバックを0件とし、意図した代替処理は別ケースで検査する。
- 実装後は変更に合った検証を行う。検証できなければ理由と未確認事項を報告する。チェックリストや指示文だけでは動作検証にならない。

## 実験の進め方

1. 最小baselineで評価から提出物の生成・検証まで通す。実提出はユーザー承認後に行う。
2. 比較基準のanchorとfold・metricを固定する。分割はgroup・時系列・重複を考慮し、`workspace/folds/`にversion付きで保存する。変更時は理由を残し、anchorも再評価する。
3. 1実験1仮説を基本に、根拠・予算・停止条件・採択条件を先に記録する。小さなsmokeからfull評価へ進め、前処理は学習側だけでfitする。
4. 同じ条件でanchorと直接比較する。fold別score・平均と標準偏差・overall OOF・実行時間・重要subgroupを区別し、誤り分析から採否と次の仮説を決める。
5. 失敗・中断もRun Logに残す。不完全な結果を完成した評価として比較せず、再利用できる知見と成立条件を短く書く。

- 実験は`templates/experiment/`から`workspace/expNNN_name/`へ作る。同じコードのパラメータ違いは`configs/*.yaml`、方針変更は新しい実験に分ける。再実行する処理はnotebookから`.py`へ移す。
- seed・fold・metric・主要パラメータはconfigに置く。`repro.set_seed()`と`write_run_metadata()`でseed、git SHA・dirty state・config hash・ライブラリversionを記録する。
- 完了した評価の予測は`workspace/README.md`に従いrunごとに保存する。データ・モデル・生の取得物・生成物はGit管理外に置き、anchor・比較・提出再現に必要な成果物は保持する。
- baseline確立後は現コンペ・類似コンペの公開解法から転用条件を調べ、期待効果・根拠・コストで候補を絞る。特徴量はfamily単位で効果を切り分け、HPOは試行数・時間を制限する。停滞時は同系統の微調整を続けず、誤り分析と候補の見直しを行う。

## 判断で守ること

- Public LBを特徴量・HPO・blend重みの主要な選択基準にしない。候補や重みの選別と採否の確認を分け、探索値を検証済みの改善と混同しない。
- 自作評価器は本番の最初の信号が得られた時点で、比較可能なsubgroup・相手・時期ごとに照合する。ずれの量・不確実性・適用範囲を全体レポートへ残し、照合前はその評価だけで大枠を確定しない。
- 大枠の変更を棄却する前に、現行案に有利な評価条件、自作評価を通らない証拠と出典、矛盾と理由を記録する。証拠不足は保留とし、予算による見送りと性能上の棄却を区別する。
- 予算不足はGPU・CPU・I/Oの計測や工数の見積根拠から律速を調べ、未計測なら推測と明記する。保留案には再検討条件を残す。
- ensembleはbest single・単純平均に対する改善、安定性、推論コストで判断する。OOF対応とstackingのリーク監査はチェックリストに従う。
- CV/LBの順位や相関が安定していても、水準のずれを見逃さない。偏り・自作評価の仮定・時間変化も調べ、矛盾があれば件数を待たずに監査する。

## 記録先と外部情報

| 内容 | 正本 |
|---|---|
| コンペ仕様・形式の読み替え | `competition/overview.md` |
| 仮説・run・結果・採否 | 実験の`SESSION_NOTES.md`（未実験案は全体レポートの候補欄） |
| CV・LB・提出物hash | `submit/submissions.csv`。重要な採否理由だけ`submit/SUBMISSIONS.md` |
| 全体の発見・戦略・次の候補 | `docs/competition_report.md`。仕様や実験値は転記せず元へリンク |
| 外部知識 | `references/knowledge/`。URL・取得日・作者・要点・適用条件・リスクを要約しINDEXを更新 |
| 作業の引き継ぎ | 必要時に`daily_reports/YYYYMMDD.md`。判断・未解決事項・次アクションだけ |

- Kaggleの調査・操作は同梱の`.claude/skills/nvidia-kaggle-skill/`を使う。`SKILL.md`から必要なworkflowだけ読み、外部スクリプトは内容を確認して実行する。Kaggle以外には使わない。
- API利用前に`KAGGLE_API_TOKEN`の設定を確認する。未設定なら`.env.example`とKaggle設定画面を案内する。tokenは環境変数か`.env`から読み、表示・ログ出力・commitしない。
- 調査結果・取得物は内容を確認して採用する。rawは`references/raw/`、実験に使った出典は実験メモへ残す。skillの`data/submissions.jsonl`は操作履歴であり、提出値の正本とは分ける。

## 提出

- CSV / kernel用ひな形を必要に応じて使う。CSVは`scripts/validate_submission.py`で公式sampleと照合し、ラベル・値域等の追加条件は課題別ガイドを参照する。
- 提出用READMEに元実験・config・環境・入力・checkpoint・推論設定・再現コマンドを残す。提出物を再生成し、学習側との推論の一致・実行制限・ルール適合を確認する。
- 提出で確認する仮説を明確にする。最終選択の期限と基準は再検証時間を残してoverviewへ記録し、Public LBだけで選ばない。複数枠では異なる弱点を持つ検証済み候補を検討する。
- 実提出・dataset upload・public dataset作成はユーザー承認後に行う。
- `scripts/record_submission.py`で提出記録を更新し、LB判明時に`scripts/plot_cv_lb.py`で関係を確認する。少数点の相関だけで自動採否しない。

## 伝え方とcommit

- 既存ファイルを読み、大きな変更では短く方針を伝えてから作業する。不明点は仮説を添えて確認する。
- 説明と文書は簡潔な日本語で、結論・変更・理由・検証を具体的に述べる。事実と推測を区別し、未確認の効果を断定しない。
- 依頼の言い換え、過剰な称賛、誇張、定型句、造語、不自然な直訳を避ける。「堅牢性を向上」より「提出CSVの欠損値を検出」のように対象と動作を書く。
- 作業の区切りでstaging対象とcommit案を示す。`git commit`はユーザーが実行する。
- commit messageは短い英文1行。本文・署名を付けず、接頭辞と動詞で差分を表す。例：`docs: simplify experiment notes`。`update files`など曖昧な表現は避ける。
