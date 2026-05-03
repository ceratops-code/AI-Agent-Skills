<!-- INTERNAL: include in Ceratops runtime release-branch staging and ship skills -->

## Release Branch Runtime

- Treat the runtime checkout's active `release/*` branch as the single local preview source of truth for the staged repo snapshot.
- Blocking: Keep installed Ceratops skill folders generated from the runtime checkout path, not from task worktrees.
- Reuse the same `release/*` branch name locally and remotely by default. Do not rename or remap it unless the user explicitly chooses that tradeoff.
- Refresh remote refs with `git fetch --prune origin` before judging whether a runtime `release/*` branch already exists remotely, should be reused, or was already cleaned up.
- Mandatory: Rerun the runtime installer after switching the runtime checkout branch so installed skill copies match the active repo snapshot.
- Mandatory: When the GH skill family was touched, confirm copied scripts and contract payloads exist in the relevant installed skill folders after the installer or restore step.
