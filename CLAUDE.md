# Kaggle Agent Template

このリポジトリは、Claude Code で Kaggle を中心としたデータ分析コンペを進めるための軽量テンプレートです。

## まず読む

作業開始時は次を確認する。

1. `competition/overview.md`
2. `references/knowledge/INDEX.md`
3. `docs/competition_report.md`
4. 最新の `daily_reports/*.md`
5. GPU 利用可否が未確認なら `uv run python scripts/check_gpu.py`
6. `git status --short`

コンペ仕様、評価指標、提出形式、fold 方針が曖昧なまま学習コードを書かない。

## 実装前ガード

`competition/overview.md` の次の項目が空なら、学習コードや提出コードを書かない。まず不足情報を埋める。

- Metric の公式定義とローカル実装方針
- Submission の type、required file、required columns
- Validation の fold method、grouping key、leakage risks
- Rules の external data、pretrained models、internet

## 実行可能なガード

- metric を実装・変更したら `src/kaggle_agent_template/metrics.py` と `tests/` を更新し、`uv run pytest` を実行する。
- 提出CSVを作ったら `scripts/validate_submission.py` で `sample_submission.csv` と突き合わせる。
- 提出したら `submit/SUBMISSIONS.md` に人間向けの要約を書き、`submit/submissions.csv` に機械可読ログを残す。
- Public LB を記録したら `scripts/plot_cv_lb.py` で CV / LB plot と直近傾向を更新する。
- 実験実行時は seed を適用し、`results/run_metadata.json` に git SHA、config hash、主要ライブラリversionを残す。

## 環境とGPU

- Python 実行、lint、notebook 起動は `uv run` 経由を基本にする。
- `uv sync` 後は `src/kaggle_agent_template/` が editable install される。手動の `PYTHONPATH` 追加に依存しない。
- Kaggle のデータ取得、discussion / kernels / submissions の確認、提出は Kaggle CLI または Kaggle 用 skill を使う。ブラウザ操作やスクレイピングに寄せない。
- 環境構築後は `uv run python scripts/check_gpu.py` で GPU 利用可否を確認する。
- GPU が使える場合は、コンペのタスクに合う GPU 対応ライブラリを優先して検討する。
- PyTorch などの重い GPU 依存は、コンペで必要になってから追加する。
- 導入コマンドは、対象ライブラリの公式ドキュメントに基づいて提案する。
- Kaggle Notebook で実行する場合は、accelerator、internet、external data、pretrained model のルールを確認する。

## 進め方

1. `competition/overview.md` にコンペ情報を整理する。
2. notebook、discussion、外部記事から使う知識を `references/knowledge/` に要約し、`INDEX.md` を更新する。
3. `workspace/expNNN_name/` に実験ディレクトリを作る。
4. 最小 baseline で提出ファイルを作り、提出形式が通るかを先に確認する。
5. 信頼できる CV を作り、その後に特徴量やモデルを改善する。
6. 実験ごとに `SESSION_NOTES.md` へ仮説、変更、結果、出典を書く。
7. コンペ理解は `docs/competition_report.md` に日本語で集約する。
8. その日の判断と次アクションを `daily_reports/YYYYMMDD.md` に集約する。
9. 提出したら `submit/SUBMISSIONS.md` に CV / LB / 出典を残す。

## 外部知識の扱い

- Kaggle notebook、discussion、外部記事を読んだら、使えそうな知識を `references/knowledge/` に md で残す。
- raw の HTML、ipynb、スクリーンショット、取得ファイルは `references/raw/` に置く。raw は Git に入れない。
- md には URL、取得日、作者、対象コンペ、要点、使える場面、リスク、実験候補を書く。
- 重要な知識を追加したら `references/knowledge/INDEX.md` も更新する。
- 内容をそのまま長く貼らない。要約し、出典を明記する。
- notebook や discussion 由来のアイデアを実験に使う場合は、`SESSION_NOTES.md` に出典を書く。
- 提出に効いた外部知識は `submit/SUBMISSIONS.md` にも出典を残す。
- rules の external data、pretrained models、internet が不明な場合は、外部データや外部モデルを使うコードを書かない。

## 実験ルール

