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
- Vendored revision: `410c70b0b076b0d0ca76f10a855e7e337d9bd09b`
- License: MIT; see `nvidia-kaggle-skill/LICENSE`
- Local compatibility changes: removed unsupported `permissions` frontmatter and use the root `uv` environment

Use this skill for Kaggle competitions. Claude Code discovers it from the project automatically; no user-level plugin installation is required. Do not use it for non-Kaggle competitions.

Keep secrets in the root `.env`, never in this directory. Before updating, review the upstream diff and replace the whole skill directory so `SKILL.md`, workflow files, and `scripts/` stay in sync. Preserve the upstream license and update the revision above.

Keep the upstream `SKILL.md`, workflow markdown files, and `scripts/` together.
