---
name: ceratops-gh-repo-ship-change
description: Ship local repository changes through GitHub and any relevant artifact registry with Ceratops defaults. Use when Codex needs to inspect a dirty repo, update docs, metadata, README, SECURITY, tags, versions, package manifests, CI, tests, changelog, release notes, branch protection impact, open a PR, fix CI, merge or auto-merge, publish Docker, PyPI, npm, Maven, NuGet, crates, RubyGems, PowerShell Gallery, GitHub Packages, or other changed artifacts, install or pull the published artifact locally, and clean up branches and stale state.
---

# Ceratops GH Repo Ship Change

## Overview

Take an existing published repo from local changes to a verified merged result. Publish external artifacts only when the change affects a releasable package, image, module, binary, or other public artifact.

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

## Inputs To Capture

- Intended change scope, issue or PR reference, target branch, repo owner and name, and merge preference.
- Version bump, tag, release-note, changelog, and artifact-publish expectations.
- Affected ecosystems and registries, if any.
- Required local checks, CI checks, security gates, branch protection, release workflow, and package verification commands.
- Topics, CODEOWNERS, SECURITY instructions, README examples, and local consumer paths affected by the change.

Infer missing inputs from local files and live repo state before asking.

## Boundaries

- Use this skill when the repo already exists and there are actual local changes to complete, merge, and optionally release.
- If the repo is not yet published or lacks a usable remote, stop and use `$ceratops-gh-repo-publish`.
- If the task is only repo validation or stale-state cleanup with no content changes, stop and use `$ceratops-gh-repo-health-audit`.
- If only PR finalization remains and no content changes are needed, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect State And Scope

- Inspect git status, diff, untracked files, remotes, current branch, upstream, open PRs, tags, releases, CI config, manifests, lockfiles, docs, generated files, and registry metadata.
- Identify whether the change is code, docs, config, dependency, release, packaging, security, CI, or generated-artifact work.
- Confirm no secrets, private data, machine-local paths, or internal-only references are being introduced.
- Reuse an existing branch or PR when appropriate instead of creating duplicates.

### 2. Research Current Standards

- Check current official docs for GitHub PR, Actions, security, release behavior, and any touched registry or package-manager workflow.
- Compare 2-3 strong reference repos only when that will catch expected docs, security, CI, release, or packaging updates for this repo type.

### 3. Complete The Change

- Finish in-scope code, docs, tests, generated files, and packaging metadata needed for the change to be coherent.
- Add regression tests or regression checks for meaningful behavior fixes or behavior changes.
- Update README, examples, install or run commands, SECURITY, CONTRIBUTING, changelog, release notes, package metadata, topics, CODEOWNERS, and CI only when the change makes them stale.

### 4. Validate Locally

- Run the relevant local checks: format, lint, tests, smoke tests, build, packaging, generated-file checks, container build, or security checks.
- For packages, build local artifacts and install or consume them locally before publishing.
- For images, build locally and run a smoke test before publishing.
- Fix in-scope failures instead of stopping at the first error.

### 5. PR, CI, And Merge

- Create or update a branch and commit intentionally.
- Push the branch and create or update a PR with concise change and validation evidence.
- Wait for required CI, code scanning, and branch protection checks, and fix in-scope failures.
- Merge or enable auto-merge only when checks, reviews, and conversations allow it.
- Delete the branch when safe, sync the local default branch, prune stale refs, and keep a safety branch only when needed.
- If the repo is public and the run touches repo settings, release posture, or reports repo or process health, inspect the live community profile including moderation or reported-content health before closing.

### 6. Publish Artifacts When Relevant

- Determine whether the merged change requires a release, tag, package, image, or other registry publish.
- Use the current official release flow for the relevant ecosystem.
- Derive versions from trustworthy project metadata and tag history instead of inventing semantics.
- Verify live registry endpoints, tags, digests, package pages, release pages, and artifacts when a publish actually happens.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify live GitHub state for the PR, merge, checks, code scanning, branch protection, tags, release, branch deletion, and default branch.
- Verify live registry state for every published artifact and verify local install, pull, or consumption when relevant.
- Verify local state: clean worktree on the default branch, remotes, refs, generated files, artifacts, temp paths, caches, credential changes, and local consumer paths.

## Output Contract

Report only:

- changed scope and PR URL
- merge state and final commit
- checks run and live CI or security result
- release or tag URL when relevant
- artifact version, digest, package details, and local verification result when relevant
- intentionally retained branches, PRs, files, temp paths, or side effects with reasons
- exact blocker, credential step, or paid requirement

## Example Invocations

`Use $ceratops-gh-repo-ship-change to ship the current changes, merge the PR, publish any changed artifact, and verify it locally.`

`Use $ceratops-gh-repo-ship-change. This is a Python CLI change; update packaging and docs, publish to PyPI if a release is required, install it locally, and verify the command works.`