- 1 実験 1 ディレクトリで管理する。1 notebook だけで完結させない。
- 1 実験 1 仮説を基本にする。
- 実験開始前に採択条件を `SESSION_NOTES.md` に書く。指標や subgroup はコンペに合わせる。
- notebook は EDA や試行錯誤に使う。再実行したい学習・推論は `.py` に移す。
- 実験ディレクトリには `SESSION_NOTES.md`, `config.yaml`, `run.sh`, `train.py` を置く。
- 同じコードでパラメータだけを変える場合は、同じ実験ディレクトリ内の `configs/*.yaml` に分ける。大きく方針が変わる場合だけ新しい実験ディレクトリを作る。
- seed、fold、metric、主要パラメータは config に置く。
- seed は `kaggle_agent_template.repro.set_seed()` で適用する。
- 実験時は `results/run_metadata.json` に git SHA と config hash を残す。
- 初回は高性能モデルより先に、最小 baseline で submission が受理されることを確認する。
- fold はデータ単位を確認してから決める。group や時系列がある場合はランダム KFold にしない。
- fold を作ったら `workspace/folds/` に保存し、使った version を `SESSION_NOTES.md` と config に記録する。
- 前処理の fit は train fold のみで行う。
- target、集約、ランキング、encoding を使う特徴量は `docs/validation_checklist.md` で fold-safe か確認する。
- metric 実装は、小さい手計算ケースや公開 baseline と照合してから実験に使う。
- CV と LB がずれたら、モデルより先に fold、metric、分布差、リークを疑う。
- CV / LB が3件そろったら相関を診断し、以後は Public LB 更新ごとに plot を更新する。直近5件の相関が弱ければ追加提出より先に validation を監査する。少数点の相関だけで自動採否しない。
- 実験詳細は `SESSION_NOTES.md` に残す。`submit/SUBMISSIONS.md` は提出結果と判断の要約だけにする。
- データ、モデル、提出物などの大容量ファイルは Git に入れない。
- 中間モデルと OOF は Git 管理外に置き、anchor、提出再現、比較に不要な成果物は定期的に削除する。

## MCP は任意拡張

MCP は最初から必須にしない。データ理解や notebook 生成を繰り返す段階で必要になったら追加する。

追加する場合は、次の3種類に分ける。

- `data_information`: `competition/overview.md` や軽量なデータ要約を返す。コンペ固有の列説明、join key、target、metric を扱う。
- `analysis_executor`: 小さな分析関数を実行し、結果を `workspace/expNNN_name/results/artifacts/` に保存して path を返す。
- `notebook_writer`: 実験ディレクトリ内の notebook に markdown/code セルを追加する。ただし再利用する処理は `.py` に移す。

MCP の分析結果は、返された artifact を必ず読んでから考察する。コード生成だけで判断しない。

## Kaggle skill は任意拡張

Kaggle コンペで `nvidia-kaggle` plugin / `nvidia-kaggle-skill` が使える場合は、overview、rules、public notebook、discussion、writeup、kernel reproduction、kernel submission、dataset upload の調査や操作に使ってよい。
ただし、Kaggle 以外のコンペでは必須にしない。

project-local skill は `.claude/skills/` に置く。skill を使う前に、対象 skill の `SKILL.md` と参照先 workflow markdown を読む。
第三者 skill に含まれる `scripts/` は外部コードとして扱い、実行前に何をするか確認する。

使う場合も、このリポジトリの運用ルールを優先する。

- 取得した competition overview、rules、metric、submission 情報は `competition/overview.md` に反映する。
- notebook、discussion、writeup 由来の知識は `references/knowledge/` に出典付きで要約し、`INDEX.md` を更新する。
- 再現した kernel や notebook は、実験に使うなら `workspace/expNNN_name/` に整理する。raw 取得物は `references/raw/` に置き、Git に入れない。
- skill が生成した report、cache、download を読んでから判断する。生成物の存在だけで採用しない。
- `KAGGLE_API_TOKEN` は `.env` または環境変数から読む。secret として扱い、表示、ログ出力、commit をしない。
- `.env.example` はサンプルとして管理するが、実トークン入りの `.env` は Git に入れない。
- competition submission、dataset upload、public dataset 作成は外部に影響するため、必ずユーザー承認後に行う。

## 提出前チェック

- 行数、列名、ID 順序、欠損、値域を確認する。
- `uv run python scripts/validate_submission.py --sample data/raw/sample_submission.csv --submission submit/vNNN_expNNN_name/submission.csv` を実行する。
- 提出元の実験、fold、モデル、CV、推論設定を記録する。
- `uv run python scripts/record_submission.py ...` で `submit/submissions.csv` に追記する。
- Public LB が分かったら `uv run python scripts/plot_cv_lb.py` を実行し、CV / LB の関係を確認する。
- CSV 提出は `templates/submit_csv/`、Kaggle kernel 提出は `templates/submit_kernel/` を必要に応じてコピーして使う。
- Kaggle への実提出はユーザー承認後に行う。

## コンペ理解ドキュメント

- `docs/competition_report.md` は人間向けの日本語要約として更新する。
- EDA の細かい出力や実験ログをすべて貼らず、重要な発見、判断、次の実験候補に絞る。
- データ仕様、metric、validation、CV / LB の関係、試したアプローチを最新化する。
- 実験の詳細は `workspace/expNNN_name/SESSION_NOTES.md` に残し、日ごとの判断は `daily_reports/YYYYMMDD.md` に残す。

## Claude Code の振る舞い

- 既存ファイルを読んでから作業する。
- 不明点は仮説を添えて短く確認する。
- 大きな変更では短い方針を出してから実装する。
- 実装後は実行可能な検証を行う。
- 検証できない場合は、理由とリスクを記録する。
- 作業の区切りでは commit を提案する。ただし `git commit` はユーザーが実行する。提案時は staging 対象と commit message 案を示す。
