---
name: ceratops-skill-update
description: Update existing Ceratops skills and the shared skill-maintenance layer in `AI-Agent-Skills` while keeping ownership clear between per-skill deltas, shared sections, the section manifest, runtime generation, sync or validation scripts, helper runtime claims, contracts, and repo docs.
---

# Ceratops Skill Update

Maintain existing Ceratops skills as one consistency surface instead of patching individual skill files in isolation. Decide first whether the source of truth is a skill-local delta, a shared section, the section manifest, runtime payloads, sync or validation logic, helper-runtime claims, contracts, or repo docs, then update the narrowest correct source.

## Skill-Specific Rules

- Mandatory: Treat `templates/sections/`, `templates/skill-sections.json`, `scripts/build-runtime-skills.py`, `scripts/sync-skill-sections.py`, `scripts/validate-skills.py`, `contracts/`, related repo docs, and any touched helper-runtime claims as one coupled maintenance surface.
- Mandatory: Decide the broadest correct source of truth before editing anything. Prefer shared sections and the section manifest for shared behavior, and keep per-skill source text limited to true deltas.
- Blocking: Do not put generated shared-section blocks in source `skills/*/SKILL.md`; update `templates/sections/`, `templates/skill-sections.json`, or `scripts/build-runtime-skills.py` when runtime generation needs to change.
- Mandatory: Add a new shared section only when it reduces meaningful duplication, clarifies ownership, or prevents conflicting drift across multiple skills. Prefer deleting, merging, or narrowing sections when that is cleaner.
- Mandatory: Treat this skill as the default Ceratops entrypoint for modifying existing skills.
- Mandatory: Update `agents/openai.yaml` when trigger behavior or the user-facing prompt becomes stale.
- Blocking: Ensure every Ceratops skill keeps `assets/ceratops-logo-500.png` copied from the repo-root `assets/ceratops-logo-500.png`, and sets both `interface.icon_small` and `interface.icon_large` in `agents/openai.yaml` to `./assets/ceratops-logo-500.png` when skill metadata, installer, or validation surfaces are updated.
- Mandatory: Update helper scripts or helper-runtime claims when the section model, runtime generation markers, validation rules, contract payloads, or skill claims require it.
- Blocking: Stop in the worktree by default. Do not stage or ship the resulting repo changes unless the user explicitly asked for staging, runtime-preview sync, or GitHub shipping.
- Mandatory: Use the default maintenance-check policy recorded in `templates/skill-sections.json`; run each required command once after relevant edits settle, suppress routine successful `--help` output with redirection rather than shell pipes, and rerun only failed commands or commands invalidated by later edits.

## Inputs To Capture

- Which existing skills or shared files are in scope: `skills/*`, `templates/sections/`, `templates/skill-sections.json`, `scripts/build-runtime-skills.py`, `scripts/sync-skill-sections.py`, `scripts/validate-skills.py`, `contracts/`, helper-runtime files, and repo docs.
- Whether the requested change belongs in skill-local text, a shared section, the section manifest, sync or validation logic, helper-runtime code or claims, or repo docs.
- Whether the task should stop at local repo changes or also stage them into the active local `release/*` batch.

Infer missing inputs from the current repo state before asking.

## Boundaries

- Use this skill when the task is to update existing Ceratops skills or the shared skill-maintenance layer itself.
- If the task is creating a brand-new Ceratops skill, stop and use `$ceratops-skill-create`.
- If the task is only staging or shipping already-prepared skill changes, stop and use `$ceratops-codex-skill-stage-release` or `$ceratops-gh-codex-skill-ship`.
- If the task is only a routine GitHub health contract review, stop and use `$ceratops-gh-skills-standards-update`.

## Workflow

### 1. Inspect the current maintenance surface

- Inspect the targeted skills, the shared section files, the section manifest, sync and validation scripts, touched helper-runtime files or claims, and repo docs that describe the current structure.
- Mandatory: Start maintenance inspection with targeted `rg` or path inventory and small line-window reads; broaden to full-file reads only for governing control files, ownership decisions, or unresolved context.
- Identify which parts are source of truth versus generated output.
- Classify the requested change as skill-local, shared, structural, validation-only, helper-runtime-adjacent, or docs-only.

### 2. Decide ownership before editing

- Decide whether the change belongs in a per-skill delta, an existing shared section, the section manifest, sync or validation logic, helper-runtime code or claims, or repo docs.
- Prefer the smallest change that keeps future maintenance consistent.
- If a proposed new section would only hold trivial text or one repeated line, keep it inline unless the duplication is already causing drift or ownership confusion.

### 3. Apply the updates at the real source of truth

- Update existing skills, shared sections, the section manifest, runtime payloads, sync or validation scripts, helper-runtime files or claims, contracts, and repo docs only where the chosen ownership requires it.
- Mandatory: Before renaming or moving shared contracts, scripts, templates, or payload folders, build one old-to-new reference map and update docs, skills, manifests, validators, and checkers from that map before running validation.
- When removing, merging, or narrowing sections, update every affected assignment and keep runtime generated section source comments readable in installed `SKILL.md` files.
- If the repo's current sync or validation flow no longer matches the section model, fix the scripts instead of working around them in skill text.

### 4. Run the needed checks

- If shared section source files or `templates/skill-sections.json` assignments changed, run the shared-source check path from `templates/skill-sections.json`: sync validation first, then full validation.
- After a successful sync check for the current shared-source delta, do not rerun sync as a routine closure check unless shared section sources, section assignments, runtime payloads, or sync logic changed again; use validation and targeted diffs for later helper, changelog, or skill-local edits.
- If the change stayed inside skill-local text, `agents/openai.yaml`, or repo docs, skip sync and run the skill-local validation path from `templates/skill-sections.json`.
- If helper-runtime code or claims changed, also run the helper-runtime smoke path from `templates/skill-sections.json`.
- Re-open the changed files from disk and confirm source skills, manifest assignments, runtime payloads, docs, contracts, and metadata still align.

### 5. Report or hand off

- Stop at validated local repo changes unless the user explicitly asked for staging or shipping.
- If local preview staging was requested, continue with `$ceratops-codex-skill-stage-release`.
- If GitHub publication was requested, stage first if needed, then continue with `$ceratops-gh-codex-skill-ship`.

## Completion Gate

- Verify every changed skill and shared file still points at the intended source of truth.
- Verify runtime shared-section generation is updated through shared sources, the manifest, and the builder when shared sources changed.
- Verify the section manifest, sync script, validation script, repo docs, and touched `agents/openai.yaml` files remain aligned.
- Blocking: Verify all Ceratops skill-local icon copies match the repo-root icon source and all `agents/openai.yaml` icon paths are runtime-local.
- Verify any removed, merged, or renamed section leaves no stale assignment or stale runtime payload behind.

## Output Contract

Report only:

- skills or shared maintenance surfaces updated
- new, removed, merged, or narrowed shared sections with reasons
- unresolved blockers or non-blocking debt
- intentionally retained inconsistencies or follow-up items with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-skill-update to update the Ceratops skills, choose the right source of truth automatically, run the needed checks, and keep the repo consistent.`
