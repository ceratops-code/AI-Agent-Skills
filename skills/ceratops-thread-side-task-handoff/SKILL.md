---
name: ceratops-thread-side-task-handoff
description: Create a minimal copy-paste prompt for spinning a newly discovered side task into another thread. Use when Codex should ignore most of the original task and capture only the side task's origin, conclusion, current objective, minimal refs, and next step.
---

# Ceratops Thread Side-Task Handoff

Produce one minimal copy-paste prompt for starting a side task in a new thread.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Treat the original task as background. Include it in one short line only when needed.
- Optimize for the side task only. Ignore most of the original task unless it directly constrains the new thread.
- Produce a prompt, not a bundle and not instructions to use a follow-up handoff skill.
- Reuse fresh state already established in the current thread.
- Refresh only facts whose staleness would change the first step in the new thread.
- Prefer the discovered conclusion and current objective over chronology.
- Include what stays in the current thread only when it matters for scope control.
- Keep refs exact but minimal.
- Treat `source-of-truth refs` as the minimum exact entities the new thread is likely to open immediately because they directly govern, define, or evidence the side task itself.
- Do not list general process instructions, generic runtime constraints, or merely helpful background artifacts as `source-of-truth refs` unless the side task is specifically about them or the first next step depends on opening them.
- Put active instructions or process constraints under constraints, not under `source-of-truth refs`, unless those instruction files are themselves part of the side task.
- If the user says `include the following questions`, `including the questions`, or equivalent wording, carry those questions into the prompt as next-thread asks instead of answering them here.

## Inputs To Capture

- The original task in one line, if it matters.
- What was discovered or concluded that created the side task.
- The side task's current objective.
- What stays in the current thread, if that matters.
- The exact repos, files, PRs, tags, releases, images, paths, or automations the side task is likely to open immediately.
- Optional evidence or background artifacts only when the first next step is likely to inspect them immediately.
- Any active constraints or instructions that materially affect the side task.

Infer missing inputs from the current thread and local state before asking.

## Required Prompt Content

- What we were trying to do, in one short line if relevant
- What we came to eventually or discovered that created the side task
- What the objective is now
- What stays in the current thread, if relevant
- Exact source-of-truth refs, kept minimal
- Active constraints or instructions that materially affect the work
- The first next step or question for the new thread

## Boundaries

- Use this skill only when the user wants to spin off a newly discovered sub-issue into a different thread.
- If the whole task should move to a new thread, stop and use `$ceratops-thread-full-handoff`.
- If the task should continue in the same thread after a manual stop, restart, or crash, stop and use `$ceratops-thread-resume-manual-stop`.

## Workflow

### 1. Isolate the side task

- Separate the side task from the original task.
- Keep only the original-task context needed to explain why the side task exists.

### 2. Refresh only first-step-critical state

- Reuse fresh state from the current thread by default.
- Refresh only the local or remote state that would change the first step in the new thread or make the prompt misleading.

### 3. Emit a paste-ready prompt

- Produce a prompt that can be pasted directly into a new thread.
- Make the current objective and first next step explicit.
- Write the prompt as direct instruction to the new thread, not as commentary about a handoff artifact.

## Credential Handling

- Do not ask for credentials unless verifying the handoff requires protected state that cannot be inferred locally.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the prompt includes the required content and enough exact refs to start correctly.
- Verify the prompt excludes irrelevant branches of the original task unless they materially constrain the side task.
- Verify each listed `source-of-truth ref` is first-step-relevant and authoritative for the side task itself, not just a generic constraint or a maybe-useful artifact.
- Verify the prompt does not pretend a fresh re-check happened when it did not.

## Output Contract

Emit one copy-paste prompt for a new thread and nothing extra.

## Example Invocation

`Use $ceratops-thread-side-task-handoff to create a copy-paste prompt for spinning this side issue into a new thread and keep the main task out unless it directly matters.`
