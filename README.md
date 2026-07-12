# kaggle-agent-template

Claude Code で Kaggle などのデータ分析コンペを進めるための、シンプルな運用テンプレートです。

素の Claude Code でもコードは書けます。ただしコンペでは、仕様、評価指標、fold、外部知識、実験結果、提出履歴が散らばると、あとで判断できなくなります。
このテンプレートは、Claude Code が毎回読む場所と、結果を残す場所を固定することで、コンペ運用を破綻しにくくします。

守ることは 4 つだけです。

1. コンペ仕様を先に整理する
2. 外部知識は出典付きで要約する
3. 実験は `workspace/` に分けて残す
4. 結果と判断は日報と提出履歴に書く

対象は、Claude Code を使って Kaggle または同様のデータ分析コンペを進めたい人です。モデルやデータは同梱せず、コンペごとの作業を整理・再現するための土台だけを提供します。

## このテンプレートが役に立つこと

- Claude Code が作業開始時に読むファイルを固定できる
- metric、submission、validation が曖昧なまま実装しないようにできる
- 1 実験 1 ディレクトリで、仮説、config、結果をまとめて残せる
- public notebook や discussion の知識を、raw と要約に分けて管理できる
- 提出形式、metric、提出ログをコードで確認できる
- CV / LB / fold / 提出元を追えるので、良かった実験を再現しやすい
- Git の差分が読みやすくなり、Claude Code が作業状態を誤解しにくい

## Quick Start

