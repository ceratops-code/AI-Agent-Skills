---
name: ceratops-gh-codex-skill-ship
description: Ship Ceratops or other local Codex skill changes from the runtime checkout's staged `release/*` branch through GitHub and back to the installed runtime on `main`. Use when Codex should validate staged skill changes, confirm the runtime checkout is on the intended release branch, publish the batch through GitHub, then restore the runtime checkout and installed skills to synced `main`.
---

# Ceratops GH Codex Skill Ship

Ship a staged Ceratops skill batch through GitHub, then restore the runtime checkout and installed skill state to clean `main`.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Blocking: Reuse fresh sufficient same-run evidence across adjacent, resumed, or chained workflows when it still proves the current decision; do not reacquire evidence or rerun checks solely to refresh already-sufficient evidence unless state is uncertain, plausibly changed, externally mutable for the decision, materially broadened, or required fresh by a higher-precedence instruction, skill, automation, or completion gate.
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
- Local GH helper package install command: `python -m pip install --editable .`
- Ceratops-installed skills should resolve through junctions to the source repo unless there is a documented exception.

## Skill-Specific Rules

- Ship from the runtime checkout's active `release/*` branch, not directly from a task worktree.
- If the runtime checkout is not on the intended release branch or the staged batch is not yet integrated there, stop and use `$ceratops-codex-skill-stage-release`.
- Validate every changed skill folder before shipping.
- Ensure `SKILL.md`, `agents/openai.yaml`, and any bundled resources stay aligned.
- Prefer running the repo installer when GH skills, the GH helper package, or install metadata changed; otherwise repair the local installed junctions directly when needed.
- Reuse the general GitHub ship flow rather than inventing a parallel release process.
- Restore the runtime checkout to synced `main`, remove the local `release/*` branch automatically when it is merged or tree-identical to `main`, and rerun the installer after merge; retain the release branch only with an explicit active-workflow reason.
- Remove low-risk stale task worktrees, task branches, installed copies, stale junctions, stale release branches, or stale generated skill artifacts when safe.

## Script Bundle

- Runtime restore helper: `scripts/restore-runtime-main.ps1`

## Inputs To Capture

- Changed skill folders and whether each one is new, updated, metadata-only, or cleanup.
- Runtime checkout branch, staged release branch, PR or merge expectations, and validation expectations.
- Installed junction expectations and any known exceptions.

## Boundaries

- Use this skill when working in the `codex-skills` runtime checkout or another skill source repo with the same local runtime-install pattern.
- If the task is creating a brand-new Ceratops skill and not yet staged or shipped, stop and use `$ceratops-skill-create`.
- If the task is updating existing Ceratops skill contents and not yet staged or shipped, stop and use `$ceratops-skill-update`.
- If the runtime checkout is not yet staged on the intended `release/*` branch, stop and use `$ceratops-codex-skill-stage-release`.
- If the task is general repo shipping not focused on Codex skills and local skill installation, stop and use `$ceratops-gh-ship-change`.

## Workflow

### 1. Inspect staged skill scope

- Inspect the runtime checkout state, staged release branch, changed skill folders, installed junction state, and any duplicated installed copies.
- Identify whether the work is a new skill, a skill update, a rename, a removal, metadata-only work, or cleanup.

### 2. Validate the staged release batch

- Confirm the runtime checkout is on the intended `release/*` branch and clean aside from deliberate staged commits.
- Run the skill validator for every changed skill.
- Check that `agents/openai.yaml` still matches the intended user-facing name, short description, and default prompt.
- Verify any referenced bundled resources exist and are actually needed.
- When the GH helper package or installer changed, prove the packaged runtime still imports with `python -m ceratops_gh_current_state --help`.

### 3. Ship the staged repo change

- Use `$ceratops-gh-ship-change` from the runtime checkout when the staged release branch needs to be committed, pushed, PR'd, merged, and cleaned up.
- If GitHub deleted the remote `release/*` branch after a prior merge, recreate the same-named remote branch from the current local `release/*` branch instead of inventing a different remote branch name.
- Reuse an existing branch or PR when the staged release branch already has one.
- If the work is only validation or stale-state cleanup with no content changes, use `$ceratops-gh-repo-health-audit` instead.

### 4. Restore runtime `main`

- Run `scripts/restore-runtime-main.ps1` to switch the runtime checkout back to `main`, fast-forward from `origin/main`, drop the release branch when it is merged or tree-identical after a squash merge, and rerun the installer.
- Confirm the installed skill path resolves to the runtime checkout on `main`.

### 5. Verify final installed state

- After merge, verify the runtime checkout is synced clean and the installed skill path still resolves correctly.
- Report any intentionally retained installed exceptions or repo leftovers.

## Completion Gate

- Verify every changed skill validates locally.
- Verify the repo change is merged or correctly blocked.
- Verify the runtime checkout ends on local `main` tracking `origin/main`, unless intentionally retained on a release branch.
- Verify no source task branch, source task worktree, or release branch remains unless an explicit active-workflow reason is reported.
- Verify each expected installed junction resolves to the runtime checkout.
- Verify the GH helper package resolves from the runtime checkout when the GH skill family was part of the run.

## Output Contract

Report only:

- changed skills
- unresolved blockers or non-blocking debt
- intentionally retained installed exceptions or repo leftovers with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-gh-codex-skill-ship to ship the staged Ceratops skill batch through GitHub, restore the runtime checkout to main, and verify the installed skills resolve there.`
