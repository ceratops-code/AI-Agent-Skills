---
name: ceratops-gh-merge-pr
description: Merge a GitHub pull request safely with Ceratops defaults. Use when Codex needs to inspect a PR, verify branch protection, reviews, conversations, CI, code scanning, mergeability, auto-merge, merge queue, or required checks, merge or enable auto-merge, delete the branch, sync the local default branch, prune refs, and verify the final repo state.
---

# Ceratops GH Merge PR

## Overview

Merge one GitHub PR only after proving the repo will remain healthy. This is the narrow finalization workflow for PR completion; it does not take ownership of code changes, dependency campaigns, or first-time publication.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- On every run, check current official docs for unstable standards and use 2-3 strong current reference repos when useful.
- If runtime research reveals a durable missing general rule, update this `SKILL.md`, validate the skill, and report the maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local state and local auth before asking for credentials or making assumptions.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Inputs To Capture

- PR URL, number, branch, or local branch that identifies the PR.
- Repo owner and name, default branch, merge method preference, and whether auto-merge or immediate merge is expected.
- Required checks, review policy, conversation-resolution policy, merge queue, admin enforcement, branch deletion policy, and whether the branch is from a fork.
- Local branch and worktree state that might be affected by syncing or cleanup.

Infer missing inputs from `gh`, git remotes, the current branch, and live repo data before asking.

## Boundaries

- Use this skill when the PR content is already ready and the remaining work is to verify gates, merge, and clean up.
- If the PR needs code, docs, CI, or packaging changes first, stop and use `$ceratops-gh-repo-ship-change`.
- If the PR queue is part of a broader dependency-update campaign, stop and use `$ceratops-gh-repo-dependency-update`.
- If the repo itself is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-repo-publish`.

## Workflow

### 1. Inspect Local And Remote State

- Inspect local git status, current branch, remotes, upstream, default branch, and whether the local branch maps to a PR.
- Check GitHub auth through `gh`, git credentials, env vars, and connected GitHub tooling before asking for login.
- Inspect the live PR base, head, mergeability, draft state, labels, assignees, reviews, unresolved conversations, requested changes, checks, code scanning state, deployments, merge queue state, and branch protection.

### 2. Research Current Rules When Needed

- Check current official GitHub docs or `gh` help when merge queue, auto-merge, branch protection, required status checks, review behavior, or cleanup semantics are unclear or likely changed.
- Prefer live GitHub API or CLI state over memory.

### 3. Prepare The PR

- Confirm the PR is not draft unless the user explicitly wants to keep it draft.
- Confirm required checks are green or pending in a state suitable for auto-merge.
- Confirm required reviews are satisfied and no blocking review remains.
- Confirm required conversations are resolved.
- Confirm the PR is up to date when strict status checks require it.

### 4. Merge Or Enable Auto-Merge

- Use merge queue if required by the repo.
- Use auto-merge when checks are pending but all other merge requirements are satisfied.
- Use the repo's allowed and preferred merge method.
- Verify the merge or queued auto-merge from the live PR endpoint instead of trusting only the command exit code.

### 5. Clean Up

- Delete the remote head branch only when the PR is merged, deletion is allowed, and the branch is not a reusable release or integration branch.
- Sync the local default branch to the remote default branch without destructive resets.
- Prune stale refs safely.
- Keep a clearly named safety branch only when needed to preserve reachable work after a squash or rebase merge.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify live PR state, merge commit or queue state, checks, reviews, conversations, branch protection result, branch deletion, and default branch state.
- Verify local repo state, branch, remotes, refs, worktree cleanliness, and retained safety branches.

## Output Contract

Report only:

- PR URL and final state
- merge method, merge commit, queue state, or auto-merge state
- checks or security state that gated the merge
- branch deletion and local sync result
- intentionally retained branch or side effect with reason
- exact blocker or credential step if blocked

## Example Invocations

`Use $ceratops-gh-merge-pr for PR #12. Merge it when checks pass, delete the branch, and sync local main.`

`Use $ceratops-gh-merge-pr for the PR attached to this branch. Use auto-merge if checks are still pending.`
