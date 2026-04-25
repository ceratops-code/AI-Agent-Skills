---
name: ceratops-codex-skill-stage-release
description: Stage committed Ceratops skill changes into the runtime checkout's local `release/*` branch for coherent local preview. Use when Codex should merge ready task-worktree branches into a release branch created from `main`, switch the runtime checkout to that branch, update the local skill install, and run the local validation batch before GitHub shipping.
---

# Ceratops Codex Skill Stage Release

Stage committed skill branches into the runtime checkout's local release branch so Codex can use one coherent unpublished repo snapshot.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target

<!-- SECTION SOURCE: templates/sections/release-branch-runtime.md -->

## Release Branch Runtime

- Treat the runtime checkout's active `release/*` branch as the single local preview source of truth for the staged repo snapshot.
- Keep installed Ceratops skill junctions and the editable GH helper package pointed at the runtime checkout path, not at task worktrees.
- Reuse the same `release/*` branch name locally and remotely by default. Do not rename or remap it unless the user explicitly chooses that tradeoff.
- Refresh remote refs with `git fetch --prune origin` before judging whether a runtime `release/*` branch already exists remotely, should be reused, or was already cleaned up.
- Rerun the runtime installer after switching the runtime checkout branch so installed skill junctions and the editable GH helper package match the active repo snapshot.
- When the GH skill family was touched, confirm the editable GH helper package resolves from the runtime checkout after the installer or restore step.
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Defaults

- Source repo: `$HOME/CodexProjects/CeratopsSkills/codex-skills`
- Installed Ceratops skill path: `$CODEX_HOME/skills/<skill-name>`
- Default release branch: `release/local`
- Runtime installer: `powershell -ExecutionPolicy Bypass -File .\\scripts\\install-skills.ps1`

## Skill-Specific Rules

- Stage only committed task-worktree branches. Do not use this skill as a substitute for intentional commits on the source branches.
- After a squash-merged ship, recreate or rebase long-lived task branches from updated `main` before staging more work. Do not re-merge a branch whose earlier contents already landed on `main` via squash.
- Use `--reset` staging when rebuilding the release branch from `main` is cheaper or safer than untangling partial staged state.

## Script Bundle

- Release-branch staging helper: `scripts/stage-release.ps1`

## Inputs To Capture

- The committed task branches that are ready to join the local batch.
- The runtime checkout path and intended local `release/*` branch.
- Whether the release branch should append more branches or be rebuilt from `main`.
- Local validation expectations for the staged batch.

Infer missing inputs from local repo state before asking.

## Boundaries

- Use this skill when the goal is coherent local preview or local batching of unpublished skill changes in the runtime checkout.
- If the task is creating a brand-new Ceratops skill and not yet staging it, stop and use `$ceratops-skill-create`.
- If the task is updating existing Ceratops skill contents and not yet staging them, stop and use `$ceratops-skill-update`.
- If the runtime release branch is already staged and the task is ready to publish, stop and use `$ceratops-gh-codex-skill-ship`.
- If the task is general repo shipping not focused on Codex skills and local skill installation, stop and use `$ceratops-gh-ship-change`.

## Workflow

### 1. Inspect source and runtime state

- Inspect the source worktree branches, runtime checkout branch, installed junction state, and any duplicated installed copies.
- Confirm each branch to stage is intentionally committed and available to the shared repo.
- Refresh remote refs with `git fetch --prune origin` before judging whether `origin/release/*` still exists or whether a prior staged branch or PR was already cleaned up.
- Assume the next ship will reuse the same `release/*` branch name remotely unless the user explicitly chose a different branch-naming scheme.
- If a branch already shipped through a squash merge, recreate or rebase it on current `main` before staging new work from it.
- Decide whether the release branch should be reused or rebuilt from `main`.

### 2. Stage the runtime release branch

- Run `scripts/stage-release.ps1` to create or reuse the local `release/*` branch from `main`, switch the runtime checkout there, and merge the requested committed branches.
- If the runtime checkout is dirty before staging, stop and resolve that state instead of merging into it blindly.

### 3. Sync installed runtime state

- Run `powershell -ExecutionPolicy Bypass -File .\\scripts\\install-skills.ps1` from the runtime checkout.
- Confirm the installed skill paths resolve to the runtime checkout.

### 4. Validate the staged batch locally

- Run `python scripts/validate-skills.py`.
- When the GH helper package or installer changed, run `python -m ceratops_gh_current_state --help`.

### 5. Report the staged state

- Report the active local `release/*` branch, the staged task branches, and any blockers that still prevent shipping.
- Leave the runtime checkout on the staged release branch only when the batch is intentionally active.

## Completion Gate

- Verify the runtime checkout is on the intended local `release/*` branch.
- Verify each requested task branch was staged or a blocker was reported precisely.
- Verify the installed skill paths resolve to the runtime checkout.
- Verify the local validation batch passed or the blocking failures were reported.

## Output Contract

Report only:

- the active local release branch and staged task branches
- unresolved blockers or non-blocking debt
- intentionally retained runtime state with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-codex-skill-stage-release to merge the ready skill branches into the local runtime release branch, switch the runtime checkout there, and validate the staged batch.`
