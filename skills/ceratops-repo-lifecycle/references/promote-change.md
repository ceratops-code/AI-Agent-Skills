# Promote Change Action

## Goal

Fast-forward selected committed task branches into `release/local`. For
`promote-and-deploy`, run explicitly selected repository deploy operations in
order, execute their returned handoffs in that order when managed skills exist,
and report missing handoffs without blocking completed repository deployment.
For composed shipping,
suppress promotion deployment and return only the sibling ship helper's
terminal release-publication, local-deployment, finalization, and cleanup
result.

## Context

### Script Bundle

- (D) Invocation contract: bind `<skill-root>` to the directory containing this
  action's parent `SKILL.md`; require
  `<skill-root>/scripts/promote-repository.py` once before the first call.
  Invoke that exact path with the working directory equal to its `--repo-root`
  value; stop if it is absent and never resolve it relative to that repository.
- (D) Promotion helper:
  `python
  "<skill-root>/scripts/promote-repository.py" --repo-root PATH
  --source-branch BRANCH [--source-branch BRANCH...] --main-branch main
  --release-branch release/local --remote-name origin --no-run-operation`.
- (D) Promotion plus deployment:
  `python
  "<skill-root>/scripts/promote-repository.py" --repo-root PATH
  --source-branch BRANCH [--source-branch BRANCH...] --main-branch main
  --release-branch release/local --remote-name origin
  --run-operation ID [--run-operation ID...]`.
- (D) Promotion followed by terminal shipping uses the same command with
  `--ship-after-promotion` as its complete operation choice. Do not add
  `--run-operation` or `--no-run-operation`; shipping alone publishes or
  explicitly no-ops the release, then deploys or explicitly no-ops locally
  after merge.
- (D) Fast-change callers may prepare a clean release checkout without
  promotion or deployment:
  `python
  "<skill-root>/scripts/promote-repository.py" --repo-root PATH
  --main-branch main --release-branch release/local --remote-name origin
  --prepare-release-only`.

### Inputs To Capture

- Repository checkout, selected committed source branches, main branch,
  `release/local`, and remote.
- Whether the selected action is `promote`, `promote-and-deploy`, or composed
  promotion and shipping.
- Optional PR `--title` and `--body` require `--ship-after-promotion` and pass
  unchanged to shipping.
- Ordered deploy operation IDs for `promote-and-deploy`, or ordered release
  preflight, release publication, and deploy operation IDs for composed
  shipping. An explicit list replaces that phase's default.

## Constraints

### Boundaries

- Promote only explicitly selected task branches.
- Keep unrelated branches and worktrees outside inspection and cleanup scope.
- Before promotion, automatically rebase a selected clean, unpublished,
  linear-history task branch onto current `release/local`. If rebasing fails,
  abort it, verify the original head and clean worktree were restored, and
  block with the conflicting paths. Stop for other source mutation, review, or
  commit work.

### Workflow

1. Require clean selected worktrees. Through the promotion helper, establish
   Git ancestry with the eligible automatic rebase and run `git diff --check`.
2. For `promote`, run the helper with `--no-run-operation`.
3. For `promote-and-deploy`, repeat `--run-operation ID` in the requested
   order. The helper prevalidates the complete selection before executing the
   first operation. An absent `deploy` section is an explicit no-op; a selected
   ID missing from an existing operations map blocks before execution.
4. For composed promotion and shipping, run it with
   `--ship-after-promotion` and, when explicitly selected, repeat
   `--release-preflight-operation ID`, `--release-operation ID`, and
   `--deploy-operation ID`; use one optional `--sdlc-contract PATH`. The helper
   suppresses promotion deployment, records the exact head and canonical scope,
   then invokes the sibling ship helper after successful promotion with the
   same ordered selections, `release/local`, main, the remote, and exact commit.
   Return only its terminal shipping result or one closed blocker; reject
   unknown or incomplete responses.
5. Use the helper's `managed_skills` and ordered `handoffs` result after all
   selected repository operations succeed or no-op. Execute each returned
   handoff against `release/local`; when managed skills exist without one,
   report them as not deployed and continue.
6. Atomically normalize an exact version-1 pending-work scope to version 2
   before reuse. Retire a missing legacy source, keep a clean source contained
   in the legacy target as `retained`, and mark a dirty, unavailable, or
   advanced source `preserved` so stale cleanup cannot block the new promotion
   or delete evolved work. Treat the normalized version-2 scope as the only
   source scope later passed to ship. Persist each selected source's exact tip
   and helper-owned state. Advance a reusable scope only when its recorded
   target is an ancestor of the new target. Recover a missing source
   automatically only when its `deleting` state and recorded commit ancestry
   prove an interrupted helper deletion; a missing `retained` source blocks.
7. On a shipping blocker, retain the scope, branches, worktrees, and checkpoints
   for resume. Terminal shipping owns finalization and selected-work cleanup;
   it leaves a worktree and branch untouched when the worktree's parent chain
   has no `worktrees` directory component and reports the exact preserved path.

The helper refreshes the remote, fast-forwards main, reuses an existing local
`release/local` without merging main into it, and creates it from main when
missing. When release `HEAD` is not an ancestor, it rebases only an unpublished,
linear selected branch in its existing clean worktree. It refuses published or
nonlinear history. A failed attempt must restore the original branch head and
clean worktree before it reports the failure and conflicting paths. The helper
then runs `git diff --check`, fast-forwards each branch, records the exact
generic scope, and optionally executes the ordered structured deployment
selection. In composed mode it skips those operations and invokes
`ship-repository.py` once,
pinned to the promoted head and canonical scope. The sibling helper preserves
its CI and review waits and owns merge, post-merge release publication, local
deployment, finalization, and
cleanup. An incomplete or blocked ship result stops without promotion cleanup.
Lifecycle deployment treats an absent `deploy` section as a no-op; a selected
ID missing from an existing operations map is strict.
Preparation-only requires a clean `main` checkout and exits immediately after
`release/local` is ready, before source preflight, promotion, scope records,
or deployment.

## Done When

### Completion Gate

- The checkout is clean on `release/local`.
- Every selected branch is contained in the reported release commit.
- Every attempted automatic rebase either completed and reported both heads or
  restored the original clean source state before blocking.
- Repository deployment ran during promotion only when `promote-and-deploy`
  was selected; every selected operation ran in order, any returned handoffs
  completed in order, and managed skills without one were reported as not
  deployed. In composed mode, shipping ran every selected publication and
  deployment operation at its lifecycle-owned phase after merge.
- The exact pending-work scope is retained for standalone promotion or a
  shipping blocker; successful composed shipping finalizes it, cleans selected
  sources, and reports any preserved legacy sources or non-cleanup-eligible
  worktrees left untouched.

### Output Contract

Report only:

- `release/local`, exact head, promoted branches, and automatic rebase results
- ordered operation outcomes and returned or missing handoffs when selected
- pending-work scope
- blockers or intentionally retained state
