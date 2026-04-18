---
name: ceratops-gh-repo-health-audit
description: Audit and repair GitHub repository health with Ceratops defaults. Use when Codex needs to validate that a repo has no unpublished local changes, stale PRs, stale branches, stale tags, stale releases, outdated README or SECURITY instructions, wrong topics, stale CODEOWNERS, missing branch protection, failing CI, stale dependency config, missing security controls, unverified packages or images, old registry artifacts, local path leftovers, or other repo hygiene gaps.
---

# Ceratops GH Repo Health Audit

## Overview

Validate that an existing GitHub repo is clean, current, secure, documented, published, and not carrying leftover workflow debris. Apply safe fixes directly; report risky, ambiguous, destructive, paid, or credential-bound fixes precisely.

## Hard Requirements

- Treat every bullet in `Hard Requirements`, `Inputs To Capture`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract` as mandatory unless explicitly inapplicable.
- Before completion, re-open this `SKILL.md` and run a line-by-line closure pass over every mandatory bullet. Classify each item internally as satisfied, not applicable with reason, blocked with exact blocker, or intentionally retained side effect.
- Keep this checklist explicit and living. For every run, check current official docs and, when useful, 2-3 strong current reference repos of the same type. If runtime research reveals a durable, broadly relevant missing repo-health, security, release, packaging, or registry expectation, update this `SKILL.md`, validate the skill, and report the maintenance.
- Inspect both local and live GitHub state before concluding the repo is healthy or stale.
- Verify current state from real endpoints rather than trusting local config, old docs, or previous run notes.
- Apply only low-risk safe fixes without asking. Stop and report before destructive deletions, irreversible release/tag changes, ownership changes, paid features, or ambiguous policy changes.
- Do not call the repo healthy while actionable workflow PRs, stale setup branches, unpublished changes, failing required checks, stale docs, missing security reporting, or unverified artifacts remain unclassified.
- Preserve rollback branches, release tags, and historical artifacts when there is a plausible reproducibility or rollback reason; classify why they remain.

## Inputs To Capture

- Repo owner/name, default branch, intended visibility, intended owner or org, and whether `ceratops-code` should own Ceratops repos.
- Expected artifacts and registries: Docker Hub, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or others.
- Expected branch protection, CI checks, release policy, dependency update policy, security posture, topics, CODEOWNERS, and support/contact policy.
- Local repo path, local consumer paths, generated files, scheduled tasks, services, shortcuts, shell profiles, Docker MCP overrides, and automation configs tied to the repo.

Infer missing inputs from live repo state and local files before asking.

## Workflow

### 1. Inspect Local And Live State

- Inspect git status, remotes, branches, upstream, tags, refs, ignored files, generated files, artifacts, temp paths, package outputs, and local consumer references.
- Inspect live GitHub repo metadata, visibility, owner, topics, description, default branch, open PRs, issues relevant to maintenance, branches, tags, releases, Actions runs, code scanning, Dependabot, security settings, branch protection, rulesets, collaborators/teams when visible, and community profile.
- Inspect package registries and published artifacts relevant to the repo.
- Check auth through `gh`, git credentials, env vars, package manager configs, Docker sessions, and connected tooling before asking for credentials.

### 2. Research Current Standards

- Check current official docs for GitHub community health, branch protection/rulesets, Actions, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and each relevant ecosystem or registry.
- Compare 2-3 strong current reference repos when it helps identify expected files, folders, metadata, workflows, security controls, release patterns, package metadata, or registry docs.
- Apply only relevant current practices. Skip outdated, heavy, paid, unsupported, or repo-inappropriate items and report meaningful skips.

### 3. Audit Repo Health

- Verify README accuracy, install/run/build/test/publish instructions, screenshots/examples, badges, links, release notes, changelog, support path, and registry links.
- Verify `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, issue templates, issue-template labels, pull request template, support/contact routing, `.gitignore`, `.dockerignore`, CI, release workflows, dependency update automation, and code scanning config when relevant.
- Verify public repo security posture: private vulnerability reporting or clear private reporting path, Dependabot security updates, secret scanning, push protection, code scanning, dependency graph, and current alert state when available at no extra cost.
- Distinguish broken security controls from Scorecard-style maturity or process alerts. Do not silently omit non-blocking open alerts; report each retained item and the not-performed work needed to clear it.
- Verify default-branch protection: required real checks, strict status checks, PR flow, review policy, stale review dismissal, conversation resolution, admin enforcement, no force pushes, and no deletions as appropriate for the repo.
- Verify topics are precise and current, not spammy or stale.
- Verify CODEOWNERS points only to existing appropriate owners and no stale upstream/internal teams.
- Verify versions, tags, releases, package metadata, Docker tags, package registry versions, image digests, and latest-release pointers match the repo's intended state.
- Verify Docker MCP overrides point at the intended image and, when applicable, verify active runtime tool annotations and at least one safe read-only tool call.
- Verify no stale PRs, stale setup branches, duplicate dependency PRs, unmerged release PRs, dangling local commits, unpublished artifacts, stale generated files, stale local path references, stale Docker MCP overrides, or old automation config references remain unclassified.

### 4. Repair Safe Gaps

- Apply low-risk fixes such as doc link updates, README command corrections, SECURITY reporting clarification, topic cleanup, stale CODEOWNERS correction, missing `.dockerignore`, obvious CI metadata correction, dependency config cleanup, branch deletion for already-merged unprotected branches, local ref pruning, and generated-file refresh when clearly required.
- Open or update a PR for repo changes when branch protection or repo policy requires it.
- Do not delete tags, releases, packages, protected branches, backup branches, or external artifacts unless the stale classification is proven and the action is safe or explicitly approved.
- If a fix changes publishable metadata or artifact content, run the ship-change workflow rather than silently publishing from the audit.

### 5. Validate

- Run local checks needed to prove safe fixes did not break the repo.
- Verify live GitHub and registry state after each external change.
- Re-check open PRs, branches, releases, tags, security settings, CI, code scanning, topics, community files, package endpoints, and local cleanliness after fixes.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Re-open this `SKILL.md` and validate the audit line by line against every mandatory section.
- Verify live state for every touched repo setting, security control, branch protection rule, PR, branch, tag, release, workflow, code scanning result, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact, temp path, cache, credential/config change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.
- Classify every artifact, external entity, and side effect as healthy/active, intentionally retained with reason, stale and removed, not applicable, or blocked with exact blocker.
- If any actionable stale item remains, report it as intentionally retained or blocked instead of calling the repo clean.

## Output Contract

Report only:

- health gaps fixed
- health gaps intentionally retained with exact reasons
- remaining blockers or credential steps
- live GitHub/security/CI/release/registry verification results
- branches, PRs, tags, releases, local paths, temp paths, or artifacts removed or retained
- paid requirement with product, reason, and price if encountered

## Example Invocations

`Use $ceratops-gh-repo-health-audit for this repo. Fix safe repo-health gaps and report only real blockers.`

`Use $ceratops-gh-repo-health-audit. Verify no stale PRs, branches, tags, releases, registry artifacts, stale docs, or security gaps remain.`
