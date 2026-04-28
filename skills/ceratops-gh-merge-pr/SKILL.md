---
name: ceratops-gh-merge-pr
description: Merge a GitHub pull request safely with Ceratops defaults, starting with a live scripted readiness check and ending with verified cleanup.
---

# Ceratops GH Merge PR

Merge one GitHub PR only after proving the repo will remain healthy. This is the narrow finalization workflow for PR completion; it does not take ownership of code changes, dependency campaigns, or first-time publication. Start with the bundled live PR check instead of relying on prose summaries or stale screenshots.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Blocking: Everything in this section is part of the skill contract unless explicitly inapplicable to the current task.
- Blocking: When this skill is invoked, follow this `SKILL.md` as the workflow contract for the task; if a higher-precedence instruction conflicts with a required skill step, report the conflict instead of silently skipping the step.
- Blocking: Do not claim completion unless this skill's completion gate is satisfied, intentionally inapplicable, or reported as a blocker.
- Blocking: Scope completion, current-state, root-cause, no-fix, unsupported, and durable-resolution claims to evidence actually checked, or to fresh same-task evidence that still applies.
- Blocking: Reuse fresh sufficient same-run evidence unless state is uncertain, plausibly changed, materially broadened, externally mutable for the decision, or this skill explicitly requires a fresh check.
- Blocking: Prefer direct local evidence and targeted diagnostics for the next skill decision; use current official sources only when local evidence leaves a concrete ambiguity or the task depends on unstable external behavior.
- Blocking: Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine skill runs unless the user explicitly asks or a required decision remains ambiguous after targeted evidence.
- Blocking: Ask before risky, destructive, irreversible, credential-dependent, externally mutating, complex, invasive, nonstandard, or high-maintenance steps unless the user already explicitly requested that tradeoff.
- Blocking: Do not update this `SKILL.md` or other skill/control files during a routine run unless the user explicitly asked for skill maintenance or the task cannot be completed safely without a narrow in-scope fix.
- Mandatory: When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Mandatory: Follow this skill's output contract when present; otherwise report only the outcome, unresolved blockers, retained state with reasons, and important unverified items.

<!-- SECTION SOURCE: templates/sections/gh-current-state.md -->

## GH Current State

- Use the shared helper package `ceratops_gh_current_state` for bundled GitHub current-state checks when it covers the next decision.
- Use `gh`, GitHub API, and `ceratops_gh_current_state` as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Blocking: Do not ask for credentials unless they are truly required after local checks.
- Blocking: If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target
- Blocking: If the user refuses a missing permission, credential, login, or scope, stop retrying and report the blocked action and exact entities still pending.
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Script Bundle

- PR readiness check: `python -m ceratops_gh_current_state pr-readiness --pr NUMBER_OR_URL`
- Repo settings check when repo health is part of the merge closeout: `python -m ceratops_gh_current_state repo-health --repo OWNER/REPO`
- Direct merge command: `gh pr merge --admin NUMBER_OR_URL_OR_BRANCH [--merge|--squash|--rebase] [--delete-branch]`

## Inputs To Capture

- PR URL, number, branch, or local branch that identifies the PR.
- Repo owner and name, default branch, merge method preference, and whether auto-merge or immediate merge is expected.
- Release policy, artifact-publish expectation, and whether merging this PR creates an immediate publish obligation.
- Required checks, review policy, conversation-resolution policy, merge queue, admin enforcement, branch deletion policy, and whether the branch is from a fork.
- Whether the PR changes workflow refs or GitHub Actions permissions.
- Local branch and worktree state that might be affected by syncing or cleanup.

Infer missing inputs from `gh`, git remotes, the current branch, and live repo data before asking.

## Boundaries

- Use this skill when the PR content is already ready and the remaining work is to verify gates, merge, and clean up.
- If the PR needs code, docs, CI, or packaging changes first, stop and use `$ceratops-gh-ship-change`.
- If merging the PR requires an immediate release, tag, package, image, or registry publish, stop and use `$ceratops-gh-ship-change` so the merge and artifact contract are handled together.
- If the PR queue is part of a broader dependency-update campaign, stop and use `$ceratops-gh-repo-dependency-update`.
- If the repo itself is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-repo-create-and-publish`.

## Workflow

### 1. Inspect local state and auth

- Inspect local git status, current branch, remotes, upstream, default branch, and whether the local branch maps to a PR.
- Check GitHub auth through `gh`, git credentials, env vars, and connected GitHub tooling before asking for login.

### 2. Run the live PR check first

- Run `python -m ceratops_gh_current_state pr-readiness` before merge or auto-merge decisions.
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
- Confirm the PR can be completed by merge and cleanup alone. If completion also requires release or artifact publishing, stop and use `$ceratops-gh-ship-change`.
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

## Completion Gate

- Verify the final merge decision was backed by a fresh pre-merge `python -m ceratops_gh_current_state pr-readiness` run, then verify the post-merge PR state separately from the live PR endpoint.
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
