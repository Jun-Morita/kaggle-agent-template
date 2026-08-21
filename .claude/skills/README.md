# Project Skills

This repository includes NVIDIA's project-local Kaggle skill:

```text
.claude/skills/
└─ nvidia-kaggle-skill/
   ├─ SKILL.md
   ├─ workflow markdown files
   ├─ scripts/
   └─ LICENSE
```

- Upstream: https://github.com/NVIDIA/nvidia-kaggle
- Vendored revision: `2b78cf29f5f30680764292a6592de8d53d4147a8`
- License: MIT; see `nvidia-kaggle-skill/LICENSE`
- Local compatibility changes: removed unsupported `permissions` frontmatter and use the root `uv` environment

Use this skill for Kaggle competitions. Claude Code discovers it from the project automatically; no user-level plugin installation is required. Do not use it for non-Kaggle competitions.

Keep secrets in the root `.env`, never in this directory. Before updating, review the upstream diff and replace the whole skill directory so `SKILL.md`, workflow files, and `scripts/` stay in sync. Preserve the upstream license and update the revision above.

Kernel submission attempts are written to the ignored `data/submissions.jsonl` operational log. The curated experiment, CV, LB, and file-hash record remains `submit/submissions.csv`.

Keep the upstream `SKILL.md`, workflow markdown files, and `scripts/` together.

The skill uses progressive disclosure: `SKILL.md` selects a workflow, and only the linked workflow file should be read for that task. `tests/test_skill_contract.py` checks discovery metadata, linked files, and positive/negative eval coverage without calling Kaggle.

The upstream `evals/evals.json` includes dataset-upload cases. Do not run write-action evals automatically or with live credentials; competition submissions and dataset uploads still require explicit user approval.

Design references: [Anthropic's Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en) and [`anthropics/skills`](https://github.com/anthropics/skills/tree/0a64e398ec6bb34a494f0c347e8ccae53a862f8e/skills/skill-creator). Local tests enforce the documented frontmatter limits, compact `SKILL.md`, linked resources, and positive/negative eval coverage.
