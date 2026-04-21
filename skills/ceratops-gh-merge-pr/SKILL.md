---
name: ceratops-gh-merge-pr
description: Merge a GitHub pull request safely with Ceratops defaults, starting with a live scripted readiness check and ending with verified cleanup.
---

# Ceratops GH Merge PR

Merge one GitHub PR only after proving the repo will remain healthy. This is the narrow finalization workflow for PR completion; it does not take ownership of code changes, dependency campaigns, or first-time publication. Start with the bundled live PR check instead of relying on prose summaries or stale screenshots.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- Use local state, `gh`, GitHub API, and `ceratops_gh_runtime` first.
- Check current official docs or `gh` help only when those sources leave a concrete task-blocking ambiguity or materially conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or GH-skill maintenance work during routine runs.
- Routine runs do not update this `SKILL.md` unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- When a skill touches a public GitHub repo and reports repo, security, maturity, or process health, inspect the live community profile and equivalent no-cost moderation or community-health signals instead of inferring health from files, CI, or alert counts alone.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper package: `ceratops_gh_runtime`
- PR readiness check: `python -m ceratops_gh_runtime pr-readiness --pr NUMBER_OR_URL`
- Repo settings check when repo health is part of the merge closeout: `python -m ceratops_gh_runtime repo-health --repo OWNER/REPO`
- Direct merge command: `gh pr merge --admin NUMBER_OR_URL_OR_BRANCH [--merge|--squash|--rebase] [--delete-branch]`

## Inputs To Capture

- PR URL, number, branch, or local branch that identifies the PR.
- Repo owner and name, default branch, merge method preference, and whether auto-merge or immediate merge is expected.
- Required checks, review policy, conversation-resolution policy, merge queue, admin enforcement, branch deletion policy, and whether the branch is from a fork.
- Whether the PR changes workflow refs or GitHub Actions permissions.
- Local branch and worktree state that might be affected by syncing or cleanup.

Infer missing inputs from `gh`, git remotes, the current branch, and live repo data before asking.

## Boundaries

- Use this skill when the PR content is already ready and the remaining work is to verify gates, merge, and clean up.
- If the PR needs code, docs, CI, or packaging changes first, stop and use `$ceratops-gh-ship-change`.
- If the PR queue is part of a broader dependency-update campaign, stop and use `$ceratops-gh-repo-dependency-update`.
- If the repo itself is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-repo-create-and-publish`.

## Workflow

### 1. Inspect local and remote state

- Inspect local git status, current branch, remotes, upstream, default branch, and whether the local branch maps to a PR.
- Check GitHub auth through `gh`, git credentials, env vars, and connected GitHub tooling before asking for login.
- Inspect the live PR base, head, mergeability, draft state, labels, assignees, reviews, unresolved conversations, requested changes, checks, code scanning state, deployments, merge queue state, and branch protection.

### 2. Research current rules when needed

- Check current official GitHub docs or `gh` help when merge queue, auto-merge, branch protection, required status checks, review behavior, or cleanup semantics are unclear or likely changed.
- Prefer live GitHub API or CLI state over memory.

### 3. Run the live PR check first

- Run `python -m ceratops_gh_runtime pr-readiness` before merge or auto-merge decisions.
- Treat the script output as the first source of truth for draft state, mergeability, blocking review decisions, visible status-check failures, and pending status checks.
- Re-run the script after any action that could change readiness, such as rebasing, updating the branch, dismissing a blocker, or waiting for CI.

### 4. Prepare the PR

- Confirm the PR is not draft unless the user explicitly wants to keep it draft.
- Confirm required checks are green or pending in a state suitable for auto-merge.
- Confirm required reviews are satisfied and no blocking review remains.
- Confirm required conversations are resolved.
- Confirm the PR is up to date when strict status checks require it.
- If the PR changes workflow refs or GitHub Actions permissions, confirm it does not introduce mutable external action refs that violate the repo's SHA-pinning policy. If it does, stop and use `$ceratops-gh-ship-change`.

### 5. Merge or enable auto-merge

- Use `gh pr merge --admin` for every direct merge this skill performs. Add the PR selector, the repo's allowed merge-method flag, and `--delete-branch` when cleanup is intended and allowed.
- Use `gh pr merge --auto` only when the user explicitly wants GitHub to defer the final merge until remaining requirements finish; otherwise close the PR now with `gh pr merge --admin`.
- If the repo would otherwise route the PR through a merge queue, treat `gh pr merge --admin` as an intentional queue bypass and use it only after the fresh readiness check and live PR state show the bypass is justified.
- If the readiness check is green on checks and mergeability and the only remaining blocker is the acting maintainer's own required review, and the repo intentionally allows that maintainer to self-merge, use `gh pr merge --admin` instead of fabricating approval or waiting for a second account.
- Use the repo's allowed and preferred merge method.
- Verify the merge or queued auto-merge from the live PR endpoint instead of trusting only the command exit code.

### 6. Clean up and verify

- Delete the remote head branch only when the PR is merged, deletion is allowed, and the branch is not a reusable release or integration branch.
- After the merge, verify the live PR endpoint shows the PR as merged instead of reusing the pre-merge readiness script on a now-closed PR.
- Sync the local default branch to the remote default branch without destructive resets.
- Prune stale refs safely.
- Keep a clearly named safety branch only when needed to preserve reachable work after a squash or rebase merge.
- Run the repo-health script if repo-health claims are part of the closeout.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify the final merge decision was backed by a fresh pre-merge `python -m ceratops_gh_runtime pr-readiness` run, then verify the post-merge PR state separately from the live PR endpoint.
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

`Use $ceratops-gh-merge-pr for PR #12. Run the bundled live PR check first, merge it when gates are satisfied, delete the branch, and sync local main.`
