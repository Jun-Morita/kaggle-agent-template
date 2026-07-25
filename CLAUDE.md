# Kaggle Agent Template

このリポジトリは、Claude Code で Kaggle を中心としたデータ分析コンペを進めるための軽量テンプレートです。

## 作業開始

最初に`git status --short`を確認する。コンペの分析・実装では`competition/overview.md`も読む。

他の文書はタスクに必要なときだけ読む。

- 作業再開・次アクション: 最新の`daily_reports/*.md`
- 外部知識の調査: `references/knowledge/INDEX.md`と関連note
- 実験の選定・全体戦略: `docs/competition_report.md`と現行anchorの`SESSION_NOTES.md`
- 特徴量実装・CV/LB乖離: `docs/validation_checklist.md`
- GPUモデルの利用: `uv run python scripts/check_gpu.py`

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
- 提出したらCV、LB、提出ファイルhashを `submit/submissions.csv` に記録し、重要な判断だけ `submit/SUBMISSIONS.md` に要約する。
- Public LB を記録したら `scripts/plot_cv_lb.py` で CV / LB plot と直近傾向を更新する。
- 実験実行時は seed を適用し、`results/run_metadata.json` に git SHA、config hash、主要ライブラリversionを残す。

## 環境とGPU

- Python 実行、lint、notebook 起動は `uv run` 経由を基本にする。
- `uv sync` 後は `src/kaggle_agent_template/` が editable install される。手動の `PYTHONPATH` 追加に依存しない。
- Kaggleでは`.claude/skills/nvidia-kaggle-skill/`を使う。必要に応じてKaggle CLIも使う。
- GPUを使う場合だけ、`uv run python scripts/check_gpu.py`で利用可否を確認する。
- GPU が使える場合は、コンペのタスクに合う GPU 対応ライブラリを優先して検討する。
- PyTorch などの重い GPU 依存は、コンペで必要になってから追加する。
- 導入コマンドは、対象ライブラリの公式ドキュメントに基づいて提案する。
- Kaggle Notebook で実行する場合は、accelerator、internet、external data、pretrained model のルールを確認する。

## 進め方

1. `competition/overview.md` にコンペ情報を整理する。
   Kaggleの場合は、先に`KAGGLE_API_TOKEN`と`.env`を確認し、同梱skillで公式情報を取得する。
2. notebook、discussion、外部記事から使う知識を `references/knowledge/` に要約し、`INDEX.md` を更新する。
3. `workspace/expNNN_name/` に実験ディレクトリを作る。
4. 最小 baseline で提出ファイルを作り、提出形式が通るかを先に確認する。
5. 信頼できる CV を作り、その後に特徴量やモデルを改善する。
6. 実験ごとの仮説、変更、結果、出典は `SESSION_NOTES.md` だけに記録する。
7. コンペ理解は `docs/competition_report.md` に日本語で集約し、実験表は重複させない。
8. その日の判断と次アクションだけを `daily_reports/YYYYMMDD.md` に残す。
9. 提出値は `submit/submissions.csv` を正本とし、重要な採否理由だけ `submit/SUBMISSIONS.md` に残す。

## 外部知識の扱い

- Kaggle notebook、discussion、外部記事を読んだら、使えそうな知識を `references/knowledge/` に md で残す。
- raw の HTML、ipynb、スクリーンショット、取得ファイルは `references/raw/` に置く。raw は Git に入れない。
- md には URL、取得日、作者、対象コンペ、要点、使える場面、リスク、実験候補を書く。
- 重要な知識を追加したら `references/knowledge/INDEX.md` も更新する。
- 内容をそのまま長く貼らない。要約し、出典を明記する。
- notebook や discussion 由来のアイデアを実験に使う場合は、`SESSION_NOTES.md` に出典を書く。
- 提出判断に重要な外部知識は `submit/SUBMISSIONS.md` にも出典を残す。
- rules の external data、pretrained models、internet が不明な場合は、外部データや外部モデルを使うコードを書かない。

## 実験ルール

