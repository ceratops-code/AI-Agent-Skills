---
name: ceratops-gh-merge-pr
description: Merge a GitHub pull request safely with Ceratops defaults, starting with a live scripted readiness check and ending with verified cleanup.
---

# Ceratops GH Merge PR

Merge one GitHub PR only after proving the repo will remain healthy. This is the narrow finalization workflow for PR completion; it does not take ownership of code changes, dependency campaigns, or first-time publication. Start with the bundled live PR check instead of relying on prose summaries or stale screenshots.

<!-- CERATOPS_COMMON_CORE_START -->
<!-- SOURCE: templates/fragments/core-minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.

<!-- SOURCE: templates/fragments/core-gh-current-state.md -->

## GH Current State

- Apply this section only to skills that make GitHub-state decisions.
- Use `gh`, GitHub API, and `ceratops_gh_runtime` as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.

<!-- SOURCE: templates/fragments/core-gh-credentials.md -->

## GH Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Use `gh`, GitHub API, and `ceratops_gh_runtime` as the first-pass evidence for merge readiness and repo-policy gates.
- Run the readiness script before widening to extra live PR fields or official docs.
- Inspect labels, assignees, deployments, merge queue detail, code-scanning findings, or broader repo-health surfaces only when the readiness check, branch protection, or the user's request makes them relevant to the merge decision.

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

### 1. Inspect local state and auth

- Inspect local git status, current branch, remotes, upstream, default branch, and whether the local branch maps to a PR.
- Check GitHub auth through `gh`, git credentials, env vars, and connected GitHub tooling before asking for login.

### 2. Run the live PR check first

- Run `python -m ceratops_gh_runtime pr-readiness` before merge or auto-merge decisions.
- Treat the script output as the first source of truth for draft state, mergeability, blocking review decisions, visible status-check failures, and pending status checks.
- Re-run the script after any action that could change readiness, such as rebasing, updating the branch, dismissing a blocker, or waiting for CI.

### 3. Inspect only merge-decision exceptions

- Inspect live PR base, head, conversation-resolution state, branch protection result, merge queue state, and workflow-ref changes only when the readiness check, current repo policy, or the user's request makes them relevant.
- Ignore labels, assignees, deployments, broader repo-health surfaces, or detailed code-scanning follow-up unless they materially gate the merge or the user explicitly asked for them.

### 4. Research current rules when needed

- Check current official GitHub docs or `gh` help only when merge queue, auto-merge, branch protection, required status checks, review behavior, or cleanup semantics remain concretely ambiguous after the readiness check and targeted live state, or when those sources materially conflict.
- Prefer live GitHub API or CLI state over memory.

### 5. Prepare the PR

- Confirm the PR is not draft unless the user explicitly wants to keep it draft.
- Confirm required checks are green or pending in a state suitable for auto-merge.
- Confirm required reviews are satisfied and no blocking review remains.
- Confirm required conversations are resolved.
- Confirm the PR is up to date when strict status checks require it.
- If the PR changes workflow refs or GitHub Actions permissions, confirm it does not introduce mutable external action refs that violate the repo's SHA-pinning policy. If it does, stop and use `$ceratops-gh-ship-change`.

### 6. Merge or enable auto-merge

- Use `gh pr merge --admin` for every direct merge this skill performs. Add the PR selector, the repo's allowed merge-method flag, and `--delete-branch` when cleanup is intended and allowed.
- Use `gh pr merge --auto` only when the user explicitly wants GitHub to defer the final merge until remaining requirements finish; otherwise close the PR now with `gh pr merge --admin`.
- If the repo would otherwise route the PR through a merge queue, treat `gh pr merge --admin` as an intentional queue bypass and use it only after the fresh readiness check and live PR state show the bypass is justified.
- If the readiness check is green on checks and mergeability and the only remaining blocker is the acting maintainer's own required review, and the repo intentionally allows that maintainer to self-merge, use `gh pr merge --admin` instead of fabricating approval or waiting for a second account.
- Use the repo's allowed and preferred merge method.
- Verify the merge or queued auto-merge from the live PR endpoint instead of trusting only the command exit code.

### 7. Clean up and verify

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
