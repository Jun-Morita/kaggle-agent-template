# kaggle-agent-template

Claude Code で Kaggle などのデータ分析コンペを進めるための、シンプルな運用テンプレートです。

素の Claude Code でもコードは書けます。ただしコンペでは、仕様、評価指標、fold、外部知識、実験結果、提出履歴が散らばると、あとで判断できなくなります。
このテンプレートは、Claude Code が毎回読む場所と、結果を残す場所を固定することで、コンペ運用を破綻しにくくします。

守ることは 4 つだけです。

1. コンペ仕様を先に整理する
2. 外部知識は出典付きで要約する
3. 実験は `workspace/` に分けて残す
4. 結果と判断は日報と提出履歴に書く

## このテンプレートが役に立つこと

- Claude Code が作業開始時に読むファイルを固定できる
- metric、submission、validation が曖昧なまま実装しないようにできる
- 1 実験 1 ディレクトリで、仮説、config、結果をまとめて残せる
- public notebook や discussion の知識を、raw と要約に分けて管理できる
- 提出形式、metric、提出ログをコードで確認できる
- CV / LB / fold / 提出元を追えるので、良かった実験を再現しやすい
- Git の差分が読みやすくなり、Claude Code が作業状態を誤解しにくい

## Quick Start

```bash
git clone https://github.com/Jun-Morita/kaggle-agent-template.git
cd kaggle-agent-template

uv venv --python 3.12
source .venv/bin/activate
uv sync
pre-commit install
```

Python 3.12 が未導入の場合:

```bash
uv python install 3.12
uv venv --python 3.12
source .venv/bin/activate
uv sync
```

## GPU チェック

環境構築後、まず GPU が使えるか確認します。

```bash
uv run python scripts/check_gpu.py
```

確認すること:

- `nvidia-smi` で GPU と driver が見えるか
- PyTorch を入れている場合、`torch.cuda.is_available()` が `True` か
- GPU が見えているのにライブラリから使えない場合、GPU対応版のMLライブラリを入れ直す必要があるか

テンプレート本体には PyTorch などの重い GPU 依存は入れていません。コンペの種類に合わせて、Claude Code に次のように依頼してください。

```text
scripts/check_gpu.py の結果を見て、このコンペで使うモデルに必要なGPU対応ライブラリを提案してください。
導入コマンドは公式ドキュメントに基づいてください。
```

Kaggle Notebook で学習や推論を行う場合も、GPU accelerator が有効か、コンペルールで internet / external data / pretrained model が許可されているかを確認します。

## 最初に Claude Code に頼むこと

Claude Code を開いたら、まず次のように依頼します。

```text
CLAUDE.md を読んで、このリポジトリの運用ルールに従ってください。
まず competition/overview.md の未記入項目を確認し、不足情報を質問してください。
```

コンペ仕様が埋まってから、baseline や提出コードの作成を依頼します。

## 迷ったらここ

### コンペ開始時にやること

1. `CLAUDE.md` を Claude Code に読ませる
2. `competition/overview.md` を埋める
3. `data/README.md` を見て、公式データの置き場所を決める
4. `scripts/check_gpu.py` で GPU 利用可否を確認する
5. metric、submission、validation、rules が埋まってから baseline を作る

Claude Code への依頼例:

```text
competition/overview.md を読んで、学習コードを書く前に不足している項目を整理してください。
特に metric、submission、validation、rules を確認してください。
```

### 良い外部情報を見つけたとき

1. raw の HTML、ipynb、スクリーンショットなどは `references/raw/` に保存する
2. 使えそうな知識だけを `references/knowledge/` に md で要約する
3. `references/knowledge/INDEX.md` を更新する
4. URL、取得日、作者、要点、リスク、実験候補を書く
5. 実験に使ったら `SESSION_NOTES.md` に出典を書く
6. 提出に効いたら `submit/SUBMISSIONS.md` にも出典を書く

Claude Code への依頼例:

```text
このnotebook/discussionの要点を references/knowledge/ に出典付きで要約してください。
このコンペで使える実験候補と、leakage / rules 上のリスクも分けて書いてください。
```

### EDA や仮説検証をしたいとき

1. `templates/experiment/` を `workspace/expNNN_name/` にコピーする
2. `SESSION_NOTES.md` に仮説を書く
3. notebook は探索用に使う
4. 再実行したい処理は `train.py` や別の `.py` に移す
5. metric を実装・変更したら `tests/` に手計算ケースを追加する
6. 図表、OOF、モデルなどの生成物は `results/` に置く
7. 結果、判断、次アクションを `SESSION_NOTES.md` に残す

```bash
cp -r templates/experiment workspace/exp001_baseline
```

