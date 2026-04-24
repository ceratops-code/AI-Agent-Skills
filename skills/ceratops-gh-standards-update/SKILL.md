---
name: ceratops-gh-standards-update
description: Audit the Ceratops GitHub skill family in the `codex-skills` repo against current GitHub repository, settings, workflow, and relevant artifact-publishing best practices, including Docker and PyPI when those surfaces are in scope, then apply safe low-risk updates. Use when routine or explicit GH-skill upkeep should first build a current best-practice baseline and then see whether `skills/ceratops-gh-*`, shared core rules, helper-runtime claims, or repo docs need updates.
---

# Ceratops GH Standards Update

Audit the Ceratops GitHub skill family deliberately instead of letting normal GH task skills drift into generalized upkeep. Build a current best-practice baseline first, then compare the Ceratops GH skill family against that baseline and refresh only the safe in-scope deltas.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper package: `ceratops_gh_runtime`
- Live repo-settings check when a GH-skill claim depends on current GitHub behavior: `python -m ceratops_gh_runtime repo-health --repo OWNER/REPO`
- Shared-core sync: `python scripts/sync-skill-core.py`
- Skill validation: `python scripts/validate-skills.py`

## References

- Best-practice audit map: `references/best-practice-baseline.md`

## Skill-Specific Rules

- For this skill, the shared-core ban on generalized best-practice refresh during routine runs is inapplicable. Routine runs must perform a bounded best-practice refresh across GitHub repo contents, repo settings, workflow hardening, and the artifact-publishing surfaces that the Ceratops GH skill family actually claims to cover.
- Build the baseline from current official docs and live product behavior first. Use `gh`, GitHub API, `ceratops_gh_runtime`, package metadata, and registry endpoints as supporting evidence, and use public reference repos only for unresolved ambiguities.
- Treat Docker, PyPI, and other artifact surfaces as in scope only when the GH skill family, repo docs, or helper claims actually touch them.
- Separate the baseline from the Ceratops delta: first decide what current best practice says, then inspect whether `skills/ceratops-gh-*`, shared-core wording, helper-runtime claims, and repo docs are stale.
- Keep detailed audit checklists in `references/` rather than bloating `SKILL.md`.
- Apply safe wording, file-reference, checklist, and repo-doc updates directly. Report approval-bound policy, security, review, merge, cost, or helper-runtime changes instead of silently tightening defaults.

## Inputs To Capture

- Whether the run is routine automation upkeep or an explicit user-requested GH-skill refresh.
- Current target scope inside `codex-skills`: `skills/ceratops-gh-*`, `templates/common-core.md`, `scripts/sync-skill-core.py`, `scripts/validate-skills.py`, `src/ceratops_gh_runtime/`, and repo docs.
- Which best-practice surfaces are actually in scope: GitHub repo contents, repo settings, workflow hardening, release posture, Docker or OCI publishing, PyPI publishing, or a documented no-artifact posture.
- Whether current findings stay inside safe minor updates or cross the approval boundary.
- Whether the current task should only stage updates into the active local `release/*` batch or also ship them through GitHub now.

Infer missing inputs from local repo state, installed skill state, live GitHub evidence, and the active automation prompt before asking.

## Boundaries

- Use this skill when the work is to refresh the Ceratops GitHub skill family against current GitHub repository, settings, workflow, release, or artifact-publishing best practices.
- If the task is normal repo shipping, PR handling, dependency updates, or repo-health work rather than GH skill-family upkeep, stop and use the matching `ceratops-gh-*` task skill.
- If the work is only shipping already-prepared skill changes with no further upkeep analysis, stop and use `$ceratops-gh-codex-skill-ship`.
- If the requested change would widen scope beyond `ceratops-gh-*`, change default GitHub policy, change merge or review posture, change security posture, add mandatory paid features, or materially alter the GH helper runtime, stop before applying it and report the recommendation.

## Workflow

### 1. Inspect local and installed state

