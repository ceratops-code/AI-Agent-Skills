---
name: ceratops-gh-skills-standards-update
description: Audit the Ceratops GitHub skill family in the `codex-skills` repo against current GitHub repository, settings, workflow, and relevant artifact-publishing best practices for the artifact types covered by the Ceratops publish and ship skills, including Docker, PyPI, and other supported registries or public artifacts when those surfaces are in scope, then apply safe low-risk updates. Use when routine or explicit GH-skill upkeep should first build a current best-practice baseline and then see whether `skills/ceratops-gh-*`, shared section rules, helper-runtime claims, or repo docs need updates.
---

# Ceratops GH Skills Standards Update

Audit the Ceratops GitHub skill family deliberately instead of letting normal GH task skills drift into generalized upkeep. Build a current best-practice baseline first, then compare the Ceratops GH skill family against that baseline and refresh only the safe in-scope deltas.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Blocking: Everything in this section is part of the skill contract unless explicitly inapplicable to the current task.
- Blocking: When this skill is invoked, follow this `SKILL.md` as the workflow contract for the task; if a higher-precedence instruction conflicts with a required skill step, report the conflict instead of silently skipping the step.
- Blocking: Do not claim completion unless this skill's completion gate is satisfied, intentionally inapplicable, or reported as a blocker.
- Blocking: Scope completion, current-state, root-cause, no-fix, unsupported, and durable-resolution claims to evidence actually checked, or to fresh same-task evidence that still applies.
- Blocking: Reuse fresh sufficient same-run evidence unless state is uncertain, plausibly changed, materially broadened, externally mutable for the decision, or this skill explicitly requires a fresh check.
- Blocking: Prefer direct local evidence and targeted diagnostics for the next skill decision; use current official sources only when local evidence leaves a concrete ambiguity or the task depends on unstable external behavior.
- Blocking: Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine skill runs unless the user explicitly asks or a required decision remains ambiguous after targeted evidence.
- Blocking: Ask before risky, destructive, irreversible, credential-dependent, externally mutating, complex, invasive, nonstandard, or high-maintenance steps unless the user already explicitly requested that tradeoff.
- Blocking: Do not update this `SKILL.md` or other skill/control files during a routine run unless the user explicitly asked for skill maintenance or the task cannot be completed safely without a narrow in-scope fix.
- Mandatory: When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Mandatory: Follow this skill's output contract when present; otherwise report only the outcome, unresolved blockers, retained state with reasons, and important unverified items.

<!-- SECTION SOURCE: templates/sections/gh-current-state.md -->

## GH Current State

- Use the shared helper package `ceratops_gh_current_state` for bundled GitHub current-state checks when it covers the next decision.
- Use `gh`, GitHub API, and `ceratops_gh_current_state` as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Blocking: Do not ask for credentials unless they are truly required after local checks.
- Blocking: If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target
- Blocking: If the user refuses a missing permission, credential, login, or scope, stop retrying and report the blocked action and exact entities still pending.
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Script Bundle

- Live repo-settings check when a GH-skill claim depends on current GitHub behavior: `python -m ceratops_gh_current_state repo-health --repo OWNER/REPO`
- Shared-sections sync: `python scripts/sync-skill-sections.py`
- Skill validation: `python scripts/validate-skills.py`

## References

- Best-practice audit map: `references/best-practice-baseline.md`

## Skill-Specific Rules

- For this skill, the shared section rule against generalized best-practice refresh during routine runs is inapplicable. Routine runs must perform a bounded best-practice refresh across GitHub repo contents, repo settings, workflow hardening, and the artifact-publishing surfaces that the Ceratops GH skill family actually claims to cover.
- Build the baseline from current official docs and live product behavior first. Use `gh`, GitHub API, `ceratops_gh_current_state`, package metadata, and registry endpoints as supporting evidence, and use public reference repos only for unresolved ambiguities.
- Treat artifact surfaces as in scope only when the GH skill family, repo docs, or helper claims actually touch them, using the artifact boundary defined by `ceratops-gh-repo-create-and-publish` and `ceratops-gh-ship-change`.
- Separate the baseline from the Ceratops delta: first decide what current best practice says, then inspect whether `skills/ceratops-gh-*`, shared section wording or assignments, helper-runtime claims, and repo docs are stale.
- Keep detailed audit checklists in `references/` rather than bloating `SKILL.md`.
- Apply safe wording, file-reference, checklist, and repo-doc updates directly. Report approval-bound policy, security, review, merge, cost, or helper-runtime changes instead of silently tightening defaults.

## Inputs To Capture

