---
name: ceratops-codex-skill-stage-release
description: Stage committed Ceratops skill changes into the runtime checkout's local `release/*` branch for coherent local preview. Use when Codex should merge ready task-worktree branches into a release branch created from `main`, switch the runtime checkout to that branch, update the local skill install, and run the local validation batch before GitHub shipping.
---

# Ceratops Codex Skill Stage Release

Stage committed skill branches into the runtime checkout's local release branch so Codex can use one coherent unpublished repo snapshot.

## Defaults

- Source repo: active `AI-Agent-Skills` checkout root
- Installed Ceratops skill path: `$CODEX_HOME/skills/<skill-name>`
- Default release branch: `release/local`
- Runtime installer: `powershell -ExecutionPolicy Bypass -File .\\scripts\\install-skills.ps1`

## Skill-Specific Rules

- Stage only committed task-worktree branches. Do not use this skill as a substitute for intentional commits on the source branches.
- Blocking: Before reporting a staged release branch as ready to ship or invoking `$ceratops-gh-codex-skill-ship`, check remaining local worktrees and local branches for staged, unstaged, untracked, or committed work that is not included in the release branch.
- Blocking: If another local branch or worktree has work not included in the release branch, stop before shipping and ask whether to commit and stage it into the same release, intentionally retain it for later, or clean it up; do not decide silently.
- After a branch is successfully merged into the local release branch, remove that branch's task worktree and local source branch automatically when safe; use `-KeepMergedBranches` only when there is an explicit active-workflow reason and report that reason.
- After a squash-merged ship, recreate or rebase long-lived task branches from updated `main` before staging more work. Do not re-merge a branch whose earlier contents already landed on `main` via squash.
- Use `--reset` staging when rebuilding the release branch from `main` is cheaper or safer than untangling partial staged state.

## Script Bundle

- Release-branch staging helper: `scripts/stage-release.ps1`
- Pending local work check: `scripts/check-pending-release-work.ps1`

## Inputs To Capture

- The committed task branches that are ready to join the local batch.
- The runtime checkout path and intended local `release/*` branch.
- Whether the release branch should append more branches or be rebuilt from `main`.
- Any explicit reason to keep a merged source task branch or task worktree after staging.
- Any other local worktree or branch with staged, unstaged, untracked, or committed work not included in the intended release branch.
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

- Inspect the source worktree branches, runtime checkout branch, installed managed skill-copy state, and any duplicated installed copies.
- Blocking: Inspect remaining local worktrees and local branches before ship handoff so non-staged work is not silently left behind.
- Confirm each branch to stage is intentionally committed and available to the shared repo.
- Refresh remote refs with `git fetch --prune origin` before judging whether `origin/release/*` still exists or whether a prior staged branch or PR was already cleaned up.
- Assume the next ship will reuse the same `release/*` branch name remotely unless the user explicitly chose a different branch-naming scheme.
- If a branch already shipped through a squash merge, recreate or rebase it on current `main` before staging new work from it.
- Decide whether the release branch should be reused or rebuilt from `main`.

### 2. Stage the runtime release branch

- Run `scripts/stage-release.ps1` to create or reuse the local `release/*` branch from `main`, switch the runtime checkout there, merge the requested committed branches, and remove each merged source task worktree and local source branch unless explicitly retained.
- If the runtime checkout is dirty before staging, stop and resolve that state instead of merging into it blindly.

### 3. Sync installed runtime state

- Run `powershell -ExecutionPolicy Bypass -File .\\scripts\\install-skills.ps1` from the runtime checkout.
- Confirm each installed Ceratops skill copy has `.ceratops-runtime-manifest.json` and was regenerated by the runtime installer.

### 4. Validate the staged batch locally

- Run `python scripts/validate-skills.py`.
- Mandatory: When the PR-readiness helper script or installer changed, run `python scripts/github_pr_readiness.py --help`.

### 5. Report the staged state

- Blocking: Run `scripts/check-pending-release-work.ps1` against the runtime checkout and intended release branch before reporting the batch as ship-ready or continuing to `$ceratops-gh-codex-skill-ship`.
- Blocking: If the pending-work check reports any other dirty worktree, untracked work, staged work, unstaged work, or branch commits outside the release branch, stop before shipping and ask the user whether to include, retain, or clean up that work.
- Report the active local `release/*` branch, the staged task branches, and any blockers that still prevent shipping.
- Leave the runtime checkout on the staged release branch only when the batch is intentionally active.

## Completion Gate

- Verify the runtime checkout is on the intended local `release/*` branch.
- Verify each requested task branch was staged and its source worktree and local branch were removed, or a blocker or explicit retention reason was reported precisely.
- Blocking: Verify the pending local work check passed before ship handoff, or every reported non-staged branch or worktree is covered by an explicit user choice, retention reason, or blocker.
- Verify the installed skill copies are managed runtime outputs and include fresh runtime manifests.
- Verify the local validation batch passed or the blocking failures were reported.

## Output Contract

Report only:

- the active local release branch and staged task branches
- unresolved blockers or non-blocking debt
- intentionally retained runtime state, branches, or worktrees with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-codex-skill-stage-release to merge the ready skill branches into the local runtime release branch, switch the runtime checkout there, and validate the staged batch.`
