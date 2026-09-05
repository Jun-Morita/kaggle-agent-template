# Workspace

実験ディレクトリをここに作る。

```text
workspace/exp001_baseline/
├─ SESSION_NOTES.md
├─ config.yaml
├─ configs/            # パラメータ違いを置く場合だけ
├─ run.sh
├─ train.py
├─ notebook.ipynb      # 必要な場合だけ
└─ results/            # git 管理外
```

1 実験 1 ディレクトリを基本にする。notebook は探索用、`.py` は再実行用、`SESSION_NOTES.md` は判断と結果の記録用。
同じコードでパラメータだけを変える場合は `configs/*.yaml` に分ける。方針が変わる場合だけ新しい実験ディレクトリを作る。

新規実験では `templates/experiment/` をコピーしてから始める。

## 予測と実行記録

コンペ用の学習コードには、完了したfull CVごとに次を保存する処理を実装する。ひな形の`train.py`は予測生成まで実装していない。

- `results/<run-id>/oof.csv`: 行を一意に識別するID（必要なら複合キー）、fold、正解値、予測値
- `results/<run-id>/test.csv`: testのIDと同じ意味・順序の予測列
- `SESSION_NOTES.md`: config・実行metadata・予測への参照、fold別score、CV平均・標準偏差、overall OOF score、実行時間、採否理由

`run-id`はconfig名と実行日時などで一意にし、configの`output.dir`も同じディレクトリへ設定する。再実行で過去の結果を上書きしない。
CSVを基本とし、Parquetを選ぶ場合は対応ライブラリを追加する。多クラス・複数targetでは予測列を増やし、クラス順・予測の尺度・後処理を記録する。

OOF（各行を学習に使っていないモデルの予測）は、検証対象の各IDに過不足なく対応させる。時系列の初期学習区間など未検証行は対象外と明記し、予測を埋めてscore計算に混ぜない。test予測のfold平均等の集約方法も記録する。
失敗・中断したrunはRun Logへ理由を残し、不完全な予測をensembleに使わない。不採用でも再比較に使うOOF・test予測と記録は保持する。
