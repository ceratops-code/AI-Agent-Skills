---
name: ceratops-codex-skill-ship
description: Ship Ceratops or other local Codex skill changes from the codex-skills source repo to GitHub and the installed local skill set. Use when Codex should validate changed skill folders, ensure installed junctions under .codex/skills are correct, publish the repo change through GitHub, and verify the installed skills resolve to the intended source.
---

# Ceratops Codex Skill Ship

Ship changes to the local Codex skill source repo and keep the installed Ceratops skill junctions in sync.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Defaults

- Source repo: `%USERPROFILE%\\CodexProjects\\CeratopsSkills\\codex-skills`
- Installed Ceratops skill path: `%USERPROFILE%\\.codex\\skills\\<skill-name>`
- Local GH helper package install command: `python -m pip install --editable .`
- Ceratops-installed skills should resolve through junctions to the source repo unless there is a documented exception.

## Skill-Specific Rules

- Validate every changed skill folder before shipping.
- Ensure `SKILL.md`, `agents/openai.yaml`, and any bundled resources stay aligned.
- Prefer running the repo installer when GH skills, the GH helper package, or install metadata changed; otherwise repair the local installed junctions directly when needed.
- Reuse the general GitHub ship flow rather than inventing a parallel release process.
- Remove low-risk stale installed copies, stale junctions, or stale generated skill artifacts when safe.

## Inputs To Capture

- Changed skill folders and whether each one is new, updated, metadata-only, or cleanup.
- Repo branch, PR, merge, and validation expectations.
- Installed junction expectations and any known exceptions.

## Boundaries

- Use this skill when working in the `codex-skills` source repo or another skill source repo with the same local-install pattern.
- If the task is only creating or editing the skill contents and not shipping them, stop and use the system `$skill-creator` guidance plus the relevant task skill.
- If the task is general repo shipping not focused on Codex skills and local skill installation, stop and use `$ceratops-gh-ship-change`.

## Workflow

### 1. Inspect changed skill scope

- Inspect changed skill folders, repo state, installed junction state, and any duplicated installed copies.
- Identify whether the work is a new skill, a skill update, metadata-only work, or cleanup.

### 2. Validate skills locally

- Run the skill validator for every changed skill.
- Check that `agents/openai.yaml` still matches the intended user-facing name, short description, and default prompt.
- Verify any referenced bundled resources exist and are actually needed.
- When the GH helper package or installer changed, prove the packaged runtime still imports with `python -m ceratops_gh_runtime --help`.

### 3. Sync installed skill state

- Run `scripts/install-skills.ps1` when the GH helper package, install flow, or broad skill set changed. For narrow skill-only changes, create or repair the installed junction for each Ceratops skill that should be locally discoverable.
- Confirm the installed path resolves to the intended source folder.
- Confirm the GH helper package resolves from the intended checkout when the GH skill family was touched.
- Remove low-risk stale installed duplicates, wrong-path junctions, or stale installed GH runtime skill links.

### 4. Ship the repo change

- Use `$ceratops-gh-ship-change` when repo changes need to be committed, pushed, PR'd, merged, and cleaned up.
- If the work is only validation or stale-state cleanup with no content changes, use `$ceratops-gh-repo-health-audit` instead.

### 5. Verify final installed state

- After merge, verify the source repo is synced clean and the installed skill path still resolves correctly.
- Report any intentionally retained installed exceptions or repo leftovers.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify every changed skill validates locally.
- Verify the repo change is merged or correctly blocked.
- Verify each expected installed junction resolves to the intended source folder.
- Verify the GH helper package resolves from the intended checkout when the GH skill family was part of the run.

## Output Contract

Report only:

- changed skills
- unresolved blockers or non-blocking debt
- intentionally retained installed exceptions or repo leftovers with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-codex-skill-ship to ship the changed Ceratops skills to GitHub, update the installed junctions, and verify the installed skills resolve to the source repo.`
