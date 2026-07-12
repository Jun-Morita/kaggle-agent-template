# Validation Checklist

特徴量実装前と CV / LB 乖離時に、該当項目だけを確認する。

## Fold-safe feature engineering

- [ ] scaler、imputer、encoder、feature selector は train fold だけで fit している
- [ ] target encoding、集約、ランキングは validation fold の target や未来情報を参照していない
- [ ] group、entity、time の境界が fold 分割と特徴量生成の両方で守られている
- [ ] OOF 特徴量は各行を学習に使っていないモデルから生成している
- [ ] test 全体を使う教師なし特徴がルールと検証目的に合っている
- [ ] 提出時に再現できない列や処理がない

## Candidate gate

- [ ] 実験前に primary metric の最小改善量を決めた
- [ ] 必要なら fold、時期、subgroup の許容幅を決めた
- [ ] 実行後に採択条件を変更していない

採択条件はコンペ固有である。AUC、LOYO、特定 subgroup などをテンプレート共通の必須条件にはしない。

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
- [ ] 比較や blend に必要な OOF を保持する
- [ ] 再生成できる不採用モデルは削除する
- [ ] 大容量成果物は Git に追加しない

`workspace/**/results/`, `workspace/**/models/`, `workspace/**/oof/` は `.gitignore` の対象である。削除前に、提出再現と比較に必要な成果物を確認する。
