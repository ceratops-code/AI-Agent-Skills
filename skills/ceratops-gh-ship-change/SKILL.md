---
name: ceratops-gh-ship-change
description: Ship local repository changes through GitHub and any relevant artifact registry with Ceratops defaults, using scripted live repo and PR checks before merge decisions.
---

# Ceratops GH Ship Change

Take an existing published repo from local changes to a verified merged result. Publish external artifacts only when the change affects a releasable package, image, module, binary, or other public artifact. Verify machine-checkable GitHub state through the bundled helper scripts before trusting prose or stale screenshots.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- On every run, check current official docs for unstable standards and use 2-3 strong current reference repos when useful.
- If runtime research reveals a durable missing general rule, update this `SKILL.md`, validate the skill, and report the maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- When a skill touches a public GitHub repo and reports repo, security, maturity, or process health, inspect the live community profile and equivalent no-cost moderation or community-health signals instead of inferring health from files, CI, or alert counts alone.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper path relative to this skill: `..\ceratops-gh-runtime\scripts\gh_live_checks.py`
- Repo settings check: `python <resolved-helper-path> repo-health --repo OWNER/REPO`
- PR readiness check: `python <resolved-helper-path> pr-readiness --pr NUMBER_OR_URL`

## Inputs To Capture

- Intended change scope, issue or PR reference, target branch, repo owner and name, and merge preference.
- Version bump, tag, release-note, changelog, and artifact-publish expectations.
- Affected ecosystems and registries, if any.
- Required local checks, CI checks, security gates, branch protection, release workflow, and package verification commands.
- Whether the run touches GitHub Actions workflows or repo Actions permissions, and whether the repo already enforces SHA pinning.
- Topics, CODEOWNERS, SECURITY instructions, README examples, and local consumer paths affected by the change.

Infer missing inputs from local files and live repo state before asking.

## Boundaries

- Use this skill when the repo already exists and there are actual local changes to complete, merge, and optionally release.
- If the repo is not yet published or lacks a usable remote, stop and use `$ceratops-gh-repo-create-and-publish`.
- If the task is only repo validation or stale-state cleanup with no content changes, stop and use `$ceratops-gh-repo-health-audit`.
- If only PR finalization remains and no content changes are needed, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect state and scope

- Inspect git status, diff, untracked files, remotes, current branch, upstream, open PRs, tags, releases, CI config, manifests, lockfiles, docs, generated files, and registry metadata.
- Identify whether the change is code, docs, config, dependency, release, packaging, security, CI, or generated-artifact work.
- Confirm no secrets, private data, machine-local paths, or internal-only references are being introduced.
- Reuse an existing branch or PR when appropriate instead of creating duplicates.

### 2. Research current standards

- Check current official docs for GitHub PR, Actions, security, release behavior, and any touched registry or package-manager workflow.
- Compare 2-3 strong reference repos only when that will catch expected docs, security, CI, release, or packaging updates for this repo type.

### 3. Prove live GitHub state with scripts

- Run the bundled repo-health script whenever the run touches repo settings, release posture, or repo-health claims, including review-policy or code-scanning expectations.
- Run the bundled PR-readiness script before merge or auto-merge decisions instead of relying on prose summaries of checks, reviews, or mergeability.
- Re-run the relevant script after any live GitHub change that could invalidate the prior result.

### 4. Complete the change

- Finish in-scope code, docs, tests, generated files, and packaging metadata.
- If the run touches workflow files or GitHub Actions settings, pin every non-local action in the changed workflows to a verified full SHA with a same-line version comment and do not introduce new mutable refs.
- Add regression tests or regression checks for meaningful behavior fixes or behavior changes.
- Update README, examples, install or run commands, SECURITY, CONTRIBUTING, changelog, release notes, package metadata, topics, CODEOWNERS, and CI only when the change makes them stale.

### 5. Validate locally

- Run the relevant local checks: format, lint, tests, smoke tests, build, packaging, generated-file checks, container build, or security checks.
- For packages, build local artifacts and install or consume them locally before publishing.
- For images, build locally and run a smoke test before publishing.
- Fix in-scope failures instead of stopping at the first error.

### 6. PR, CI, and merge

- Create or update a branch and commit intentionally.
- Push the branch and create or update a PR with concise change and validation evidence.
- Wait for required CI, code scanning, and branch protection checks, and fix in-scope failures.
- Use the live script findings plus current GitHub state to decide whether to merge now, enable auto-merge, or stop on a blocker.
- When this skill merges the PR directly, use `gh pr merge --admin` with the allowed merge-method flag and `--delete-branch` when cleanup is intended and allowed.
- Use `gh pr merge --auto` only when GitHub should wait for remaining requirements instead of closing the PR immediately.
- Delete the branch when safe, remove any temporary worktree created for the run after its branch is no longer needed, sync the local default branch, prune stale refs, and keep a safety branch only when needed.
- If the repo is public and the run touches repo settings, release posture, or reports repo or process health, inspect the live community profile including moderation or reported-content health before closing.

### 7. Publish artifacts when relevant

- Determine whether the merged change requires a release, tag, package, image, or other registry publish.
- Use the current official release flow for the relevant ecosystem.
- Derive versions from trustworthy project metadata and tag history instead of inventing semantics.
- Publish external artifacts only when the merged change affects a releasable artifact.
- Verify live registry endpoints, tags, digests, package pages, release pages, and artifacts when a publish actually happens.
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
- Verify live registry state for every published artifact and verify local install, pull, or consumption when relevant.
- Verify changed workflow files still use the intended full-SHA action refs when the run touched GitHub Actions workflows or settings.
- Verify local state: default branch, worktree, remotes, refs, generated files, artifacts, temp paths, caches, credential changes, and local consumer paths.
- Verify any temporary branch or worktree created for the run was removed unless intentionally retained.

## Output Contract

Report only:

- overall shipping outcome
- released or published artifact details when materially relevant to downstream use
- unresolved blockers or non-blocking debt
- intentionally retained branches, PRs, files, temp paths, or side effects with reasons
- anything important not verified
- exact credential step or paid requirement if blocked

## Example Invocation

`Use $ceratops-gh-ship-change to ship these local changes through GitHub with the bundled live checks, publish any relevant artifacts, verify them locally, and clean up state.`
