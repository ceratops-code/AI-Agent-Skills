---
name: ceratops-gh-merge-pr
description: Merge a GitHub pull request safely with Ceratops defaults. Use when Codex needs to inspect a PR, verify branch protection, reviews, conversations, CI, code scanning, mergeability, auto-merge, merge queue, or required checks, merge or enable auto-merge, delete the branch, sync the local default branch, prune refs, and verify the final repo state.
---

# Ceratops GH Merge PR

## Overview

Merge one GitHub PR only after proving the repo will remain healthy. This is the small utility workflow for PR finalization; it does not publish packages unless the repo's merge automation does that and the result must be verified.

## Hard Requirements

- Treat every bullet in `Hard Requirements`, `Inputs To Capture`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract` as mandatory unless explicitly inapplicable.
- Before completion, re-open this `SKILL.md` and run a line-by-line closure pass over every mandatory bullet. Classify each item internally as satisfied, not applicable with reason, blocked with exact blocker, or intentionally retained side effect.
- Keep this checklist explicit and living. For every run, check current official GitHub docs or `gh` behavior when merge semantics, branch protection, merge queue, auto-merge, required checks, or cleanup behavior are uncertain or likely changed. If runtime research reveals a durable, broadly relevant missing rule, update this `SKILL.md`, validate the skill, and report the maintenance.
- Inspect local repo state and live PR state before choosing a merge path.
- Do not bypass branch protection, required checks, unresolved conversations, required reviews, security failures, or merge queue rules unless the user explicitly asks and the bypass is available without paid features or policy violation.
- Do not merge with failing required checks. For non-required failing checks, classify the risk and merge only when clearly irrelevant or explicitly approved by repo policy.
- Preserve user changes in the local worktree. Do not reset, checkout, or delete branches destructively.
- Prefer repo-configured merge method and auto-merge/merge-queue policy over personal preference.
- Stop only for missing auth after local checks, unresolved required review, unresolved conversation, failing required check, merge conflict, ambiguous target PR, destructive cleanup risk, or paid/permission blocker.

## Inputs To Capture

- PR URL, number, branch, or local branch that identifies the PR.
- Repo owner/name, default branch, merge method preference, and whether auto-merge or immediate merge is expected.
- Required checks, review policy, conversation-resolution policy, merge queue, admin enforcement, branch deletion policy, and whether the branch is from a fork.
- Local branch and worktree state that might be affected by syncing or cleanup.

Infer missing inputs from `gh`, git remotes, current branch, and live repo data before asking.

## Workflow

### 1. Inspect Local And Remote State

- Run local git inspection: status, current branch, remotes, upstream, default branch, and whether the local branch maps to a PR.
- Check GitHub auth through `gh`, git credentials, env vars, and connected GitHub tooling before asking for login.
- Fetch remote refs safely and inspect the PR's base, head, mergeability, draft state, labels, assignees, reviews, unresolved conversations, requested changes, checks, code scanning state, deployments, merge queue status, and branch protection.
- If the PR is not the intended one, stop with the exact ambiguity.

### 2. Research Current Rules When Needed

- Check current official GitHub docs or `gh` help when merge queue, auto-merge, branch protection, required status check, review, or branch deletion behavior is unclear.
- Prefer live GitHub API/CLI state over local assumptions.
- Do not rely on stale memory for newly changed GitHub merge or protection features.

### 3. Prepare The PR

- Confirm the PR is not draft unless the user asked to mark ready and it is ready.
- Confirm required checks are green or pending in a state suitable for auto-merge.
- Confirm required reviews are satisfied and no blocking review remains.
- Confirm conversations required by branch protection are resolved.
- Confirm the PR is up to date when strict status checks require it.
- If checks are failing from an in-scope simple issue and the user asked to complete the merge, fix the issue in the PR branch when safe; otherwise report the exact blocker.

### 4. Merge Or Enable Auto-Merge

- Use merge queue if required by the repo.
- Use auto-merge when checks are pending but all other merge requirements are satisfied and auto-merge is enabled for the repo.
- Use the repo's allowed/preferred merge method. If multiple are allowed and no preference exists, choose the method that preserves the repo's established history style.
- Verify the merge or queued auto-merge from the live PR endpoint, not just the command exit code.
- If auto-merge is enabled rather than completed, report the pending checks or queue state precisely.

### 5. Clean Up

- Delete the remote head branch only when the PR is merged, the branch is not protected, deletion is allowed, and the branch is not a reusable release or integration branch.
- Sync the local default branch to the remote default branch without destructive resets.
- Prune stale refs safely.
- Before force-deleting a local branch left behind by a squash or rebase merge, verify its patch is empty against the synced default branch; keep a safety branch and report it if the patch is not empty.
- Keep a clearly named safety branch only when needed to preserve reachable work after squash/rebase merge or history rewrite.
- Verify local status is clean or report exact retained local changes.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Re-open this `SKILL.md` and validate the work line by line against every mandatory section.
- Verify live PR state, merge commit or queue state, checks, reviews, conversations, branch protection result, branch deletion, and default branch state.
- Verify local repo state, branch, remotes, refs, worktree cleanliness, and retained safety branches.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked with exact blocker.
- If merge completion is not actually live, report the blocker or queued auto-merge state instead of claiming the PR is merged.

## Output Contract

Report only:

- PR URL and final state
- merge method, merge commit, queue state, or auto-merge state
- checks/security state that gated the merge
- branch deletion and local sync result
- intentionally retained branch or side effect with reason
- exact blocker or credential step if blocked

## Example Invocations

`Use $ceratops-gh-merge-pr for PR #12. Merge it when checks pass, delete the branch, and sync local main.`

`Use $ceratops-gh-merge-pr for the PR attached to this branch. Use auto-merge if checks are still pending.`
