---
name: ceratops-gh-scripted-repo-publish
description: Create or harden a public GitHub repository with scripted live setting checks first, while preserving the original Ceratops GH publish skill family unchanged.
---

# Ceratops GH Scripted Repo Publish

Use the same first-time publish and hardening scope as `$ceratops-gh-repo-publish`, but prove live GitHub settings with the bundled helper scripts before closing.

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

## Inputs To Capture

- GitHub owner or org. Prefer `ceratops-code` only when user or existing org context explicitly indicates Ceratops ownership and access is available at no extra cost.
- Repo name, default branch, visibility, branch naming, and whether the repo should remain a fork.
- Maintainer merge policy: by Ceratops default, require 1 approving review on the default branch and add the authenticated maintainer account as the bypass actor so the owner can still self-ship; only choose a different review policy when the user explicitly asks for it.
- Package or image identity for the real deliverable: Docker, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or another relevant registry.
- Version source, release policy, tag style, changelog or release-note source, and first-release expectations.
- License intent, topics, CODEOWNERS owners, support route, and security reporting path.
- Local consumers of the project path such as shortcuts, automation configs, services, tests, docs, generated runtime paths, or Docker MCP overrides.

Infer the safest practical default unless the choice is risky, destructive, ambiguous, or credential-bound.

## Boundaries

- Use this skill for first-time publication, repo creation or forking, visibility decisions, initial hardening, and first release setup.
- If the repo already exists and only local changes or a normal release need shipping, stop and use `$ceratops-gh-scripted-repo-ship-change`.
- If the user only wants a state check, stale-item cleanup, or settings validation on an existing repo, stop and use `$ceratops-gh-scripted-repo-health-audit`.
- If only PR finalization remains, stop and use `$ceratops-gh-scripted-merge-pr`.

## Workflow

### 1. Inspect local state

- Inspect git state, tags, branches, remotes, ignored files, generated artifacts, README, license, CI files, docs, security files, manifests, lockfiles, package metadata, and existing release data.

### 2. Research and decide

- Check current official docs for GitHub community health, moderation, Actions, branch protection, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and the selected registry or packaging ecosystem.
- Compare 2-3 strong reference repos only when that will catch relevant missing repo structure, security, release, or packaging expectations for this project type.

### 3. Make the repo publishable

- Add or update only the relevant repo files and workflows for the project type.
- For first-time public repos, add the standard public-repo community files unless a stronger project-specific alternative already exists: `README`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, and at least one issue or pull-request intake template.
- Replace internal, misleading, or broken defaults before publication.

### 4. Configure GitHub and prove the result

- Create or fork the GitHub repo, push it, and verify the live endpoint.
- Turn off unused live features such as wiki or projects when the repo does not actually use them.
- Configure the default-branch review rule to require 1 approval and add the authenticated maintainer account to the bypass list unless the user explicitly asks for stricter review gating.
- Run the bundled repo-health script after GitHub settings changes and before closing publish work.
- Treat the script findings as the first source of truth for settings such as `content_reports_enabled`, branch protection, strict checks, required approvals, stale review dismissal, code scanning default setup, secret scanning, push protection, Dependabot security updates, delete-branch-on-merge, and auto-merge.
- For first-time public publish, also check the live community profile and do not close while the remaining gap is a safe standard-file addition you can still make directly.

### 5. Validate and publish

- Run the relevant local validation, ensure the latest relevant CI and code-scanning runs on the default branch are green, and publish the real external artifact only when the project actually has one.
- Verify live GitHub, release, and registry endpoints instead of trusting only local CLI success.
- If a single-maintainer fixture or sandbox repo needs one last hardening PR and GitHub self-approval rules would otherwise deadlock the run, you may temporarily lower required approvals just enough to merge that hardening PR, then immediately restore the intended review rule and verify the final live state.

### 6. Tag and release

- Create and push a release tag only when the repo is publishable and the version source is clear.
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

- Verify the final GitHub setting claims are backed by a fresh `python <resolved-helper-path> repo-health` run.
- Verify live review protection still shows `required_approving_review_count: 1` and the intended maintainer bypass actor unless the user explicitly chose a different merge policy.
- Verify live external state for every touched repo, protection rule, security setting, release, package, image, CI run, code scanning result, PR state, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact directory, cache, temp path, credential or config change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.

## Output Contract

Report only:

- what was created or changed
- exact GitHub repo URL and resolved owner or org
- exact release URL and pushed tags when relevant
- exact package or image URL, version, tag, and digest when relevant
- local install or pull verification result when relevant
- intentionally retained branches, PRs, temp files, or side effects with reasons
- remaining blocker, credential step, or paid requirement

## Example Invocation

`Use $ceratops-gh-scripted-repo-publish for this project. Publish it end-to-end to GitHub and the right public registry, and prove live GitHub settings with the bundled checks before closing.`
