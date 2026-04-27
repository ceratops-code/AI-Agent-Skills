---
name: ceratops-thread-resume-manual-stop
description: Resume an interrupted task in the current thread from current local state after a manual stop, restart, or crash. Use when Codex should inspect current local state, assume no external changes unless stated otherwise, continue from the next justified stage, and avoid rebuilding the whole task from scratch.
---

# Ceratops Thread Resume Manual Stop

Resume a same-thread task from current local state after a manual pause, cancellation, restart, or crash.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Blocking: Reuse fresh sufficient same-run evidence across adjacent, resumed, or chained workflows when it still proves the current decision; do not reacquire evidence or rerun checks solely to refresh already-sufficient evidence unless state is uncertain, plausibly changed, externally mutable for the decision, materially broadened, or required fresh by a higher-precedence instruction, skill, automation, or completion gate.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Skill-Specific Rules

- Treat recent thread context plus current local state as the primary sources of truth, even after a restart, unless local evidence forces a broader rebuild.
- Assume nothing external changed unless the user says it did or local evidence suggests otherwise.
- Do not restart the whole task from zero if the next justified stage can be identified cheaply.
- Re-check only entities that were touched, plausibly affected, or needed for the next stage or final verification.
- If the next viable option is complex, invasive, nonstandard, or high-maintenance, stop and ask before taking it.
- Do not ask for credentials unless the resumed task actually requires them.

## Inputs To Capture

- The current task goal and completion standard from the recent thread.
- Any user statement about what changed since the stop.
- The last clearly completed stage and the next likely stage.
- The local repos, files, artifacts, PRs, images, or automations that were in scope.

Infer missing inputs from the recent thread and local state before asking.

## Boundaries

- Use this skill only when the work stays in the current thread and Codex should resume from current local state after a manual stop, pause, restart, or crash.
- If the user wants to move a whole task into a new thread, stop and use `$ceratops-thread-full-handoff`.
- If the user wants to spin off a sub-issue into a new thread, stop and use `$ceratops-thread-side-task-handoff`.

## Workflow

### 1. Re-anchor the task

- Read only the recent thread tail needed to recover the goal, the latest confirmed state, and any unfinished stage.
- Restate the next justified stage internally before acting.

### 2. Refresh narrow local state

- Inspect only the touched or plausibly affected local state: git status, changed files, generated outputs, temp paths, local installs, or runtime state.
- Refresh remote or external state only if the task depends on it or it may have changed while stopped.

### 3. Continue from the next justified stage

- Resume at the next unfinished stage rather than replaying already-completed work.
- Reuse prior verified results unless your own actions, elapsed time, or external changes make them stale.
- Fix newly discovered low-risk in-scope issues immediately.

### 4. Finish with risk-based closure

- Before completion, run the narrowest justified closure pass for the task.
- Remove low-risk stale items that are no longer needed.
- Report only unresolved blockers, unresolved non-blocking debt, intentionally retained items, and anything important not verified.

## Completion Gate

- Verify the resumed task reached the next justified stable state or the requested completion state.
- Verify any re-checked local or remote entities are still consistent with the final answer.

## Output Contract

Report only:

- the resumed stage or completed outcome
- any detected divergence from the earlier assumed state
- unresolved blockers or non-blocking debt
- intentionally retained items with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-thread-resume-manual-stop to resume this interrupted task in the current thread from current local state after a stop, restart, or crash. Nothing changed externally.`