- 比較基準となるanchorを固定し、同じfoldとmetricで比較する。
- 実験候補は「期待効果 × 根拠の強さ ÷ 実装・計算コスト」で優先する。手軽さだけで選ばない。
- 1実験1仮説を基本とし、開始前に根拠、計算予算、停止条件、採択条件を`SESSION_NOTES.md`に書く。
- 平均CVだけでなく、fold間のばらつき、重要subgroup、実行時間、OOFの誤りもanchorと比較する。
- 改善が鈍った系統の微調整を続けず、誤り分析、データ理解、異なるモデル系統へ移る。
- ensembleは単体CVだけでなく、OOF誤差の違いとensemble後のCV改善を確認して採用する。
- 1実験1ディレクトリで管理し、notebookだけで完結させない。
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
- 実験詳細は `SESSION_NOTES.md`、CV/LBと提出物情報は `submit/submissions.csv` を正本にする。`submit/SUBMISSIONS.md` は重要な判断の要約だけにする。
- データ、モデル、提出物などの大容量ファイルは Git に入れない。
- 中間モデルと OOF は Git 管理外に置き、anchor、提出再現、比較に不要な成果物は定期的に削除する。

## Kaggle skill

Kaggleコンペでは、同梱の`.claude/skills/nvidia-kaggle-skill/`をoverview、rules、public notebook、discussion、writeup、kernel reproduction、kernel submission、dataset uploadの調査や操作に使う。Kaggle以外のコンペでは使わない。

Kaggle APIを使う前に、`KAGGLE_API_TOKEN`と`.env`の準備をユーザーへ案内する。未準備なら`.env.example`のコピーとKaggle設定画面でのtoken発行を案内し、準備されるまでAPIを呼ばない。tokenの値は読めても表示しない。

skillが発火したら、`SKILL.md`から依頼に対応するworkflow markdownだけを追加で読む。他のworkflowを先読みしない。
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

- 行数、列名、ID 順序、欠損、有限値、値域を確認する。
- `uv run python scripts/validate_submission.py --sample data/raw/sample_submission.csv --submission submit/vNNN_expNNN_name/submission.csv` を実行する。
- LBで確認する仮説を明確にする。ほぼ同じ予測を繰り返し提出しない。
- 提出元の実験、fold、モデル、CV、推論設定を記録する。
- `uv run python scripts/record_submission.py ...` で `submit/submissions.csv` をversion単位で登録・更新する。
- Public LB が分かったら `uv run python scripts/plot_cv_lb.py` を実行し、CV / LB の関係を確認する。
- CSV 提出は `templates/submit_csv/`、Kaggle kernel 提出は `templates/submit_kernel/` を必要に応じてコピーして使う。
- Kaggle への実提出はユーザー承認後に行う。

## コンペ理解ドキュメント

- `docs/competition_report.md` は人間向けの日本語要約として更新する。
- EDA の細かい出力や実験ログをすべて貼らず、重要な発見、判断、次の実験候補に絞る。
- データ仕様、metric、validation、CV / LB の関係、試したアプローチの要約を最新化する。
- 実験の詳細と数値は `workspace/expNNN_name/SESSION_NOTES.md`、提出値は `submit/submissions.csv` に残す。日報には判断と次アクションだけを書く。

## Claude Code の振る舞い

- 既存ファイルを読んでから作業する。
- 不明点は仮説を添えて短く確認する。
- 大きな変更では短い方針を出してから実装する。
- 実装後は実行可能な検証を行う。
- 検証できない場合は、理由とリスクを記録する。
- ユーザー向け説明と文書は、指定がなければ自然で簡潔な日本語で書く。
- 結論、確認できた事実、その解釈、次の行動を区別し、数値やファイル名を具体的に示す。
- 依頼内容を言い換えて繰り返さない。根拠のない「重要です」「効果的です」「包括的に」などの定型表現を避ける。
- 不自然な直訳より一般的な技術用語を使い、必要な場合だけ初出で短く説明する。
- 作業の区切りでは commit を提案する。ただし `git commit` はユーザーが実行する。提案時は staging 対象と commit message 案を示す。
