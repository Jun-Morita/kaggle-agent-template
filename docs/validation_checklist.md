# Validation Checklist

baselineのfull CV後、特徴量実装前、ensemble時、CV / LB乖離時に該当項目を確認する。
監査では改善案への期待から離れ、「CVが本番より楽になる理由」をコードとデータから探す。
指摘は根拠（ファイル・処理）、CVへの影響、最小修正、確認方法を`SESSION_NOTES.md`へ残す。

## Fixed validation

- [ ] 保存済みfoldをIDで読み込み、欠損・重複・対象行の不一致を検出する
- [ ] 本番の予測対象に応じたリーク単位（entity、重複サンプル、augmentation元等）が学習側と検証側をまたがない
- [ ] 時系列では未来情報が過去の学習・特徴量生成に入らない
- [ ] fold変更時は理由と新versionを残し、anchorも同じ条件で再評価する

## Fold-safe feature engineering

- [ ] scaler、imputer、encoder、feature selector は train fold だけで fit している
- [ ] target encoding、集約、ランキングは validation fold の target や未来情報を参照していない
- [ ] group、entity、time の境界が fold 分割と特徴量生成の両方で守られている
- [ ] OOF 特徴量は各行を学習に使っていないモデルから生成している
- [ ] pseudo-labelや外部学習済みモデルの生成・選択に検証targetが混入していない
- [ ] test 全体を使う教師なし特徴がルールと検証目的に合っている
- [ ] 提出時に再現できない列や処理がない

## Candidate gate

- [ ] 実験前に primary metric の最小改善量を決めた
- [ ] 必要なら fold、時期、subgroup の許容幅を決めた
- [ ] 実行後に採択条件を変更していない

採択条件はコンペ固有である。AUC、LOYO、特定 subgroup などをテンプレート共通の必須条件にはしない。

## OOF / Ensemble

- [ ] 各モデルのID・fold・正解値・検証対象行が一致し、行順だけで連結していない
- [ ] 予測の欠損・無限値・クラス順・尺度・後処理を確認した
- [ ] OOF scoreを保存済み予測から再計算し、fold平均とは区別している
- [ ] best singleと単純平均を比較基準にし、誤差相関だけで採用していない
- [ ] blend重みの選択・stackerのfitと評価を分離し、Public LBで重みを調整していない
- [ ] stackerの評価foldのtargetが、入力特徴を作るbase modelにも入っていない
- [ ] 改善のfold間安定性と推論時間・メモリが提出条件を満たす

OOF上で重みを最適化し、同じOOFで測った改善は探索値として扱う。
通常のOOFをさらに分割しただけでは、stacker学習側の特徴を作るbase modelが評価側targetを見ている場合がある。
stackingの性能確認には、未使用holdoutか、外側fold内でbase modelから作り直すnested CVを使う。
評価を分離できない場合は未確認と記録し、検証済みの改善と混同しない。

## CV / LB divergence

CV と Public LB が3件そろったら診断を始め、以後は LB 更新ごとに直近5件の傾向を確認する。

```bash
uv run python scripts/plot_cv_lb.py
```

相関が弱い、またはCV改善とLB悪化が繰り返される場合は、次の順で確認する。

1. metric の実装と score direction
2. submission と OOF の対応、後処理の差
3. group、time、重複行を考慮した fold
4. preprocessing と feature engineering のリーク
5. fold 別・時期別・重要 subgroup 別の安定性
6. train/test の分布差

分布差が疑わしい場合は、train/test ラベルを予測する小さな adversarial validation を行う。識別性能が高ければ重要特徴と split を調べ、CV が test 分布を再現しているか見直す。

診断結果と validation の変更理由は `docs/competition_report.md` に要約し、個別実験の詳細は `SESSION_NOTES.md` に残す。

## Artifact retention

- [ ] 現行 anchor と提出再現に必要なモデルを保持する
- [ ] 比較やblendに必要なOOF・test予測と、不採用・失敗の記録を保持する
- [ ] 再生成できる不採用モデルは削除する
- [ ] 大容量成果物は Git に追加しない

`workspace/**/results/`, `workspace/**/models/`, `workspace/**/oof/` は `.gitignore` の対象である。削除前に、提出再現と比較に必要な成果物を確認する。
