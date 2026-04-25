<!-- INTERNAL: include in Ceratops runtime release-branch staging and ship skills -->

## Release Branch Runtime

- Treat the runtime checkout's active `release/*` branch as the single local preview source of truth for the staged repo snapshot.
- Keep installed Ceratops skill junctions and the editable GH helper package pointed at the runtime checkout path, not at task worktrees.
- Reuse the same `release/*` branch name locally and remotely by default. Do not rename or remap it unless the user explicitly chooses that tradeoff.
- Refresh remote refs with `git fetch --prune origin` before judging whether a runtime `release/*` branch already exists remotely, should be reused, or was already cleaned up.
- Reuse fresh same-run evidence for local branch, worktree, and release-branch cleanup state; do not rerun removal or verification commands for items already known removed unless the state is uncertain, plausibly changed, or required fresh by another active instruction.
- Rerun the runtime installer after switching the runtime checkout branch so installed skill junctions and the editable GH helper package match the active repo snapshot.
- When the GH skill family was touched, confirm the editable GH helper package resolves from the runtime checkout after the installer or restore step.
