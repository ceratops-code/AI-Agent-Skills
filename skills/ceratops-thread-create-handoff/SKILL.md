---
name: ceratops-thread-create-handoff
description: Create a compact verified handoff bundle for opening a new thread on an existing task. Use when Codex should compress the goal, verified current state, unresolved issues, exact source-of-truth entities, and next justified step into paste-ready text without dragging along the whole thread.
---

# Ceratops Thread Create Handoff

Produce a compact handoff for a new thread without copying the whole conversation.

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

- Verify current state before writing the handoff.
- Keep the handoff short and operational, not narrative.
- Include only information the next thread actually needs.
- Exclude already-fixed details unless they matter to the remaining state or the next decision.

## Required Handoff Fields

- Current goal
- Verified current state
- Unresolved blockers or unresolved non-blocking debt
- Intentionally retained items with reasons
- Exact source-of-truth repos, files, PRs, tags, releases, images, paths, or automations
- Next justified step
- Active instructions or constraints that materially affect the work

## Boundaries

- Use this skill only when the user wants to move an existing task into a different thread.
- If the task should continue in the same thread after a manual stop, stop and use `$ceratops-thread-resume-manual-stop`.
- If the task should continue in the same thread after a restart or crash, stop and use `$ceratops-thread-resume-after-restart`.

## Workflow

### 1. Verify before summarizing

- Refresh only the local or remote state that materially affects the handoff.
- Resolve easy stale-state confusion before writing the bundle.

### 2. Compress aggressively

- Prefer direct facts over chronology.
- Use exact identifiers, paths, PR numbers, tags, and artifact names instead of vague references.
- Omit solved branches of investigation unless they materially constrain the next step.

### 3. Emit paste-ready text

- Produce a bundle that can be pasted directly into a new thread.
- Make the next justified step explicit so the next thread can start working immediately.

## Credential Handling

- Do not ask for credentials unless verifying the handoff requires protected state that cannot be inferred locally.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the handoff includes the required fields and exact source-of-truth references.
- Verify the handoff does not claim unverified state as confirmed.

## Output Contract

Emit one compact handoff bundle with the required fields above and nothing extra.

## Example Invocation

`Use $ceratops-thread-create-handoff to prepare a compact verified handoff for moving this task into a new thread.`
