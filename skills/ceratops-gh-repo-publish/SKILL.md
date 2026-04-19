---
name: ceratops-gh-repo-publish
description: Create, fork, or production-harden a local software project as a public GitHub repository and publish the correct public artifact registry output with Ceratops defaults. Use when Codex must inspect a local project, create or update a GitHub repo, preserve an upstream fork when appropriate, configure topics, branch protection, CODEOWNERS, security, CI, release tags, and publish Docker Hub images, PyPI packages, npm packages, Maven artifacts, NuGet packages, crates, RubyGems, PowerShell Gallery modules, GitHub Packages, or another ecosystem registry selected from the project type.
---

# Ceratops GH Repo Publish

## Overview

Turn a local project into a real public GitHub repository and the right published artifact with minimal back-and-forth. Use the free path by default, and prefer public visibility only after verifying the project is safe to expose.

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

- GitHub owner or org. Prefer `ceratops-code` only when user or existing org context explicitly indicates Ceratops ownership and access is available at no extra cost.
- Repo name, default branch, visibility, branch naming, and whether the repo should remain a fork.
- Package or image identity for the real deliverable: Docker, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or another relevant registry.
- Version source, release policy, tag style, changelog or release-note source, and first-release expectations.
- License intent, topics, CODEOWNERS owners, support route, and security reporting path.
- Local consumers of the project path such as shortcuts, automation configs, services, tests, docs, generated runtime paths, or Docker MCP overrides.

Infer the safest practical default unless the choice is risky, destructive, ambiguous, or credential-bound.

## Boundaries

- Use this skill for first-time publication, repo creation or forking, visibility decisions, initial hardening, and first release setup.
- If the repo already exists and only local changes or a normal release need shipping, stop and use `$ceratops-gh-repo-ship-change`.
- If the user only wants a state check, stale-item cleanup, or settings validation on an existing repo, stop and use `$ceratops-gh-repo-health-audit`.
- If only PR finalization remains, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect Local State

- Inspect git state, tags, branches, remotes, ignored files, generated artifacts, README, license, CI files, docs, security files, manifests, lockfiles, package metadata, and any existing release data.
- Identify the real build, lint, test, package, publish, and release commands from local files.
- Identify whether the project is a library, app, CLI, service, module, template, fork, or internal snapshot that needs cleanup before publishing.
- If renaming or moving anything, audit and update local consumers before closing.

### 2. Research And Decide

- Check current official docs for GitHub community health, Actions, branch protection, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and the selected registry or packaging ecosystem.
- Compare 2-3 strong current reference repos of the same project type when that will catch relevant missing repo structure, security, release, or packaging expectations.
- Select the actual distribution target from the project type instead of forcing Docker everywhere.
- Do not choose paid features unless they are already available at no extra cost.

### 3. Make The Repo Publishable

- Add or update only the relevant repo files for this project: `README`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, issue intake, pull request template, support routing, CI workflows, release or publish workflows, dependency update config, code scanning config, and install or run instructions.
- Replace upstream-specific, internal, misleading, or broken defaults before publication.
- Add ecosystem-standard manifests and metadata only when relevant to the actual project type.
- Prefer a real private reporting path for vulnerabilities and enable no-cost security controls when available and relevant.

### 4. Configure GitHub

- Create or fork the GitHub repo, preserve upstream linkage when needed, push the repo, and verify the live endpoint.
- Set precise topics. Keep `CODEOWNERS` minimal and accurate.
- Configure default-branch protection with real required checks, strict status checks, PR flow, stale review dismissal, conversation resolution, admin enforcement, no force pushes, and no deletions when available at no extra cost.
- Enable auto-merge and delete-branch-on-merge when compatible with the workflow.
- Verify branch protection, security controls, community health, moderation or reported-content health, and alert state from live endpoints. Do not assume repo-creation defaults already produced the intended moderation settings.

### 5. Validate And Publish

- Run the relevant local validation for the project: format, lint, tests, build, packaging, container build, generated-file refresh, and release validation.
- Ensure the latest relevant CI and code scanning runs on the default branch are green before closing.
- Publish the correct external artifact only when the project actually has one.
- Verify live GitHub, release, and registry endpoints instead of trusting only local CLI success.

### 6. Tag And Release

- Create and push an initial release tag only when the repo is publishable and the version source is clear.
- Prefer existing version metadata from manifests, release config, changelog, or tag series.
- Skip tagging when version semantics are unclear without invention, and report the skip precisely.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists. Do not prefer connector storage over normal local credential stores.

## Completion Gate

- Verify live external state for every touched repo, protection rule, security setting, release, package, image, CI run, code scanning result, PR state, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact directory, cache, temp path, credential/config change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.
- Ensure the local repo is clean on the default branch and tracking the remote default branch. If a squash merge or history rewrite would strand useful local work, keep one clearly named safety branch and report it.

## Output Contract

Report only:

- what was created or changed
- exact GitHub repo URL and resolved owner or org
- exact release URL and pushed tags when relevant
- exact package or image URL, version, tag, and digest when relevant
- local install or pull verification result when relevant
- intentionally retained branches, PRs, temp files, or side effects with reasons
- remaining blocker, credential step, or paid requirement

## Example Invocations

`Use $ceratops-gh-repo-publish for this project. Publish it end-to-end to public GitHub and the right public registry. Use the free path by default.`

`Use $ceratops-gh-repo-publish for this project. Owner: ceratops-code. Topics: asar, automation, codex, electron, powershell, windows.`

`Use $ceratops-gh-repo-publish for this project. It is a Python library, so publish it to GitHub and PyPI.`
