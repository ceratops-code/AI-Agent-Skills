---
name: ceratops-gh-codex-skill-ship
description: Ship Ceratops or other local Codex skill changes from the runtime checkout's staged `release/*` branch through GitHub and back to the installed runtime on `main`. Use when Codex should validate staged skill changes, confirm the runtime checkout is on the intended release branch, publish the batch through GitHub, then restore the runtime checkout and installed skills to synced `main`.
---

# Ceratops GH Codex Skill Ship

Ship a staged Ceratops skill batch through GitHub, then restore the runtime checkout and installed skill state to clean `main`.

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

- Source repo: active `AI-Agent-Skills` checkout root
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

- Use this skill when working in the `AI-Agent-Skills` runtime checkout or another skill source repo with the same local runtime-install pattern.
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
