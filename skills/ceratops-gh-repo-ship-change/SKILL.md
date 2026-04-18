---
name: ceratops-gh-repo-ship-change
description: Ship local repository changes through GitHub and any relevant artifact registry with Ceratops defaults. Use when Codex needs to inspect a dirty repo, update docs, metadata, README, SECURITY, tags, versions, package manifests, CI, tests, changelog, release notes, branch protection impact, open a PR, fix CI, merge or auto-merge, publish Docker, PyPI, npm, Maven, NuGet, crates, RubyGems, PowerShell Gallery, GitHub Packages, or other changed artifacts, install or pull the published artifact locally, and clean up branches and stale state.
---

# Ceratops GH Repo Ship Change

## Overview

Take an existing published repo from local changes to a verified merged result. Publish external artifacts only when the change affects a releasable package, image, module, binary, or registry-visible output.

## Hard Requirements

- Treat every bullet in `Hard Requirements`, `Inputs To Capture`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract` as mandatory unless explicitly inapplicable.
- Before completion, re-open this `SKILL.md` and run a line-by-line closure pass over every mandatory bullet. Classify each item internally as satisfied, not applicable with reason, blocked with exact blocker, or intentionally retained side effect.
- Keep this checklist explicit and living. For every run, check current official docs and, when useful, 2-3 strong current reference repos of the same type. If runtime research reveals a durable, broadly relevant missing repo, packaging, security, release, or registry expectation, update this `SKILL.md`, validate the skill, and report the maintenance.
- Inspect local worktree, repo, remotes, branch, existing PRs, package manifests, registry config, CI, and auth before deciding the shipping path.
- Preserve user changes. Do not overwrite, reset, squash, delete, or rebase work destructively without explicit approval.
- If the repo is not yet published or lacks a usable GitHub remote, switch to the publish workflow instead of faking a ship flow.
- Update user-facing and maintainer-facing files that are affected by the change: README, SECURITY, CONTRIBUTING, release notes, changelog, package metadata, Docker docs, install commands, examples, topics, CODEOWNERS, CI, and security config as relevant.
- Run the real project checks needed for confidence before PR merge and before publishing artifacts.
- Merge through PR flow unless the repo policy explicitly permits direct pushes and the user asked for them.
- Publish changed artifacts only when relevant and verify them from real endpoints plus local install, pull, or consumption.
- Stop only for missing credentials after local checks, failing required checks that cannot be fixed safely, merge conflicts, ambiguous release/version choice, destructive risk, paid requirements, security issue, or ownership ambiguity.

## Inputs To Capture

- Intended change scope, issue or PR reference, target branch, repo owner/name, and merge preference.
- Version bump, tag, release-note, changelog, and artifact-publish expectations.
- Affected ecosystems and registries: Docker Hub, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or project-specific registries.
- Required local checks, CI checks, security gates, branch protection, release workflow, and package verification commands.
- GitHub topics, CODEOWNERS, SECURITY instructions, README examples, and local consumer paths affected by the change.

Infer missing inputs from local files and live repo state before asking.

## Workflow

### 1. Inspect State And Scope

- Inspect git status, diff, untracked files, remotes, current branch, upstream, open PRs, tags, releases, CI config, package manifests, lockfiles, Dockerfiles, docs, generated files, and registry metadata.
- Identify whether changes are code, docs, config, dependency, release, packaging, security, CI, or generated-artifact changes.
- Confirm no secrets, private data, machine-local paths, or internal-only references are being introduced.
- Detect existing PRs for the branch or same work and reuse them when appropriate instead of creating duplicates.

### 2. Research Current Standards

- Check current official docs for GitHub PR/Actions/security/release behavior, the relevant package manager, and each touched registry or publishing workflow.
- Compare 2-3 strong reference repos only when it helps catch expected docs, security, CI, release, or packaging updates for this project type.
- Apply newly current expectations only when relevant and no-cost. Skip outdated, heavy, paid, or irrelevant practices and report the skip when meaningful.

### 3. Complete The Change

- Finish in-scope code, docs, tests, generated files, and packaging metadata needed for the change to be coherent.
- Add or update regression tests for bug fixes and meaningful behavior changes.
- Update README, examples, install/run commands, SECURITY, CONTRIBUTING, changelog, release notes, package metadata, Docker docs, topics, CODEOWNERS, and CI only when the change makes them stale or incomplete.
- Refresh lockfiles, generated files, schemas, catalogs, Docker MCP overrides, or profile files when they are part of the project contract.
- Verify labels referenced by issue forms or templates exist when the change adds or edits those templates.
- Keep repo-specific cleanup separate from official requirements in the final reasoning.

### 4. Validate Locally

- Run format, lint, tests, smoke tests, build, packaging, container build, generated-file checks, and security checks relevant to the changed files.
- For packages, build local artifacts and install or consume them locally before publishing.
- For images, build locally and run a smoke test before publishing.
- Distinguish broken security controls from non-blocking maturity or process alerts such as Scorecard-only signals. Report retained items and the not-performed work explicitly instead of collapsing them into a generic shipped/healthy result.
- Fix in-scope failures instead of stopping at the first error. Classify unrelated or pre-existing failures precisely.

### 5. PR, CI, And Merge

- Create or update a branch and commit with an intentional message.
- Push the branch and create or update a PR with concise description, test evidence, release impact, and artifact impact.
- Wait for required CI, code scanning, and branch protection checks. Fix failures that are in scope.
- Merge or enable auto-merge only when branch protection, checks, reviews, and conversations allow it.
- Delete the branch when safe, sync the local default branch, prune stale refs, and keep a safety branch only when needed to preserve reachable work.

### 6. Publish Artifacts When Relevant

- Determine whether the merged change requires a release, tag, package, image, or other registry publish.
- Use the ecosystem's current official release and publishing flow. Examples include Docker Hub, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, app stores, or project-specific registries.
- Derive versions from trustworthy project metadata and tag history. Do not invent semantics when versioning is ambiguous.
- Publish only after the merge target is correct and required checks are green, unless the repo's official release flow intentionally publishes from the PR or tag.
- Verify live registry endpoints, tags, digests, package pages, release pages, and artifacts.
- For public registry artifacts published from a git tag, create or verify a GitHub release for that tag unless the repo has an explicit tags-only policy; include artifact URLs, tags, and digests or package identifiers in the release notes.
- For Docker MCP replacement images, import the override when locally applicable, verify active runtime tool annotations from the MCP client or Docker MCP CLI, and run at least one safe read-only tool call when credentials/config are available.
- Install, pull, or consume the published artifact locally using the public endpoint or intended registry endpoint.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Re-open this `SKILL.md` and validate the work line by line against every mandatory section.
- Verify live GitHub state: PR, merge, checks, code scanning, branch protection, tags, release, branch deletion, and default branch.
- Verify live registry state for every published artifact and verify local install, pull, or consumption.
- Verify local state: clean worktree on default branch, remotes, refs, generated files, artifacts, temp paths, caches, credential/config changes, and local consumer paths.
- Classify every touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked with exact blocker.
- If anything mandatory is unmet or unverifiable, report the blocker instead of claiming completion.

## Output Contract

Report only:

- changed scope and PR URL
- merge state and final commit
- checks run and live CI/security result
- release/tag and registry URLs when relevant
- artifact version, image digest, package details, and local verification result when relevant
- intentionally retained branches, PRs, files, temp paths, or side effects with reasons
- exact blocker, credential step, or paid requirement if blocked

## Example Invocations

`Use $ceratops-gh-repo-ship-change to ship the current changes, merge the PR, publish any changed artifact, and verify it locally.`

`Use $ceratops-gh-repo-ship-change. This is a Python CLI change; update packaging/docs, publish to PyPI if a release is required, install it locally, and verify the command works.`
