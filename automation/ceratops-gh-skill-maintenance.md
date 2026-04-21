# Ceratops GH Skill Maintenance

## Scope

- Repo: `codex-skills`
- Skills: `skills/ceratops-gh-*`
- Shared GH-maintenance files: `templates/common-core-gh.md`, `scripts/sync-skill-core.py`, `scripts/validate-skills.py`
- Repo docs to keep aligned when stale: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`

## Review Targets

- Current official GitHub docs, `gh` help, and live GitHub metadata for the settings, flows, and behaviors the GH skill family encodes.
- Strong public reference repos only for concrete ambiguities that official docs or live GitHub state do not settle cleanly.
- Duplicate guidance, contradictory defaults, stale GitHub setting names, stale file assumptions, partial follow-through, or logic that belongs in the shared GH core instead of a single skill.
- The local GH helper runtime only when a GH-skill claim or live-check contract depends on it.

## Auto-Apply Scope

- Minor wording updates that keep behavior aligned with current GitHub terms or surfaces.
- Safe file-reference updates when standard repo files or GitHub settings were added, removed, or renamed.
- Low-risk deduplication or refactoring inside the GH skill family that preserves behavior and clarifies ownership between the shared GH core and individual skills.
- Sync, validation, or repo-doc updates needed to keep the GH skill family consistent after those minor changes.

## Approval Boundary

- New or stricter default GitHub policy, changed merge or review posture, changed security posture, new mandatory paid features, new or removed skills, widened scope beyond `ceratops-gh-*`, or helper-runtime changes that materially alter live-check behavior.
- Refactors with meaningful behavior risk or unclear downstream impact.

## Execution Rules

- Start from the runtime checkout on local `main` tracking `origin/main`.
- For any repo change, create a worktree under the owning project folder's `worktrees\` directory.
- Do not edit the runtime checkout directly.
- Validate with `python .\scripts\sync-skill-core.py` and `python .\scripts\validate-skills.py`.
- If `src\ceratops_gh_runtime\` changed, also run `python -m ceratops_gh_runtime --help`.
- If safe minor updates were applied, ship them through the Ceratops GitHub ship flow, update the runtime checkout from `origin/main`, run `powershell -ExecutionPolicy Bypass -File .\scripts\install-skills.ps1` from the runtime checkout, and verify installed `ceratops-gh-*` junctions resolve to the runtime checkout.
- If approval-required changes are found, report them without applying them.

## Outcome Handling

- If no repo change was made and no recommendation was produced, do not open an inbox item.
- If minor changes were applied, open an inbox item with the applied updates and any approval-required follow-ups.
- If no change was applied but approval-required recommendations remain, open an inbox item with only those recommendations.