- Inspect current repo branch, worktree state, existing `ceratops-gh-*` skill folders, shared core template files, GH helper runtime files, repo docs, installed Ceratops skill junctions, and the installed automation prompt when this run came from automation.
- Check GitHub auth, local git auth, and installed tooling before asking for credentials.
- Classify current differences as stale local dirt, safe in-scope change, approval-bound change, or not applicable.

### 2. Build the current best-practice baseline

- Read `references/best-practice-baseline.md` at the start of the audit and use it as the bounded checklist for the next evidence-gathering steps.
- Use local files, `gh`, GitHub API, `ceratops_gh_runtime`, `gh` help, package metadata, release metadata, and registry endpoints as the first-pass evidence for the GitHub or artifact behavior that the GH skill family encodes.
- Check current official GitHub docs for repo settings, workflow policy, rulesets, actions, security, release behavior, and repository contents wherever the next best-practice decision depends on them.
- Check current official Docker, GHCR, PyPI, or Python packaging docs only for artifact surfaces that are actually in scope.
- Use 2-3 strong current public reference repos only for concrete ambiguous patterns that official docs and live product state do not settle cleanly.

### 3. Audit the GH skill family

- Review `skills/ceratops-gh-*`, `templates/common-core.md`, `scripts/sync-skill-core.py`, `scripts/validate-skills.py`, and `src/ceratops_gh_runtime/` only where a GH-skill claim depends on them.
- Look for duplicate guidance, contradictory defaults, stale GitHub setting names, stale required-file assumptions, stale repository-health expectations, stale workflow hardening guidance, stale Docker or PyPI guidance, partial follow-through, or logic that belongs in the shared core instead of a single skill.
- Keep repo docs aligned when stale: `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.

### 4. Apply safe updates only

- Apply wording updates that align behavior with the current best-practice baseline and current GitHub or registry terms.
- Apply safe file-reference updates when standard repo files, GitHub settings, workflow surfaces, or artifact-publish expectations were added, removed, or renamed.
- Apply low-risk deduplication or refactoring inside the GH skill family that preserves behavior and clarifies ownership between the shared core, this skill, and artifact-specific task skills.
- Add or update bounded reference material when the skill needs a checklist that would otherwise bloat `SKILL.md`.
- Do not edit the runtime checkout directly. For repo changes, work in a dedicated worktree under the owning project folder.
- Do not apply new or stricter default GitHub policy, changed merge or review posture, changed security posture, new mandatory paid features, widened scope beyond `ceratops-gh-*`, or GH helper-runtime changes that materially alter live-check behavior without explicit approval.

### 5. Validate and align

- Run `python scripts/sync-skill-core.py` and `python scripts/validate-skills.py`.
- If `src/ceratops_gh_runtime/` changed, also run `python -m ceratops_gh_runtime --help`.
- Verify changed `SKILL.md` files, `agents/openai.yaml`, repo docs, and the installed automation prompt all point at the current source of truth.

### 6. Stage or ship and sync local runtime

- If safe minor updates were applied, use `$ceratops-codex-skill-stage-release` to merge the ready worktree branch into the runtime `release/*` branch, rerun the installer from the runtime checkout, and verify installed `ceratops-gh-*` skills resolve there.
- Use `$ceratops-gh-codex-skill-ship` only when the current task explicitly expects GitHub publication after the standards refresh.
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
- Verify repo changes are staged into the active local `release/*` batch or shipped, according to the current task.
- Verify installed `ceratops-gh-*` junctions resolve to the intended source folder after staging or shipping when the GH skill family changed.
- Verify the automation prompt, this `SKILL.md`, and the active instruction sources remain aligned.

## Output Contract

Report only:

- applied safe GH-skill updates
- approval-required recommendations, blockers, or non-blocking debt
- intentionally retained leftovers or exceptions with reasons
- anything important not verified

For routine automation runs with no repo change and no recommendation, do not open an inbox item.

## Example Invocation

`Use $ceratops-gh-standards-update to build a current best-practice baseline for GitHub repo contents, settings, workflows, and relevant Docker or PyPI publishing, then update the Ceratops GitHub skill family where safe.`
