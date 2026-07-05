# Project Skills

Project-local Claude Code skills can be placed here.

```text
.claude/skills/
└─ skill-name/
   ├─ SKILL.md
   ├─ scripts/
   └─ references/
```

Use this directory for skills that should travel with this repository.
Do not store secrets here. Put local secrets in `.env`.

For NVIDIA `nvidia-kaggle-skill`, copy or vendor the upstream skill directory as:

```text
.claude/skills/nvidia-kaggle-skill/
```

Keep the upstream `SKILL.md`, workflow markdown files, and `scripts/` together.
