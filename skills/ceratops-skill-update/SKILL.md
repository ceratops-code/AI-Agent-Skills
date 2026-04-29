---
name: ceratops-skill-update
description: Update existing Ceratops skills and the shared skill-maintenance layer in `AI-Agent-Skills` while keeping ownership clear between per-skill deltas, shared sections, the section manifest, sync or validation scripts, helper runtime claims, and repo docs. Use when the user asks to update Ceratops skills, keep them consistent, add/remove/merge sections, or refresh the supporting sync and validation flow without manually drifting generated skill blocks.
---

# Ceratops Skill Update

Maintain existing Ceratops skills as one consistency surface instead of patching individual skill files in isolation. Decide first whether the source of truth is a skill-local delta, a shared section, the section manifest, a sync or validation script, helper-runtime claims, or repo docs, then update the narrowest correct source and regenerate derived skill files only when needed.

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
- Blocking: For skill runtime workflows, invoke shared helpers through installed console commands or `python -m <module>` entrypoints; do not locate shared helpers by absolute paths, by the repo's parent directory, or by per-skill `scripts` junctions.
- Blocking: When a Ceratops skill-maintenance workflow explicitly needs a repo-maintenance script, treat `scripts/<name>` paths as relative to the active `AI-Agent-Skills` checkout root; resolve that root from the current worktree with `git rev-parse --show-toplevel` or from the installed skill junction under `$CODEX_HOME/skills/<skill-name>`, and stop as blocked if neither resolves to a checkout containing `skills/`, `templates/`, and `scripts/`.
- Mandatory: When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Mandatory: Follow this skill's output contract when present; otherwise report only the outcome, unresolved blockers, retained state with reasons, and important unverified items.

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

## Skill-Specific Rules

- Treat `templates/sections/`, `templates/skill-sections.json`, generated shared blocks inside `skills/*/SKILL.md`, `scripts/sync-skill-sections.py`, `scripts/validate-skills.py`, related repo docs, and any touched helper-runtime claims as one coupled maintenance surface.
- Decide the broadest correct source of truth before editing anything. Prefer shared sections and the section manifest for shared behavior, and keep per-skill text limited to true deltas.
- Do not hand-edit a generated shared-sections block in a skill when the change belongs in `templates/sections/` or `templates/skill-sections.json`. Update the source of truth and rerun sync.
- Add a new shared section only when it reduces meaningful duplication, clarifies ownership, or prevents conflicting drift across multiple skills. Prefer deleting, merging, or narrowing sections when that is cleaner.
- Treat this skill as the default Ceratops entrypoint for modifying existing skills.
- Update `agents/openai.yaml` when trigger behavior or the user-facing prompt becomes stale.
- Update helper scripts or helper-runtime claims when the section model, generated markers, validation rules, or skill claims require it.
- Stop in the worktree by default. Do not stage or ship the resulting repo changes unless the user explicitly asked for staging, runtime-preview sync, or GitHub shipping.
- Use the default maintenance-check policy recorded in `templates/skill-sections.json` instead of making the user specify commands.

## Inputs To Capture

- Which existing skills or shared files are in scope: `skills/*`, `templates/sections/`, `templates/skill-sections.json`, `scripts/sync-skill-sections.py`, `scripts/validate-skills.py`, helper-runtime files, and repo docs.
- Whether the requested change belongs in skill-local text, a shared section, the section manifest, sync or validation logic, helper-runtime code or claims, or repo docs.
- Whether the task should stop at local repo changes or also stage them into the active local `release/*` batch.

Infer missing inputs from the current repo state before asking.

## Boundaries

- Use this skill when the task is to update existing Ceratops skills or the shared skill-maintenance layer itself.
- If the task is creating a brand-new Ceratops skill, stop and use `$ceratops-skill-create`.
- If the task is only staging or shipping already-prepared skill changes, stop and use `$ceratops-codex-skill-stage-release` or `$ceratops-gh-codex-skill-ship`.
- If the task is only a routine GH-family best-practice audit inside `ceratops-gh-*`, stop and use `$ceratops-gh-skills-standards-update`.

## Workflow

### 1. Inspect the current maintenance surface

- Inspect the targeted skills, the shared section files, the section manifest, sync and validation scripts, touched helper-runtime files or claims, and repo docs that describe the current structure.
- Identify which parts are source of truth versus generated output.
- Classify the requested change as skill-local, shared, structural, validation-only, helper-runtime-adjacent, or docs-only.

### 2. Decide ownership before editing

- Decide whether the change belongs in a per-skill delta, an existing shared section, the section manifest, sync or validation logic, helper-runtime code or claims, or repo docs.
- Prefer the smallest change that keeps future maintenance consistent.
- If a proposed new section would only hold trivial text or one repeated line, keep it inline unless the duplication is already causing drift or ownership confusion.

### 3. Apply the updates at the real source of truth

- Update existing skills, shared sections, the section manifest, sync or validation scripts, helper-runtime files or claims, and repo docs only where the chosen ownership requires it.
- When removing, merging, or narrowing sections, update every affected assignment and keep the generated section source comments readable in the resulting `SKILL.md` files.
- If the repo's current sync or validation flow no longer matches the section model, fix the scripts instead of working around them in skill text.

### 4. Run the needed checks

- If shared section source files or `templates/skill-sections.json` assignments changed, run the shared-source check path from `templates/skill-sections.json`: sync first, then validate.
- After a successful sync for the current shared-source delta, do not rerun sync as a routine closure check unless shared section sources, section assignments, generated blocks, or sync logic changed again; use validation and targeted diffs for later helper, changelog, or skill-local edits.
- If the change stayed inside skill-local text, `agents/openai.yaml`, or repo docs, skip sync and run the skill-local validation path from `templates/skill-sections.json`.
- If helper-runtime code or claims changed, also run the helper-runtime smoke path from `templates/skill-sections.json`.
- Re-open the changed files from disk and confirm the generated blocks, manifest assignments, docs, and metadata still align.

### 5. Report or hand off

- Stop at validated local repo changes unless the user explicitly asked for staging or shipping.
- If local preview staging was requested, continue with `$ceratops-codex-skill-stage-release`.
- If GitHub publication was requested, stage first if needed, then continue with `$ceratops-gh-codex-skill-ship`.

## Completion Gate

- Verify every changed skill and shared file still points at the intended source of truth.
- Verify generated shared blocks were updated through the shared sources and sync flow when shared sources changed.
- Verify the section manifest, sync script, validation script, repo docs, and touched `agents/openai.yaml` files remain aligned.
- Verify any removed, merged, or renamed section leaves no stale assignment or stale generated block behind.

## Output Contract

Report only:

- skills or shared maintenance surfaces updated
- new, removed, merged, or narrowed shared sections with reasons
- unresolved blockers or non-blocking debt
- intentionally retained inconsistencies or follow-up items with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-skill-update to update the Ceratops skills, choose the right source of truth automatically, run the needed checks, and keep the repo consistent.`
