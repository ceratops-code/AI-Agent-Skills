# Contributing

Contributions should keep skills practical, current, and safe.

## Rules

- Keep each skill self-contained under `skills/<skill-name>/`.
- Keep `SKILL.md` as the portable source of truth.
- Keep `agents/openai.yaml` aligned with the skill when changing trigger behavior.
- Keep reusable automation-run policy in `skills/ceratops-automation-run/` instead of duplicating the same alert, memory, and completion rules across automation prompts.
- Keep shared Ceratops core rules in `templates/common-core.md`, keep GH-only wording inline there only when the rule truly applies only to GitHub or registry tasks, and keep routine GH best-practice refresh work in `skills/ceratops-gh-best-practice-update/` instead of normal GH task skills.
- Do not add secrets, private endpoints, local machine paths, or org-internal procedures.
- Prefer current official docs over memory when changing GitHub, registry, or agent behavior.
- Add checklist items only when they are durable and broadly useful.
- Do not add boilerplate that is not relevant to these workflows.

## Validation

Run before opening a pull request:

```powershell
python -m pip install .
python .\scripts\sync-skill-core.py
python .\scripts\validate-skills.py
python -m ceratops_gh_runtime --help
```

If the change affects workflow behavior, include a short test note in the PR explaining how the skill was exercised or reviewed.
The sync step applies the shared core template to every skill automatically.
