---
name: ceratops-gh-repo-dependency-update
description: Process Dependabot, Renovate, security, and manual dependency update work through GitHub with Ceratops defaults. Use when Codex needs to discover dependency PRs or alerts, update packages recursively, inspect changelogs and advisories, refresh lockfiles, fix CI, merge safe updates, publish affected artifacts when the repo requires it, install or pull the result locally, and continue until no actionable dependency update remains or a real blocker is reached.
---

# Ceratops GH Repo Dependency Update

## Overview

Handle dependency updates as an end-to-end repo maintenance loop. Prefer safe automation for patch/minor/security updates, but stop on ambiguous major upgrades, production risk, unavailable credentials, or paid requirements.

## Hard Requirements

- Treat every bullet in `Hard Requirements`, `Inputs To Capture`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract` as mandatory unless explicitly inapplicable.
- Before completion, re-open this `SKILL.md` and run a line-by-line closure pass over every mandatory bullet. Classify each item internally as satisfied, not applicable with reason, blocked with exact blocker, or intentionally retained side effect.
- Keep this checklist explicit and living. For every run, check current official docs, advisory sources, and relevant package-manager or registry docs. If runtime research reveals a durable, broadly relevant missing dependency-update rule, update this `SKILL.md`, validate the skill, and report the maintenance.
- Inspect local repo state, live GitHub state, dependency PRs, alerts, package manifests, lockfiles, CI, branch protection, and registry requirements before changing anything.
- Process dependency updates recursively until no actionable update remains, a full pass makes no progress, or a real blocker is reached.
- Preserve user changes. Do not reset, delete, rebase, or overwrite work destructively.
- Prioritize security updates and production-impacting fixes, then low-risk patch/minor updates, then grouped maintenance updates. Treat major upgrades, runtime migrations, and behavior-changing updates as higher risk.
- Publish artifacts only when the repo's release policy requires dependency updates to produce a new package, image, binary, or registry output.
- Stop only for missing credentials after local checks, ambiguous major upgrade, failing checks that cannot be fixed safely, merge conflicts, destructive risk, paid requirements, unsupported registry flow, or security uncertainty.

## Inputs To Capture

- Target repo, branch, update PRs, package manager ecosystems, dependency bot, and whether security updates are priority-only.
- Release policy, artifact publishing policy, versioning rules, changelog expectations, and local verification commands.
- Registry targets such as Docker Hub, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or internal registries.
- Branch protection, required checks, code scanning, vulnerability alerts, dependency graph status, auto-merge policy, and delete-branch policy.

Infer missing inputs from local files and live GitHub state before asking.

## Workflow

### 1. Inspect Queue And Risk

- Inspect git status, remotes, branch, open PRs, dependency alerts, Dependabot/Renovate config, manifests, lockfiles, package manager metadata, CI, security config, tags, releases, and registry metadata.
- Check GitHub auth, package-registry auth, and connected tooling before asking for credentials.
- Build an update queue from live PRs, alerts, and local manifests. Deduplicate grouped updates and identify blocked, superseded, stale, or conflicting PRs.
- Classify each update as security, patch, minor, major, runtime/toolchain, transitive lockfile, grouped, or manual.

### 2. Research Current Update Evidence

- Use official package metadata, release notes, changelogs, advisories, compatibility notes, migration guides, and package-manager docs before merging meaningful updates.
- Prefer official advisory databases and GitHub security alerts for vulnerability context.
- Use reference repos only when ecosystem-specific update patterns are unclear and comparison will reduce risk.
- Do not infer that an update is safe from version number alone.

### 3. Process Updates Recursively

- Start with security and low-risk updates unless dependency ordering requires otherwise.
- For each update, inspect the diff, generated files, manifest changes, lockfile changes, transitive changes, CI impact, and release impact.
- Refresh lockfiles or generated dependency metadata using the project package manager, not manual editing, unless the ecosystem expects manual edits.
- Run targeted tests first when useful, then full required checks before merge.
- Fix in-scope failures. If failure is upstream, flaky, unrelated, or pre-existing, prove that classification with evidence.
- Merge or enable auto-merge only when required checks, reviews, conversations, and branch protection allow it.
- After each merge, sync the default branch, re-check open dependency PRs and alerts, and continue until no actionable update remains or a stop condition is met.

### 4. Publish And Verify When Required

- Determine whether merged dependency updates require a release or artifact publish under the repo's policy.
- If required, publish the relevant Docker image, Python package, npm package, Maven artifact, NuGet package, crate, gem, PowerShell module, GitHub Package, or other registry artifact using current official docs.
- Verify live registry endpoints, versions, tags, image digests, package pages, and release pages.
- Install, pull, or consume the published artifact locally enough to catch packaging or runtime failures.

### 5. Cleanup

- Close or classify stale, superseded, duplicate, or blocked dependency PRs only when the reason is proven.
- Delete merged branches when safe and allowed.
- Sync local default branch, prune stale refs, and verify the worktree is clean.
- Keep only intentionally retained safety branches, failing PRs, skipped major updates, or blocked updates with exact reasons.

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
- Verify live GitHub state for every dependency PR, alert, merge, check, branch, release, code scanning result, and branch protection gate touched.
- Verify live registry state and local install, pull, or consumption for every artifact published.
- Verify local state: default branch, worktree, remotes, refs, lockfiles, generated files, temp paths, caches, credentials/config, and retained branches.
- Classify every dependency update as merged, not applicable, intentionally retained with reason, stale and removed/closed, or blocked with exact blocker.
- If an actionable update remains, report it as retained or blocked instead of claiming the repo is fully updated.

## Output Contract

Report only:

- dependency updates merged and PR URLs
- dependency updates skipped, retained, or blocked with exact reason
- checks and security evidence
- release/tag and registry URLs when relevant
- artifact version, image digest, package details, and local verification result when relevant
- stale PRs or branches closed/deleted
- exact credential step or paid requirement if blocked

## Example Invocations

`Use $ceratops-gh-repo-dependency-update for this repo. Process Dependabot PRs recursively, merge safe updates, and stop only on real blockers.`

`Use $ceratops-gh-repo-dependency-update. Prioritize security updates, publish any required package release, and verify the installed artifact locally.`
