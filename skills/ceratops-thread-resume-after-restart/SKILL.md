---
name: ceratops-thread-resume-after-restart
description: Reconstruct and resume an interrupted task in the current thread after Codex restarted, crashed, or was hard-stopped. Use when Codex should rebuild progress from disk, repo state, artifacts, PRs, and runtime signals before continuing from the next justified stage.
---

# Ceratops Thread Resume After Restart

Rebuild execution state after a restart or crash, then continue in the same thread.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- On every run, check current official docs for unstable standards and use 2-3 strong current reference repos when useful.
- If runtime research reveals a durable missing general rule, update this `SKILL.md`, validate the skill, and report the maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local state and local auth before asking for credentials or making assumptions.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- When a skill touches a public GitHub repo and reports repo, security, maturity, or process health, inspect the live community profile and equivalent no-cost moderation or community-health signals instead of inferring health from files, CI, or alert counts alone.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Treat prior thread claims as hypotheses until local or remote state confirms them.
- Reconstruct progress from disk and live state before taking the next action.
- Prefer the narrowest evidence that proves what was completed, what is partial, and what is stale.
- Do not assume in-memory plans, transient tool state, or unsaved edits survived the interruption.
- If the recovered next viable path is complex, invasive, nonstandard, or high-maintenance, stop and ask before taking it.

## Inputs To Capture

- The task goal and completion standard from the recent thread.
- Candidate repos, worktrees, temp paths, generated artifacts, automations, PRs, releases, images, or installs involved in the task.
- Any known last completed stage, last branch, or last published artifact.

Infer what you can from the thread and local state before asking.

## Boundaries

- Use this skill only when the work stays in the current thread and execution state may have been lost by restart, crash, or hard stop.
- If the task was only manually paused and the recent thread state is intact, stop and use `$ceratops-thread-resume-manual-stop`.
- If the user wants to move work into a new thread, stop and use `$ceratops-thread-create-handoff`.

## Workflow

### 1. Reconstruct evidence

- Read only the recent thread tail needed to recover the intended outcome and the last claimed progress.
- Inspect local repos, changed files, generated outputs, temp paths, published-artifact consumers, and active configs that could show what actually happened.
- Refresh remote state only for entities that matter to the next step or may have changed during the interruption.

### 2. Classify recovered state

- Mark each important entity as confirmed complete, partially complete, stale, missing, or not applicable.
- Remove low-risk stale leftovers immediately when safe.
- Treat unresolved ambiguity as a blocker only after narrow validation fails.

### 3. Continue from the next justified stage

- Resume from the earliest stage that is not yet confirmed, not from the beginning.
- Reuse earlier verified results when they remain valid.
- Fix newly discovered low-risk in-scope issues before moving on.

### 4. Finish with risk-based closure

- Before completion, run the narrowest justified closure pass for the reconstructed task state.
- Report only unresolved blockers, unresolved non-blocking debt, intentionally retained items, and anything important not verified.

## Credential Handling

- Do not ask for credentials unless reconstructing or continuing the task actually requires them.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the reconstructed state is coherent enough to justify the next action or final answer.
- Verify any corrected stale or partial state is reflected in the final answer.

## Output Contract

Report only:

- the reconstructed current state
- the resumed stage or completed outcome
- any stale or partial state that had to be corrected
- unresolved blockers or non-blocking debt
- intentionally retained items with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-thread-resume-after-restart to reconstruct progress from disk and continue this interrupted task in the current thread.`
