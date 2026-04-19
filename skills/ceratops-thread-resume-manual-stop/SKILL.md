---
name: ceratops-thread-resume-manual-stop
description: Resume an interrupted task in the current thread after execution was manually stopped or paused. Use when Codex should inspect current local state, assume no external changes unless stated otherwise, continue from the next justified stage, and avoid rebuilding the whole task from scratch.
---

# Ceratops Thread Resume Manual Stop

Resume a same-thread task after a manual pause, cancellation, or deliberate stop.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- On every run, check current official docs for unstable standards and use 2-3 strong current reference repos when useful.
- If runtime research reveals a durable missing general rule, update this `SKILL.md`, validate the skill, and report the maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local state and local auth before asking for credentials or making assumptions.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Treat recent thread context plus current local state as the primary sources of truth.
- Assume nothing external changed unless the user says it did or local evidence suggests otherwise.
- Do not restart the whole task from zero if the next justified stage can be identified cheaply.
- Re-check only entities that were touched, plausibly affected, or needed for the next stage or final verification.
- If the next viable option is complex, invasive, nonstandard, or high-maintenance, stop and ask before taking it.

## Inputs To Capture

- The current task goal and completion standard from the recent thread.
- Any user statement about what changed since the stop.
- The last clearly completed stage and the next likely stage.
- The local repos, files, artifacts, PRs, images, or automations that were in scope.

Infer missing inputs from the recent thread and local state before asking.

## Boundaries

- Use this skill only when the work stays in the current thread and execution was manually stopped or paused.
- If Codex restarted, crashed, or lost execution state, stop and use `$ceratops-thread-resume-after-restart`.
- If the user wants to move work into a new thread, stop and use `$ceratops-thread-create-handoff`.

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

## Credential Handling

- Do not ask for credentials unless the resumed task actually requires them.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

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

`Use $ceratops-thread-resume-manual-stop to resume this paused task in the current thread from current local state. Nothing changed externally.`
