# kaggle-agent-template

Claude Code で Kaggle などのデータ分析コンペを進めるための、軽量テンプレートです。
コンペ仕様、実験結果、提出履歴の置き場所を決め、何を試して何が良かったかを追えるようにします。
学習済みモデルやコンペ固有の学習コードは含みません。

基本は **仕様を整理 → 実験 → 提出を検証 → 結果を記録** の4ステップです。
Kaggle の調査用に NVIDIA の skill、実験用に config・seed・実行情報の記録、提出用に CSV 検証と CV / LB の可視化を用意しています。

## はじめる

Git、[uv](https://docs.astral.sh/uv/getting-started/installation/)、Claude Code を用意します。Python は 3.12 を使います。

### 1. リポジトリと環境を準備する

GitHub の **Use this template** でコンペ用リポジトリを作成して clone するか、次を実行します。
`<competition-name>` は自分のコンペ名に置き換えてください。

```bash
git clone https://github.com/Jun-Morita/kaggle-agent-template.git <competition-name>
cd <competition-name>
uv sync
uv run pytest
```

直接 clone した場合は、`git remote set-url origin <your-repository-url>` で保存先を自分のリポジトリへ変更します。
`uv sync` が仮想環境と依存関係を準備するので、以後の Python コマンドは `uv run ...` で実行します。

### 2. Kaggle 認証を設定する

Kaggle の[API設定](https://www.kaggle.com/settings/api)でトークンを発行します。
初回だけ次を実行し、作成した `.env` の `KAGGLE_API_TOKEN` を実際の値に書き換えます。

```bash
cp .env.example .env
uv run --env-file .env kaggle competitions list
```

`.env` は Git 管理外です。トークンをログや commit に含めないでください。
データ取得前に、Kaggle のコンペページで参加・ルールへの同意を済ませます。Kaggle 以外ではこの手順は不要です。

### 3. Claude Code に最初の作業を頼む

リポジトリのルートで `claude` を起動し、次を渡します。

```text
CLAUDE.md に従って、このコンペの準備をしてください。
コンペURL: <competition-url>
公式情報を確認して competition/overview.md を埋めてください。
Kaggle なら同梱の nvidia-kaggle-skill を使い、認証は .env から読み込んでください。
評価指標、提出形式、validation、外部データ等のルールを整理し、
取得できない情報だけ質問してください。
```

### 既存リポジトリに導入する場合

既存の変更を commit してから、テンプレートを別ディレクトリへ clone し、Claude Code に統合を依頼します。
既存のコード・データ・README・LICENSE を保持し、`CLAUDE.md`、`pyproject.toml`、`.gitignore` は既存設定とマージします。
`.git` や `.venv` はコピーせず、導入後に `uv sync` とテストを実行してください。

## 実験を進める

まず [competition/overview.md](competition/overview.md) に評価指標・提出形式・fold 方針・ルールを整理します。
**CV** は手元での検証スコア、**fold** は学習・検証の分割単位、**LB** はコンペ側のスコアです。

実験のひな形をコピーします。

```bash
cp -r templates/experiment workspace/exp001_baseline
```

Claude Code への依頼例:

```text
competition/overview.md に沿って workspace/exp001_baseline に最小baselineを実装してください。
同じfoldで比較できるようにし、仮説、計算予算、採択条件、結果を SESSION_NOTES.md に残してください。
まず提出ファイルを生成・検証できるところまで進めてください。
```

`train.py` は config の読み込み、seed の設定、実行情報の保存だけを行うひな形です。
コンペに合わせて実装した後、ルートから次で実行できます。

```bash
bash workspace/exp001_baseline/run.sh
```

同じコードのパラメータ違いは `configs/*.yaml`、方針が変わる実験は新しいディレクトリに分けます。
モデル・図表・予測は実験内の `results/` に保存します。詳細は [workspace/README.md](workspace/README.md) を参照してください。

GPU が必要な場合だけ `uv run python scripts/check_gpu.py` で確認し、モデルに合ったライブラリを追加します。PyTorch などの GPU 依存は同梱していません。

## 提出を検証・記録する

提出用のひな形は [CSV提出](templates/submit_csv/README.md) と [Kaggle kernel提出](templates/submit_kernel/README.md) から選び、`submit/v001_exp001_baseline/` にコピーします。

CSV を作成したら、公式の sample submission と比較します。

```bash
uv run python scripts/validate_submission.py \
  --sample data/raw/sample_submission.csv \
  --submission submit/v001_exp001_baseline/submission.csv
```

行数、列名、ID の重複・順序、欠損、予測の無限値を検証します。既定では先頭列を ID とみなします。
複合 ID は `--id-columns id1,id2`、数値予測は `--require-numeric`、値域は `--min-value` / `--max-value` で指定します。
CSV 以外の提出形式は、コンペに合わせて検証を実装してください。

実提出・データアップロードはユーザーの承認後に行います。提出後は次の例の CV / LB を実測値に置き換えて記録します。
LB が未確定なら `--public-lb` を省略し、確定後に同じ version で更新します。

```bash
uv run python scripts/record_submission.py \
  --version v001 \
  --source-experiment exp001_baseline \
  --fold-version v001 \
  --cv 0.1234 \
  --public-lb 0.1200 \
  --file submit/v001_exp001_baseline/submission.csv \
  --config workspace/exp001_baseline/config.yaml

uv run python scripts/plot_cv_lb.py
```

提出値とファイルの SHA-256 は `submit/submissions.csv`、図は `docs/figures/cv_lb_correlation.png` に保存されます。
CV と LB がずれたら、[validation checklist](docs/validation_checklist.md) で fold・metric・リーク・分布差を確認します。

## 何をどこに残すか

数値や実験ログを複数の文書へ転記せず、詳細は元の記録を参照します。

| 保存先 | 内容 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | エージェントの作業ルール |
| [competition/overview.md](competition/overview.md) | コンペ仕様・評価指標・ルール |
| [data/](data/README.md) | 公式データ・加工データ（データ本体は Git 管理外） |
| [workspace/](workspace/README.md) | 実験コード・config・`SESSION_NOTES.md`、固定した fold |
| [references/knowledge/](references/knowledge/README.md) | notebook・discussion 等の出典付き要約 |
| [submit/submissions.csv](submit/submissions.csv) | CV・LB・提出物の記録 |
| [submit/SUBMISSIONS.md](submit/SUBMISSIONS.md) | 重要な提出の採否理由 |
| [docs/competition_report.md](docs/competition_report.md) | コンペ理解・発見・次の実験候補 |
| [daily_reports/](daily_reports/README.md) | その日の判断・未解決事項・次アクション |

生の取得物は `references/raw/`、実験の生成物は `results/` に置き、Git に入れません。

## 同梱の Kaggle skill

NVIDIA の [nvidia-kaggle-skill](https://github.com/NVIDIA/nvidia-kaggle) を `.claude/skills/` に同梱しています。
Claude Code から追加インストールなしで、概要・ルールの取得、公開 notebook・discussion・writeup の調査、kernel の再現・提出、dataset のアップロードに使えます。
Kaggle 以外のコンペには使いません。

調査結果は `competition/overview.md` や `references/knowledge/` に要約します。
kernel 提出の操作履歴 `data/submissions.jsonl` と、CV / LB をまとめる `submit/submissions.csv` は役割が異なります。
同梱版の revision と更新手順は [skill の管理情報](.claude/skills/README.md) を参照してください。

## 開発時の確認

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

commit 時にも lint・format を実行したい場合は、`uv run pre-commit install` で有効にします。
コード・設定・要約・`uv.lock` を Git に残し、データ・モデル・実トークンは含めません。

## License

[MIT](LICENSE)。同梱 skill は [NVIDIA の MIT License](.claude/skills/nvidia-kaggle-skill/LICENSE) に従います。
