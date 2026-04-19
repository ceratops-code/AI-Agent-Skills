---
name: ceratops-gh-repo-health-audit
description: Audit and repair GitHub repository health with Ceratops defaults. Use when Codex needs to validate that a repo has no unpublished local changes, stale PRs, stale branches, stale tags, stale releases, outdated README or SECURITY instructions, wrong topics, stale CODEOWNERS, missing branch protection, failing CI, stale dependency config, missing security controls, unverified packages or images, old registry artifacts, local path leftovers, or other repo hygiene gaps.
---

# Ceratops GH Repo Health Audit

## Overview

Validate that an existing GitHub repo is clean, current, secure, documented, published, and not carrying leftover workflow debris. Apply low-risk safe fixes directly and report risky, ambiguous, destructive, paid, or credential-bound fixes precisely.

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

- Repo owner or name, default branch, intended visibility, intended owner or org, and whether Ceratops ownership is actually desired.
- Expected artifacts and registries, if any.
- Expected branch protection, CI checks, release policy, dependency update policy, security posture, topics, CODEOWNERS, and support path.
- Local repo path, local consumer paths, generated files, shortcuts, services, shell profiles, Docker MCP overrides, and automation configs tied to the repo.

Infer missing inputs from live repo state and local files before asking.

## Boundaries

- Use this skill when the task is primarily validation, stale-state cleanup, or safe repo-health repair.
- If the repo is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-repo-publish`.
- If a safe fix turns into a content change that should go through normal PR and release flow, stop audit-only mode and use `$ceratops-gh-repo-ship-change`.
- If only PR finalization remains after prior fixes, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect Local And Live State

- Inspect git status, remotes, branches, refs, tags, releases, generated files, artifacts, temp paths, package outputs, and local consumer references.
- Inspect live GitHub repo metadata, topics, description, default branch, open PRs, branches, tags, releases, Actions runs, code scanning, Dependabot, security settings, branch protection, rulesets, and community profile.
- For public repos, inspect live community-profile moderation signals such as reported-content health and `content_reports_enabled`, not just file completeness and security alerts.
- Inspect published packages or images relevant to the repo.

### 2. Research Current Standards

- Check current official docs for GitHub community health, branch protection or rulesets, Actions, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and each relevant ecosystem or registry.
- Compare 2-3 strong current reference repos when that will help identify expected files, metadata, workflows, security controls, or release patterns for this repo type.

### 3. Audit Repo Health

- Verify README accuracy, install or run instructions, release notes, changelog, support path, and registry links.
- Verify `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, issue intake, pull request template, support routing, CI, release workflows, dependency update automation, and code scanning config when relevant.
- Verify public repo security posture: private vulnerability reporting or an explicit private reporting path, Dependabot security updates, secret scanning, push protection, code scanning, dependency graph, and current alert state when available at no extra cost.
- Verify default-branch protection with real checks, strict status checks, PR flow, review policy, stale review dismissal, conversation resolution, admin enforcement, no force pushes, and no deletions as appropriate for the repo.
- Verify topics are precise and current, and CODEOWNERS contains only valid current owners.
- Verify versions, tags, releases, package metadata, image digests, and latest-release pointers match intended state.
- Audit the repo end to end for open security, code-scanning, maturity, and process alerts from GitHub, CI, dependency tooling, scorecards, and equivalent live signals relevant to the repo.
- Decide whether each alert is safe, fix low-risk items directly, and for every alert left open report its name or id, blocking status, why it is not being fixed now, and the concrete work needed to clear it.
- Verify no stale PRs, branches, tags, releases, generated files, local path references, or old automation references remain unclassified.

### 4. Repair Safe Gaps

- Apply low-risk fixes such as doc link updates, README command corrections, SECURITY clarification, topic cleanup, stale CODEOWNERS correction, missing ignore files, obvious CI metadata correction, dependency config cleanup, branch deletion for already-merged unprotected branches, and local ref pruning.
- Open or update a PR for repo changes when branch protection or repo policy requires it.
- Do not delete tags, releases, packages, protected branches, backup branches, or external artifacts unless the stale classification is proven and the action is safe or explicitly approved.

### 5. Validate

- Run the local checks needed to prove safe fixes did not break the repo.
- Verify live GitHub and registry state after each external change.
- Re-check PRs, branches, releases, tags, security settings, CI, code scanning, topics, community files, package endpoints, and local cleanliness after fixes.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify live state for every touched repo setting, security control, branch protection rule, PR, branch, tag, release, workflow, code scanning result, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact, temp path, cache, credential change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.

## Output Contract

Report only:

- health gaps fixed
- alerts fixed and alerts left open with name or id, blocking status, why they remain open, and the concrete work needed to clear them
- health gaps intentionally retained with exact reasons
- remaining blockers or credential steps
- live GitHub, security, CI, release, and registry verification results
- branches, PRs, tags, releases, local paths, temp paths, or artifacts removed or retained
- paid requirement with product, reason, and price if encountered

## Example Invocations

`Use $ceratops-gh-repo-health-audit for this repo. Fix safe repo-health gaps and report only real blockers.`

`Use $ceratops-gh-repo-health-audit. Verify no stale PRs, branches, tags, releases, registry artifacts, stale docs, or security gaps remain.`
