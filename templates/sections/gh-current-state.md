<!-- INTERNAL: include in skills that make GitHub-state decisions -->

## GH Current State

- Mandatory: Use copied repo-maintenance scripts, especially `scripts/github_pr_readiness.py` and the contract checkers, for bundled GitHub current-state checks when they cover the next decision.
- Mandatory: Use `gh`, GitHub API, copied repo-maintenance scripts, and contract evidence bundles as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.
