# Contributing

Contributions should keep skills practical, current, and safe.

## Rules

- Keep each skill self-contained under `skills/<skill-name>/`.
- Keep `SKILL.md` as the portable source of truth.
- Keep `agents/openai.yaml` aligned with the skill when changing trigger behavior.
- Keep reusable automation-run policy in `skills/ceratops-automation-run/` instead of duplicating the same alert, memory, and completion rules across automation prompts.
- Keep shared Ceratops rules in `templates/sections/` plus `templates/skill-sections.json`, keep the universal section minimal, keep GH-only wording in GH-only sections, and keep routine GH best-practice audit work in `skills/ceratops-gh-standards-update/` instead of normal GH task skills.
- Do not add secrets, private endpoints, local machine paths, or org-internal procedures.
- Prefer current official docs over memory when changing GitHub, registry, or agent behavior.
- Add checklist items only when they are durable and broadly useful.
- Do not add boilerplate that is not relevant to these workflows.

## Validation

Run before opening a pull request:

```powershell
python -m pip install .
python .\scripts\validate-skills.py
```

If the change affects workflow behavior, include a short test note in the PR explaining how the skill was exercised or reviewed.
Run `python .\scripts\sync-skill-sections.py` before validation only when shared section source files or `templates/skill-sections.json` changed. Run `python -m ceratops_gh_current_state --help` only when helper-runtime code or helper-runtime claims changed.
The sync step composes the generated shared sections block for every skill automatically.
