---
name: ceratops-gh-standards-update
description: Refresh and update the Ceratops GitHub skill family in the `codex-skills` repo against current GitHub standards and live GitHub behavior. Use when routine or explicit GH-skill upkeep should review `skills/ceratops-gh-*`, shared core rules, helper-runtime claims, and repo docs, apply safe low-risk updates, and ship the resulting skill changes.
---

# Ceratops GH Standards Update

Refresh the Ceratops GitHub skill family deliberately instead of letting normal GH task skills drift into generalized upkeep. Ground decisions in local repo state, live GitHub behavior, current official GitHub docs when needed, and targeted strong reference repos only for concrete ambiguities.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- For GitHub or registry tasks only, use `gh`, GitHub API, and `ceratops_gh_runtime` as part of the first-pass direct evidence before checking current official docs or `gh` help.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper package: `ceratops_gh_runtime`
- Live repo-settings check when a GH-skill claim depends on current GitHub behavior: `python -m ceratops_gh_runtime repo-health --repo OWNER/REPO`
- Shared-core sync: `python scripts/sync-skill-core.py`
- Skill validation: `python scripts/validate-skills.py`

## Inputs To Capture

- Whether the run is routine automation upkeep or an explicit user-requested GH-skill refresh.
- Current target scope inside `codex-skills`: `skills/ceratops-gh-*`, `templates/common-core.md`, `scripts/sync-skill-core.py`, `scripts/validate-skills.py`, `src/ceratops_gh_runtime/`, and repo docs.
- Whether current findings stay inside safe minor updates or cross the approval boundary.
- Whether shipping and local install sync should run now or remain blocked on approval-required recommendations.

Infer missing inputs from local repo state, installed skill state, live GitHub evidence, and the active automation prompt before asking.

## Boundaries

- Use this skill when the work is to refresh the Ceratops GitHub skill family against current GitHub guidance, live GitHub behavior, or concrete reference-repo patterns.
- If the task is normal repo shipping, PR handling, dependency updates, or repo-health work rather than GH skill-family upkeep, stop and use the matching `ceratops-gh-*` task skill.
- If the work is only shipping already-prepared skill changes with no further upkeep analysis, stop and use `$ceratops-gh-codex-skill-ship`.
- If the requested change would widen scope beyond `ceratops-gh-*`, change default GitHub policy, change merge or review posture, change security posture, add mandatory paid features, or materially alter the GH helper runtime, stop before applying it and report the recommendation.

## Workflow

### 1. Inspect local and installed state

- Inspect current repo branch, worktree state, existing `ceratops-gh-*` skill folders, shared core template files, GH helper runtime files, repo docs, installed Ceratops skill junctions, and the installed automation prompt when this run came from automation.
- Check GitHub auth, local git auth, and installed tooling before asking for credentials.
- Classify current differences as stale local dirt, safe in-scope change, approval-bound change, or not applicable.

### 2. Build current evidence

- Use local files, `gh`, GitHub API, `ceratops_gh_runtime`, and `gh` help as first-pass evidence for GitHub behavior or terminology that the GH skill family encodes.
- Check current official GitHub docs only when local evidence or live GitHub state leaves a concrete ambiguity or conflict.
- Use 2-3 strong current public reference repos only for concrete ambiguous patterns that official docs and live GitHub state do not settle cleanly.

### 3. Audit the GH skill family

- Review `skills/ceratops-gh-*`, `templates/common-core.md`, `scripts/sync-skill-core.py`, `scripts/validate-skills.py`, and `src/ceratops_gh_runtime/` only where a GH-skill claim depends on them.
- Look for duplicate guidance, contradictory defaults, stale GitHub setting names, stale file assumptions, stale user-local absolute paths in repo-tracked public files, partial follow-through, or logic that belongs in the shared core instead of a single skill.
- Keep repo docs aligned when stale: `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.

### 4. Apply safe updates only

- Apply minor wording updates that align behavior with current GitHub terms or surfaces.
- Apply safe file-reference updates when standard repo files or GitHub settings were added, removed, or renamed.
- Apply low-risk deduplication or refactoring inside the GH skill family that preserves behavior and clarifies ownership between the shared core and individual skills.
- Do not edit the runtime checkout directly. For repo changes, work in a dedicated worktree under the owning project folder.
- Do not apply new or stricter default GitHub policy, changed merge or review posture, changed security posture, new mandatory paid features, widened scope beyond `ceratops-gh-*`, or GH helper-runtime changes that materially alter live-check behavior without explicit approval.

### 5. Validate and align

- Run `python scripts/sync-skill-core.py` and `python scripts/validate-skills.py`.
- If `src/ceratops_gh_runtime/` changed, also run `python -m ceratops_gh_runtime --help`.
- Verify changed `SKILL.md` files, `agents/openai.yaml`, repo docs, and the installed automation prompt all point at the current source of truth.

### 6. Ship and sync local runtime

- If safe minor updates were applied, use `$ceratops-codex-skill-stage-release` to merge the ready worktree branch into the runtime `release/*` branch, then use `$ceratops-gh-codex-skill-ship` to ship the repo change, restore the runtime checkout to `main`, rerun the installer from the runtime checkout, and verify installed `ceratops-gh-*` skills resolve there.
- If approval-required changes were found, report them without applying them.
- For routine automation runs with no repo change and no recommendation, complete without opening an inbox item.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify every changed in-scope skill validates locally.
- Verify repo changes are shipped or correctly blocked.
- Verify installed `ceratops-gh-*` junctions resolve to the intended source folder after shipping when the GH skill family changed.
- Verify the automation prompt, this `SKILL.md`, and the active instruction sources remain aligned.

## Output Contract

Report only:

- applied safe GH-skill updates
- approval-required recommendations, blockers, or non-blocking debt
- intentionally retained leftovers or exceptions with reasons
- anything important not verified

For routine automation runs with no repo change and no recommendation, do not open an inbox item.

## Example Invocation

`Use $ceratops-gh-standards-update to review the Ceratops GitHub skill family against current GitHub standards, apply safe updates, and ship the resulting skill changes.`