- Whether the run is routine automation upkeep or an explicit user-requested GH-skill refresh.
- Current target scope inside `codex-skills`: `skills/ceratops-gh-*`, `templates/sections/`, `templates/skill-sections.json`, `scripts/sync-skill-sections.py`, `scripts/validate-skills.py`, `src/ceratops_gh_current_state/`, and repo docs.
- Which best-practice surfaces are actually in scope: GitHub repo contents, repo settings, workflow hardening, release posture, artifact types supported by `ceratops-gh-repo-create-and-publish` or `ceratops-gh-ship-change`, or a documented no-artifact posture.
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

- Inspect current repo branch, worktree state, existing `ceratops-gh-*` skill folders, shared section files and manifest, GH helper runtime files, repo docs, installed Ceratops skill junctions, and the installed automation prompt when this run came from automation.
- Check GitHub auth, local git auth, and installed tooling before asking for credentials.
- Classify current differences as stale local dirt, safe in-scope change, approval-bound change, or not applicable.

### 2. Build the current best-practice baseline

- Read `references/best-practice-baseline.md` at the start of the audit and use it as the bounded checklist for the next evidence-gathering steps.
- Use local files, `gh`, GitHub API, `ceratops_gh_current_state`, `gh` help, package metadata, release metadata, and registry endpoints as the first-pass evidence for the GitHub or artifact behavior that the GH skill family encodes.
- Check current official GitHub docs for repo settings, workflow policy, rulesets, actions, security, release behavior, and repository contents wherever the next best-practice decision depends on them.
- Check current official Docker, GHCR, PyPI, or Python packaging docs only for artifact surfaces that are actually in scope.
- Use 1-2 strong current public reference repos only for concrete ambiguous patterns that official docs and live product state do not settle cleanly.

### 3. Audit the GH skill family

- Review `skills/ceratops-gh-*`, `templates/sections/`, `templates/skill-sections.json`, `scripts/sync-skill-sections.py`, `scripts/validate-skills.py`, and `src/ceratops_gh_current_state/` only where a GH-skill claim depends on them.
- Look for duplicate guidance, contradictory defaults, stale GitHub setting names, stale required-file assumptions, stale repository-health expectations, stale workflow hardening guidance, stale artifact-publishing guidance, partial follow-through, or logic that belongs in a shared section instead of a single skill.
- Keep repo docs aligned when stale: `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.

### 4. Apply safe updates only

- Apply wording updates that align behavior with the current best-practice baseline and current GitHub or registry terms.
- Apply safe file-reference updates when standard repo files, GitHub settings, workflow surfaces, or artifact-publish expectations were added, removed, or renamed.
- Apply low-risk deduplication or refactoring inside the GH skill family that preserves behavior and clarifies ownership between the shared sections, this skill, and artifact-specific task skills.
- Add or update bounded reference material when the skill needs a checklist that would otherwise bloat `SKILL.md`.
- Do not edit the runtime checkout directly. For repo changes, work in a dedicated worktree under the owning project folder.
- Do not apply new or stricter default GitHub policy, changed merge or review posture, changed security posture, new mandatory paid features, widened scope beyond `ceratops-gh-*`, or GH helper-runtime changes that materially alter live-check behavior without explicit approval.

### 5. Validate and align

- If `templates/sections/` or `templates/skill-sections.json` changed, run the shared-source maintenance workflow recorded in `templates/skill-sections.json`.
- Otherwise run the skill-local-or-metadata maintenance workflow recorded in `templates/skill-sections.json`.
- If `src/ceratops_gh_current_state/` or helper-runtime claims changed, also run the helper-runtime maintenance workflow recorded in `templates/skill-sections.json`.
- Verify changed `SKILL.md` files, `agents/openai.yaml`, repo docs, and the installed automation prompt all point at the current source of truth.

### 6. Stage or ship and sync local runtime

- If safe minor updates were applied, use `$ceratops-codex-skill-stage-release` to merge the ready worktree branch into the runtime `release/*` branch, rerun the installer from the runtime checkout, and verify installed `ceratops-gh-*` skills resolve there.
- Use `$ceratops-gh-codex-skill-ship` only when the current task explicitly expects GitHub publication after the standards refresh.
- If approval-required changes were found, report them without applying them.
- For routine automation runs with no repo change and no recommendation, complete without opening an inbox item.

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

`Use $ceratops-gh-skills-standards-update to build a current best-practice baseline for GitHub repo contents, settings, workflows, and any relevant artifact publishing covered by the Ceratops publish and ship skills, then update the Ceratops GitHub skill family where safe.`
