---
name: ceratops-gh-scripted-repo-ship-change
description: Ship local repository changes through GitHub with scripted live repo and PR checks first, while keeping the original Ceratops GH ship skill intact as a separate variant.
---

# Ceratops GH Scripted Repo Ship Change

Use the same shipping scope as `$ceratops-gh-repo-ship-change`, but verify machine-checkable GitHub state through the bundled helper scripts before trusting prose or stale screenshots.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- On every run, check current official docs for unstable standards and use 2-3 strong current reference repos when useful.
- If runtime research reveals a durable missing general rule, update this `SKILL.md`, validate the skill, and report the maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local state and local auth before asking for credentials or making assumptions.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- When a skill touches a public GitHub repo and reports repo, security, maturity, or process health, inspect the live community profile and equivalent no-cost moderation or community-health signals instead of inferring health from files, CI, or alert counts alone.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper path relative to this skill: `..\ceratops-gh-scripted-runtime\scripts\gh_live_checks.py`
- Repo settings check: `python <resolved-helper-path> repo-health --repo OWNER/REPO`
- PR readiness check: `python <resolved-helper-path> pr-readiness --pr NUMBER_OR_URL`

## Inputs To Capture

- Intended change scope, issue or PR reference, target branch, repo owner and name, and merge preference.
- Version bump, tag, release-note, changelog, and artifact-publish expectations.
- Affected ecosystems and registries, if any.
- Required local checks, CI checks, security gates, branch protection, release workflow, and package verification commands.
- Topics, CODEOWNERS, SECURITY instructions, README examples, and local consumer paths affected by the change.

Infer missing inputs from local files and live repo state before asking.

## Boundaries

- Use this skill when the repo already exists and there are actual local changes to complete, merge, and optionally release.
- If the repo is not yet published or lacks a usable remote, stop and use `$ceratops-gh-scripted-repo-publish`.
- If the task is only repo validation or stale-state cleanup with no content changes, stop and use `$ceratops-gh-scripted-repo-health-audit`.
- If only PR finalization remains and no content changes are needed, stop and use `$ceratops-gh-scripted-merge-pr`.

## Workflow

### 1. Inspect state and scope

- Inspect git status, diff, untracked files, remotes, current branch, upstream, open PRs, tags, releases, CI config, manifests, lockfiles, docs, generated files, and registry metadata.

### 2. Prove live GitHub state with scripts

- Run the bundled repo-health script whenever the run touches repo settings, release posture, or repo-health claims, including review-policy or code-scanning expectations.
- Run the bundled PR-readiness script before merge or auto-merge decisions instead of relying on prose summaries of checks, reviews, or mergeability.
- Re-run the relevant script after any live GitHub change that could invalidate the prior result.

### 3. Complete and validate the change

- Finish in-scope code, docs, tests, generated files, and packaging metadata.
- Run the relevant local checks and fix in-scope failures instead of stopping at the first error.

### 4. PR, CI, and merge

- Create or update a branch and PR with concise validation evidence.
- Use the live script findings plus current GitHub state to decide whether to merge now, enable auto-merge, or stop on a blocker.

### 5. Publish and close

- Publish external artifacts only when the merged change affects a releasable artifact.
- Re-run the repo-health script after any live GitHub setting change and the PR-readiness script immediately before the final merge action.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify the merge decision is backed by a fresh `python <resolved-helper-path> pr-readiness` run.
- Verify live GitHub state for the repo with `python <resolved-helper-path> repo-health` when repo settings or process health were part of the run.
- Verify local state: default branch, worktree, remotes, refs, generated files, artifacts, temp paths, caches, credential changes, and local consumer paths.

## Output Contract

Report only:

- changed scope and PR URL
- merge state and final commit
- checks run and live CI or security result
- release or tag URL when relevant
- artifact version, digest, package details, and local verification result when relevant
- intentionally retained branches, PRs, files, temp paths, or side effects with reasons
- exact blocker, credential step, or paid requirement

## Example Invocation

`Use $ceratops-gh-scripted-repo-ship-change to ship these local changes through GitHub with the bundled live checks, publish any relevant artifacts, verify them locally, and clean up state.`