Claude Code への依頼例:

```text
templates/experiment をもとに workspace/exp001_baseline を作ってください。
まずはデータ確認と最小baselineを行い、仮説、変更、結果を SESSION_NOTES.md に残してください。
```

同じコードでパラメータだけを変える場合は、新しい実験ディレクトリを増やさず、同じディレクトリ内の `configs/*.yaml` に分けます。
方針が変わる場合だけ、新しい `workspace/expNNN_name/` を作ります。

metric を追加・変更したら、必ずテストを通します。

```bash
uv run pytest
```

### その日の取り組みをまとめたいとき

1. `templates/daily_report.md` を `daily_reports/YYYYMMDD.md` にコピーする
2. 今日動かした実験、CV / LB、分かったこと、判断を書く
3. 外部情報から得た知識があれば `Knowledge / References` に書く
4. 明日やることを `Next` にチェックリストで残す
5. その日の区切りで commit 対象と commit message を Claude Code に提案させる

Claude Code への依頼例:

```text
今日の作業を daily_reports/YYYYMMDD.md にまとめてください。
各実験のCV/LB、採用した判断、明日のNext Actionを整理してください。
最後に git status --short を見て、commit対象とcommit message案を出してください。
```

## 提出

提出形式が決まったら、必要に応じて `templates/submit_csv/` または `templates/submit_kernel/` を `submit/vNNN_expNNN_name/` にコピーします。

提出前に必ず確認します。

- 行数、列名、ID 順序、欠損、値域、重複
- 推論に使った実験、fold、model、config
- CV と LB
- 外部知識や外部データを使った場合の出典とルール適合

CSV提出では、まず `sample_submission.csv` と突き合わせます。

```bash
uv run python scripts/validate_submission.py \
  --sample data/raw/sample_submission.csv \
  --submission submit/v001_exp001_baseline/submission.csv
```

提出したら、人間向けの要約は `submit/SUBMISSIONS.md` に書き、機械可読ログは `submit/submissions.csv` に追記します。

```bash
uv run python scripts/record_submission.py \
  --version v001 \
  --source-experiment exp001_baseline \
  --fold-version v001 \
  --cv 0.1234 \
  --public-lb 0.1200 \
  --file submit/v001_exp001_baseline/submission.csv \
  --config workspace/exp001_baseline/config.yaml \
  --note "baseline"
```

Kaggle への実アップロードは Claude Code が勝手に行わず、ユーザー承認後に行います。

Claude Code への依頼例:

```text
提出前チェックを行い、submit/SUBMISSIONS.md に記録してください。
実アップロードはまだしないでください。
```

## MCP

MCP は任意拡張です。最初から必須にしません。
必要になったら、データ情報を返す `data_information`、小さな分析を実行する `analysis_executor`、notebook にセルを追加する `notebook_writer` の3種類に分けて追加します。

## Git 運用

Claude Code は作業開始時に `git status --short` を見て状況を把握します。未コミットの差分が多いと、どこまでが完了済みで、どこからが作業中か判断しにくくなります。

- 小さな区切りで commit する
- commit message には実験番号や変更意図を書く
- 大きな生成物、データ、モデル、提出ファイルは commit しない
- `uv.lock` が生成されたら commit する
- Claude Code は commit を提案し、実行はユーザーが行う

例:

```bash
git add CLAUDE.md README.md
git commit -m "docs: clarify experiment workflow for Claude Code"

git add workspace/exp001_baseline
git commit -m "exp001: add baseline training script"

git add submit/SUBMISSIONS.md submit/v001_exp001_baseline
git commit -m "submit: record v001 baseline submission"
```

## 構成

```text
kaggle-agent-template/
├─ CLAUDE.md
├─ competition/overview.md
├─ data/
├─ daily_reports/
├─ references/
├─ scripts/
├─ src/
├─ tests/
├─ workspace/
├─ submit/SUBMISSIONS.md
└─ templates/
```

```text
references/
├─ knowledge/
│  ├─ INDEX.md
│  ├─ notebooks.md
│  ├─ discussions.md
│  └─ external_ideas.md
└─ raw/                 # git 管理外
```

```text
workspace/exp001_baseline/
├─ SESSION_NOTES.md
├─ config.yaml
├─ configs/            # パラメータ違いを置く場合だけ
├─ run.sh
├─ train.py
├─ notebook.ipynb      # 必要な場合だけ
└─ results/            # git 管理外
   └─ artifacts/       # MCP や EDA の出力
```

```text
workspace/folds/
└─ v001/
   ├─ folds.csv
   └─ README.md
```

## Check

```bash
uv run python --version
uv run python scripts/check_gpu.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```
