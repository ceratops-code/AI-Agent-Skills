# Contributing

Contributions should keep skills practical, current, and safe.

## Rules

- Keep each skill self-contained under `skills/<skill-name>/`.
- Keep source `SKILL.md` files as portable delta-only skill definitions; runtime `SKILL.md` files are generated during install.
- Keep `agents/openai.yaml` aligned with the skill when changing trigger behavior.
- Keep reusable automation-run policy in `skills/ceratops-automation-run/` instead of duplicating the same alert, memory, and completion rules across automation prompts.
- Keep shared Ceratops rules in `templates/sections/` plus `templates/skill-sections.json`, keep the universal section minimal, keep GH-only wording in GH-only sections, and keep routine GitHub health contract review in `skills/ceratops-gh-skills-standards-update/` instead of normal GH task skills.
- Do not add secrets, private endpoints, local machine paths, or org-internal procedures.
- Prefer current official docs over memory when changing GitHub, registry, or agent behavior.
- Add checklist items only when they are durable and broadly useful.
- Do not add boilerplate that is not relevant to these workflows.

## Validation

Run before opening a pull request:

```powershell
python .\scripts\validate-skills.py
```

If the change affects workflow behavior, include a short test note in the PR explaining how the skill was exercised or reviewed.
Run `python .\scripts\sync-skill-sections.py` before validation only when shared section source files or `templates/skill-sections.json` changed. Run `python .\scripts\github_pr_readiness.py --help` only when PR-readiness helper code or related skill claims changed.
The sync step validates section assignments and rejects stale source files that still contain generated runtime blocks. `scripts/build-runtime-skills.py` composes runtime `SKILL.md` files and copies declared payloads during install.
