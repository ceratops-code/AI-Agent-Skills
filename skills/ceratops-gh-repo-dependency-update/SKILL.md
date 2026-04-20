---
name: ceratops-gh-repo-dependency-update
description: Process Dependabot, Renovate, security, and manual dependency update work through GitHub with Ceratops defaults. Use when Codex needs to discover dependency PRs or alerts, update packages recursively, inspect changelogs and advisories, refresh lockfiles, fix CI, merge safe updates, publish affected artifacts when the repo requires it, install or pull the result locally, and continue until no actionable dependency update remains or a real blocker is reached.
---

# Ceratops GH Repo Dependency Update

## Overview

Handle dependency updates as an end-to-end maintenance loop. Prefer safe automation for security, patch, and minor updates, and stop on ambiguous major upgrades, production risk, unavailable credentials, or paid requirements.

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
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Inputs To Capture

- Target repo, branch, dependency PRs, package-manager ecosystems, and whether security updates are priority-only.
- Release policy, artifact-publish policy, versioning rules, changelog expectations, and local verification commands.
- Registry targets, if any.
- Branch protection, required checks, code scanning, vulnerability alerts, auto-merge policy, and delete-branch policy.

Infer missing inputs from local files and live GitHub state before asking.

## Boundaries

- Use this skill when the work is primarily dependency updates, alert cleanup, or dependency bot PR processing.
- If the repo is not yet published or lacks a usable remote, stop and use `$ceratops-gh-repo-publish`.
- If the work is broader than dependency maintenance or includes substantial non-dependency code changes, stop and use `$ceratops-gh-repo-ship-change`.
- If only PR finalization remains for already-prepared dependency PRs, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect Queue And Risk

- Inspect git state, open PRs, dependency alerts, Dependabot or Renovate config, manifests, lockfiles, CI, security settings, tags, releases, and registry metadata.
- Check GitHub auth, registry auth, and connected tooling before asking for credentials.
- Build an update queue from live PRs, alerts, and local manifests, and classify each update as security, patch, minor, major, toolchain, grouped, or manual.

### 2. Research Update Evidence

- Use official package metadata, release notes, changelogs, advisories, compatibility notes, migration guides, and package-manager docs before merging meaningful updates.
- Use strong current reference repos only when ecosystem-specific update patterns are unclear and comparison will reduce risk.
- Do not infer that an update is safe from version number alone.

### 3. Process Updates Recursively

- Prioritize security and low-risk updates unless ordering constraints require otherwise.
- For each update, inspect the diff, manifest changes, lockfile changes, transitive changes, CI impact, and release impact.
- Refresh lockfiles or generated dependency metadata using the project package manager unless the ecosystem explicitly expects manual edits.
- Run targeted tests first when useful, then full required checks before merge.
- Fix in-scope failures. If a failure is flaky, unrelated, or upstream, prove that classification with evidence.
- Merge or enable auto-merge only when required checks, reviews, conversations, and branch protection allow it.
- After each merge, sync the default branch, re-check the queue, and continue until no actionable update remains, no progress is being made, or a real blocker is reached.

### 4. Publish And Verify When Required

- Determine whether merged dependency updates require a release or artifact publish under the repo's policy.
- If required, publish the relevant package, image, or artifact using the current official flow for that ecosystem.
- Verify the live registry or release endpoint and install, pull, or consume the published artifact locally enough to catch packaging or runtime failures.

### 5. Cleanup

- Close or classify stale, superseded, duplicate, or blocked dependency PRs only when the reason is proven.
- Delete merged branches when safe and allowed.
- Sync the local default branch, prune stale refs, and verify the worktree is clean.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify live GitHub state for every dependency PR, alert, merge, check, branch, release, code scanning result, and branch protection gate touched.
- Verify live registry state and local install, pull, or consumption for every artifact published.
- Verify local state: default branch, worktree, remotes, refs, lockfiles, generated files, temp paths, caches, credentials, and retained branches.

## Output Contract

Report only:

- dependency updates applied
- dependency updates skipped, retained, or blocked with exact reasons
- released or published artifact details when materially relevant to downstream use
- unresolved blockers or non-blocking debt
- anything important not verified
- exact credential step or paid requirement if blocked

## Example Invocations

`Use $ceratops-gh-repo-dependency-update for this repo. Process Dependabot PRs recursively, merge safe updates, and stop only on real blockers.`

`Use $ceratops-gh-repo-dependency-update. Prioritize security updates, publish any required package release, and verify the installed artifact locally.`
