---
name: ceratops-gh-scripted-merge-pr
description: Merge a GitHub pull request with a scripted live readiness check first, while preserving the original Ceratops GH merge skill as a separate non-scripted variant.
---

# Ceratops GH Scripted Merge PR

Use the same merge-finalization scope as `$ceratops-gh-merge-pr`, but gate merge decisions on the bundled live PR checks first.

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

## Script Bundle

- Shared helper path relative to this skill: `..\ceratops-gh-scripted-runtime\scripts\gh_live_checks.py`
- PR readiness check: `python <resolved-helper-path> pr-readiness --pr NUMBER_OR_URL`
- Repo settings check when repo health is part of the merge closeout: `python <resolved-helper-path> repo-health --repo OWNER/REPO`

## Inputs To Capture

- PR URL, number, branch, or local branch that identifies the PR.
- Repo owner and name, default branch, merge method preference, and whether auto-merge or immediate merge is expected.
- Required checks, review policy, conversation-resolution policy, merge queue, admin enforcement, branch deletion policy, and whether the branch is from a fork.
- Local branch and worktree state that might be affected by syncing or cleanup.

Infer missing inputs from `gh`, git remotes, the current branch, and live repo data before asking.

## Boundaries

- Use this skill when the PR content is already ready and the remaining work is to verify gates, merge, and clean up.
- If the PR needs code, docs, CI, or packaging changes first, stop and use `$ceratops-gh-scripted-repo-ship-change`.
- If the PR queue is part of a broader dependency-update campaign, stop and use `$ceratops-gh-scripted-repo-dependency-update`.
- If the repo itself is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-scripted-repo-publish`.

## Workflow

### 1. Inspect local and remote state

- Inspect local git status, current branch, remotes, upstream, default branch, and whether the local branch maps to a PR.
- Check GitHub auth through `gh`, git credentials, env vars, and connected tooling before asking for login.

### 2. Run the live PR check first

- Run `python <resolved-helper-path> pr-readiness` before merge or auto-merge decisions.
- Treat the script output as the first source of truth for draft state, mergeability, blocking review decisions, visible status-check failures, and pending status checks.
- Re-run the script after any action that could change readiness, such as rebasing, updating the branch, dismissing a blocker, or waiting for CI.

### 3. Merge or enable auto-merge

- Use merge queue if required by the repo.
- Use auto-merge when checks are pending but all other merge requirements are satisfied.
- If the readiness check is green on checks and mergeability and the only remaining blocker is the acting maintainer's own required review, and the repo intentionally allows that maintainer to self-merge, use the admin merge path instead of fabricating approval or waiting for a second account.
- Use the repo's allowed and preferred merge method.

### 4. Clean up and verify

- Delete the remote head branch only when the PR is merged, deletion is allowed, and the branch is not a reusable release or integration branch.
- After the merge, verify the live PR endpoint shows the PR as merged instead of reusing the pre-merge readiness script on a now-closed PR.
- Sync the local default branch without destructive resets, prune stale refs safely, and run the repo-health script if repo-health claims are part of the closeout.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify the final merge decision was backed by a fresh pre-merge `python <resolved-helper-path> pr-readiness` run, then verify the post-merge PR state separately from the live PR endpoint.
- Verify live PR state, merge commit or queue state, checks, reviews, conversations, branch protection result, branch deletion, and default branch state.
- Verify local repo state, branch, remotes, refs, worktree cleanliness, and retained safety branches.

## Output Contract

Report only:

- final merge outcome
- unresolved blockers or non-blocking debt
- intentionally retained branch or side effect with reason
- anything important not verified
- exact credential step if blocked

## Example Invocation

`Use $ceratops-gh-scripted-merge-pr for PR #12. Run the bundled live PR check first, merge it when gates are satisfied, delete the branch, and sync local main.`