事前に Git、[uv](https://docs.astral.sh/uv/getting-started/installation/)、[Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started) をインストールします。Kaggleで使う場合は、アカウント作成とコンペへの参加も必要です。

```bash
git clone https://github.com/Jun-Morita/kaggle-agent-template.git
cd kaggle-agent-template

uv sync
uv run pre-commit install
uv run pytest
claude
```

`uv sync` が仮想環境と依存関係を準備します。以後のPythonコマンドは、仮想環境を手動でactivateせず `uv run ...` で実行できます。

Python 3.12 が未導入の場合:

```bash
uv python install 3.12
uv sync
```

## 最初に Claude Code に頼むこと

Claude Code を開いたら、まず次のように依頼します。

```text
CLAUDE.md を読んで、このリポジトリの運用ルールに従ってください。
参加するコンペのURLは <competition-url> です。
まず competition/overview.md の未記入項目を確認し、不足情報を質問してください。
```

コンペ仕様が埋まってから、baseline や提出コードの作成を依頼します。

## Kaggle 認証（Kaggle のみ）

Kaggle CLIを使う場合は、次のどちらかで認証します。公式CLIが推奨するOAuthではtokenを手元で管理する必要がありません。

```bash
uv run kaggle auth login
```

Claude Code skillや非対話実行でtokenが必要な場合は、Kaggleの設定画面で発行し、`.env.example`からローカル専用の`.env`を作ります。

```bash
cp .env.example .env
```

```dotenv
KAGGLE_API_TOKEN=kgat_your_actual_token_here
```

`.env`は自動でGit管理から除外されます。token方式でKaggle CLIを実行するときは、明示的に読み込みます。

```bash
uv run --env-file .env kaggle competitions list
```

tokenを画面、ログ、commitに含めないでください。認証方式の詳細は[Kaggle CLI公式ドキュメント](https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication)を参照してください。

## 基本ワークフロー

用語に慣れていない場合は、次の意味だけ押さえておけば始められます。

- **fold**: 学習データを学習用と検証用に分ける単位
- **CV**: 手元のデータでモデル性能を測る検証
- **LB**: コンペ側のテストデータで計算されるLeaderboardスコア
- **OOF**: 各行を学習に使っていないモデルから得た予測

### コンペ開始時にやること

1. `CLAUDE.md` を Claude Code に読ませる
2. `competition/overview.md` を埋める
3. `data/README.md` を見て、公式データの置き場所を決める
4. GPUを使う場合は `scripts/check_gpu.py` で利用可否を確認する
5. Kaggle コンペなら Kaggle CLI で API 接続と参加済み状態を確認する
6. metric、submission、validation、rules が埋まってから baseline を作る

Claude Code への依頼例:

```text
competition/overview.md を読んで、学習コードを書く前に不足している項目を整理してください。
特に metric、submission、validation、rules を確認してください。
```

Kaggle CLI の接続確認例:

```bash
uv run kaggle competitions files <competition-slug>
```

`competition-slug`はコンペURL末尾の文字列です。たとえば`https://www.kaggle.com/competitions/titanic`では`titanic`です。

データを取得する場合:

```bash
uv run kaggle competitions download -c <competition-slug> -p data/raw
```

上の例はOAuth認証の場合です。`.env`のtokenを使う場合は、`uv run`の直後に`--env-file .env`を加えます。Kaggle以外のコンペでは、この手順は不要です。

### GPU を使う場合

GPUが必要なモデルを使う場合だけ確認します。

```bash
uv run python scripts/check_gpu.py
```

テンプレート本体にはPyTorchなどの重いGPU依存を含めていません。GPUが見えているのにライブラリから使えない場合は、利用するモデルに合ったGPU対応ライブラリを追加します。

Kaggle Notebookでは、acceleratorに加えてinternet、external data、pretrained modelのルールも確認してください。

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

### 最初の提出経路を確認したいとき

コンペ序盤では、強いモデルより先に「提出が通ること」を確認します。

1. 最小 baseline で `submission.csv` を作る
2. `scripts/validate_submission.py` で `sample_submission.csv` と突き合わせる
3. `submit/v001_exp001_baseline/` に提出物と再現手順を整理する
4. ユーザー承認後に Kaggle CLI で提出する
5. Submission Error が出ないことを確認する
6. `submit/SUBMISSIONS.md` と `submit/submissions.csv` に記録する

Kaggle CLI の提出例:

```bash
uv run kaggle competitions submit \
  -c <competition-slug> \
  -f submit/v001_exp001_baseline/submission.csv \
  -m "v001 baseline smoke submission"
```

Claude Code への依頼例:

```text
最小baselineで提出CSVを作り、scripts/validate_submission.py を通してください。
Kaggle CLIでの実提出コマンドを提示してください。ただし、実提出はまだ実行しないでください。
```

### CV と LB の関係を見たいとき

提出ログに CV と Public LB を記録したら、散布図を更新します。

```bash
uv run python scripts/plot_cv_lb.py \
  --log submit/submissions.csv \
  --output docs/figures/cv_lb_correlation.png
```

3件の提出結果がそろうと相関診断を開始し、5件を超えると直近5件の相関も図に表示します。警告閾値は `--warn-below`、直近件数は `--recent-window` で変更できます。

CV が改善しても LB が悪化する場合は、モデル追加や提出を増やす前に fold、metric 実装、リーク、train/test の分布差、public LB 過適合を疑います。少数の相関係数だけで結論を出さず、`docs/validation_checklist.md` に沿って診断します。

### コンペ理解をまとめたいとき

`docs/competition_report.md` に、コンペ概要、データ仕様、EDA、validation、baseline、試したアプローチを日本語で集約します。
細かい実験ログは `workspace/expNNN_name/SESSION_NOTES.md` に残し、`docs/competition_report.md` は人間が全体像を読み返すための要約にします。

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

## Kaggle 向け任意拡張

このテンプレートは Kaggle 以外のデータ分析コンペでも使えるように、特定サービスの plugin や skill を必須にしません。
Kaggle コンペで、overview、rules、public notebook、discussion、writeup、kernel submission などの調査や操作を効率化したい場合は、NVIDIA の [`nvidia-kaggle`](https://github.com/NVIDIA/nvidia-kaggle) plugin を任意で追加できます。

<details>
<summary>NVIDIA nvidia-kaggle のセットアップを見る</summary>

### Claude Code で使う方法

Claude Code では、主に2つの使い方があります。

#### 方法A: ユーザー環境に plugin として入れる

NVIDIA の案内では、Claude Code で plugin として使う場合は次のコマンドを実行します。

```bash
claude plugin marketplace add https://github.com/NVIDIA/nvidia-kaggle.git
claude plugin install nvidia-kaggle@nvidia-kaggle --scope user
```

`--scope user` はユーザーの Claude Code 環境に plugin を入れる指定です。つまり、このリポジトリに plugin 本体を commit するものではありません。
チームや別マシンで同じ workflow を使う場合は、各ユーザーが自分の Claude Code 環境に plugin を入れます。

Claude Code のバージョンによって plugin コマンドの option が変わる可能性があります。うまく動かない場合は、先に次を確認してください。

```bash
claude plugin --help
claude plugin install --help
```

`--scope user` が使えないバージョンでは、表示された help に従って install してください。

#### 方法B: プロジェクト内に skill として置く

このリポジトリだけで使いたい場合は、Claude Code の project-local skill として `.claude/skills/` に置く方法もあります。
この方式では、skill はこのプロジェクトの一部として管理されます。

```text
.claude/skills/
└─ nvidia-kaggle-skill/
   ├─ SKILL.md
   ├─ kernel-setup.md
   ├─ kernels.md
   ├─ research-brief.md
   ├─ submission.md
   ├─ writeups.md
   └─ scripts/
```

NVIDIA の `skills/nvidia-kaggle-skill/` ディレクトリを使う場合は、`SKILL.md` だけでなく、workflow markdown files と `scripts/` も一緒に置きます。
このテンプレートでは置き場所として `.claude/skills/README.md` だけを用意しています。外部コードを同梱する場合は、更新方法、ライセンス、差分管理を決めてから追加してください。

project-local skill はリポジトリをcloneした人にも共有できます。一方で、第三者のskillには実行スクリプトが含まれることがあるため、追加・更新時は内容を読んでから使います。

### Skill から認証情報を使う場合

project-local skillでtokenを使う場合も、上で作成した`.env`を利用します。Claude Codeにはtokenを表示しないよう明示します。

依頼例:

```text
NVIDIA nvidia-kaggle skill を使って Kaggle の competition overview を取得してください。
KAGGLE_API_TOKEN は .env から読み込んでください。トークン値は表示しないでください。
取得結果は competition/overview.md に要約して反映してください。
```

使う場合も、このリポジトリの記録ルールを優先します。

- competition overview / rules / metric は `competition/overview.md` に反映する
- notebook / discussion / writeup の要約は `references/knowledge/` に出典付きで残す
- kernel や notebook を再現する場合は `workspace/expNNN_name/` か `references/raw/` に整理する
- 提出した場合は `submit/SUBMISSIONS.md` と `submit/submissions.csv` に記録する
- competition submission、dataset upload、public dataset 作成は、必ずユーザー承認後に行う

</details>

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
├─ docs/
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
# GPUを使う場合
uv run python scripts/check_gpu.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## License

[MIT License](LICENSE)
