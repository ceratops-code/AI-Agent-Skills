---
name: ceratops-gh-codex-skill-ship
description: Ship Ceratops or other local Codex skill changes from the runtime checkout's staged `release/*` branch through GitHub and back to the installed runtime on `main`. Use when Codex should validate staged skill changes, confirm the runtime checkout is on the intended release branch, publish the batch through GitHub, then restore the runtime checkout and installed skills to synced `main`.
---

# Ceratops GH Codex Skill Ship

Ship a staged Ceratops skill batch through GitHub, then restore the runtime checkout and installed skill state to clean `main`.

## Defaults

- Source repo: active `AI-Agent-Skills` checkout root
- Installed Ceratops skill path: `$CODEX_HOME/skills/<skill-name>`
- Default release branch: `release/local`
- Runtime installer: `powershell -ExecutionPolicy Bypass -File .\\scripts\\install-skills.ps1`
- Installed Ceratops skills should be managed runtime copies with `.ceratops-runtime-manifest.json`.

## Skill-Specific Rules

- Ship from the runtime checkout's active `release/*` branch, not directly from a task worktree.
- If the runtime checkout is not on the intended release branch or the staged batch is not yet integrated there, stop and use `$ceratops-codex-skill-stage-release`.
- Validate every changed skill folder before shipping.
- Ensure `SKILL.md`, `agents/openai.yaml`, and any bundled resources stay aligned.
- Mandatory: Prefer running the repo installer when GH skills, copied helper scripts, contracts, templates, or install metadata changed; otherwise rebuild only the affected managed runtime skill copies when needed.
- Reuse the general GitHub ship flow rather than inventing a parallel release process.
- Restore the runtime checkout to synced `main`, remove the local `release/*` branch automatically when it is merged or tree-identical to `main`, and rerun the installer after merge; retain the release branch only with an explicit active-workflow reason.
- Remove low-risk stale task worktrees, task branches, unmanaged duplicate installed copies, stale release branches, or stale generated skill artifacts when safe.

## Script Bundle

- Runtime restore helper: `scripts/restore-runtime-main.ps1`

## Inputs To Capture

- Changed skill folders and whether each one is new, updated, metadata-only, or cleanup.
- Runtime checkout branch, staged release branch, PR or merge expectations, and validation expectations.
- Installed managed-copy expectations and any known exceptions.

## Boundaries

- Use this skill when working in the `AI-Agent-Skills` runtime checkout or another skill source repo with the same local runtime-install pattern.
- If the task is creating a brand-new Ceratops skill and not yet staged or shipped, stop and use `$ceratops-skill-create`.
- If the task is updating existing Ceratops skill contents and not yet staged or shipped, stop and use `$ceratops-skill-update`.
- If the runtime checkout is not yet staged on the intended `release/*` branch, stop and use `$ceratops-codex-skill-stage-release`.
- If the task is general repo shipping not focused on Codex skills and local skill installation, stop and use `$ceratops-gh-ship-change`.

## Workflow

### 1. Inspect staged skill scope

- Inspect the runtime checkout state, staged release branch, changed skill folders, installed managed-copy state, and any duplicated installed copies.
- Identify whether the work is a new skill, a skill update, a rename, a removal, metadata-only work, or cleanup.

### 2. Validate the staged release batch

- Confirm the runtime checkout is on the intended `release/*` branch and clean aside from deliberate staged commits.
- Run the skill validator for every changed skill.
- Check that `agents/openai.yaml` still matches the intended user-facing name, short description, and default prompt.
- Verify any referenced bundled resources exist and are actually needed.
- Mandatory: When the PR-readiness helper script or installer changed, prove the copied helper still runs with `python scripts/github_pr_readiness.py --help`.

### 3. Ship the staged repo change

- Use `$ceratops-gh-ship-change` from the runtime checkout when the staged release branch needs to be committed, pushed, PR'd, merged, and cleaned up.
- If GitHub deleted the remote `release/*` branch after a prior merge, recreate the same-named remote branch from the current local `release/*` branch instead of inventing a different remote branch name.
- Reuse an existing branch or PR when the staged release branch already has one.
- If the work is only validation or stale-state cleanup with no content changes, use `$ceratops-gh-repo-health-audit` instead.

### 4. Restore runtime `main`

- Run `scripts/restore-runtime-main.ps1` to switch the runtime checkout back to `main`, fast-forward from `origin/main`, drop the release branch when it is merged or tree-identical after a squash merge, and rerun the installer.
- Confirm the installed skill copy was regenerated from the runtime checkout on `main`.

### 5. Verify final installed state

- After merge, verify the runtime checkout is synced clean and the installed skill copy still has a current runtime manifest.
- Report any intentionally retained installed exceptions or repo leftovers.

## Completion Gate

- Verify every changed skill validates locally.
- Verify the repo change is merged or correctly blocked.
- Verify the runtime checkout ends on local `main` tracking `origin/main`, unless intentionally retained on a release branch.
- Verify no source task branch, source task worktree, or release branch remains unless an explicit active-workflow reason is reported.
- Verify each expected installed skill copy is managed by the runtime installer.
- Mandatory: Verify the relevant copied scripts and contract payloads exist in installed GH skill folders when the GH skill family was part of the run.

## Output Contract

Report only:

- changed skills
- unresolved blockers or non-blocking debt
- intentionally retained installed exceptions or repo leftovers with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-gh-codex-skill-ship to ship the staged Ceratops skill batch through GitHub, restore the runtime checkout to main, and verify the installed managed skill copies.`
