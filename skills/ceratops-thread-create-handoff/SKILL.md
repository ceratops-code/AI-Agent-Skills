---
name: ceratops-thread-create-handoff
description: Create a compact handoff bundle for opening a new thread on an existing task or sub-issue. Use when Codex should compress the handed-off issue, current working state, unresolved issues, deferred questions, exact source-of-truth entities, and next justified step into paste-ready text without dragging along the whole thread.
---

# Ceratops Thread Create Handoff

Produce a compact handoff for a new thread without copying the whole conversation or re-auditing the whole task.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- On every run, check current official docs for unstable standards and current best practices, and use 2-3 strong current reference repos when useful.
- If runtime research reveals a durable missing general rule or durable best-practice improvement, update this `SKILL.md`, validate the skill, and report the maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- When a skill touches a public GitHub repo and reports repo, security, maturity, or process health, inspect the live community profile and equivalent no-cost moderation or community-health signals instead of inferring health from files, CI, or alert counts alone.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Do not broaden work just to verify the handoff.
- Reuse fresh state already established in the current thread when the source-of-truth entity is already identified.
- Refresh only items whose staleness would change the next step or make the handoff misleading.
- Keep the handoff short and operational, not narrative.
- Include only information the next thread actually needs.
- Exclude already-fixed details unless they matter to the remaining state or the next decision.
- Determine exactly what is being handed off: the whole task or a specific sub-issue that split off from the current thread.
- When the current thread continues on a different issue, say explicitly what stays here and what moves to the new thread.
- If the user asks new questions for the handed-off issue, do not answer them in the current thread unless explicitly requested. Put them into the handoff as deferred next-thread questions or tasks.
- If the user says `include the following questions`, `including the questions`, or equivalent wording after invoking this skill, interpret those questions as deferred next-thread work by default rather than answering them in the current thread.

## Required Handoff Fields

- Handoff scope: the exact issue or sub-issue being moved
- Remaining scope in the current thread, if any
- Current goal
- Current working state
- Unresolved blockers or unresolved non-blocking debt
- Deferred questions or next-thread asks, if any
- Intentionally retained items with reasons, if non-obvious or material
- Exact source-of-truth repos, files, PRs, tags, releases, images, paths, or automations
- Next justified step
- Active instructions or constraints that materially affect the work

## Boundaries

- Use this skill only when the user wants to move an existing task into a different thread.
- If the task should continue in the same thread after a manual stop, stop and use `$ceratops-thread-resume-manual-stop`.
- If the task should continue in the same thread after a restart or crash, stop and use `$ceratops-thread-resume-after-restart`.

## Workflow

### 1. Refresh only what matters before summarizing

- Reuse fresh state from the current thread by default.
- Refresh only the local or remote state that materially affects the next step or would change the handoff.
- Resolve easy stale-state confusion before writing the bundle when that confusion affects the handoff.
- Identify whether the handoff covers the whole task or only a newly arising sub-issue.

### 2. Compress aggressively

- Prefer direct facts over chronology.
- Use exact identifiers, paths, PR numbers, tags, and artifact names instead of vague references.
- Omit solved branches of investigation unless they materially constrain the next step.
- Separate the handed-off issue from any issue that remains in the current thread.

### 3. Emit paste-ready text

- Produce a bundle that can be pasted directly into a new thread.
- Make the next justified step explicit so the next thread can start working immediately.
- Include any deferred questions as open questions or next tasks for the new thread to handle.

## Credential Handling

- Do not ask for credentials unless verifying the handoff requires protected state that cannot be inferred locally.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the handoff includes the required fields and exact source-of-truth references.
- Verify the handoff does not pretend a fresh re-check happened when it did not.

## Output Contract

Emit one compact handoff bundle with the required fields above and nothing extra.

## Example Invocation

`Use $ceratops-thread-create-handoff to prepare a compact handoff for moving this task into a new thread.`

`Use $ceratops-thread-create-handoff. Keep the MCP issue in this thread, but hand off the credit-usage issue to a new thread and include my following credit-usage questions in that handoff instead of answering them here.`

`Use $ceratops-thread-create-handoff for handoff of the new credit-usage issue, including the questions:
1. ...
2. ...
3. ...`
