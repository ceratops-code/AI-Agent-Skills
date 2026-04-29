---
name: ceratops-thread-resume-manual-stop
description: Resume an interrupted task in the current thread from current local state after a manual stop, restart, or crash. Use when Codex should inspect current local state, assume no external changes unless stated otherwise, continue from the next justified stage, and avoid rebuilding the whole task from scratch.
---

# Ceratops Thread Resume Manual Stop

Resume a same-thread task from current local state after a manual pause, cancellation, restart, or crash.

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
- Blocking: For skill runtime workflows, invoke shared helpers through installed console commands or `python -m <module>` entrypoints; do not locate shared helpers by absolute paths, by the repo's parent directory, or by per-skill `scripts` junctions.
- Blocking: When a Ceratops skill-maintenance workflow explicitly needs a repo-maintenance script, treat `scripts/<name>` paths as relative to the active `AI-Agent-Skills` checkout root; resolve that root from the current worktree with `git rev-parse --show-toplevel` or from the installed skill junction under `$CODEX_HOME/skills/<skill-name>`, and stop as blocked if neither resolves to a checkout containing `skills/`, `templates/`, and `scripts/`.
- Mandatory: When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Mandatory: Follow this skill's output contract when present; otherwise report only the outcome, unresolved blockers, retained state with reasons, and important unverified items.

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
