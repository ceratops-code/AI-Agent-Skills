---
name: ceratops-thread-full-handoff
description: Create a copy-paste prompt for moving a whole task into a new thread. Use when Codex should compress the goal, current confirmed state, critical refs, and next step without re-auditing the whole task.
---

# Ceratops Thread Full Handoff

Produce one copy-paste prompt for continuing the whole task in a new thread.

<!-- CERATOPS_COMMON_CORE_START -->
<!-- SOURCE: templates/fragments/core-minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.

<!-- SOURCE: templates/fragments/core-thread-first-step.md -->

## First-Step State Refresh

- Apply this section only to thread-handoff skills.
- Reuse fresh state already established in the current thread by default.
- Refresh only facts whose staleness would change or misdirect the first step in the new thread.
- Keep refs exact but limited to the entities the next thread is likely to open first.
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Treat this as moving the whole task, not spinning off a side issue.
- Produce a prompt, not a bundle and not instructions to use a follow-up handoff skill.
- Do not broaden work just to make the prompt feel complete.
- Reuse fresh state already established in the current thread.
- Refresh only facts whose staleness would misdirect the first step in the new thread.
- Prefer current state, current objective, and next step over chronology.
- Exclude solved branches unless they materially constrain the next step.
- Include only the refs the new thread is likely to need immediately.
- If the user says `include the following questions`, `including the questions`, or equivalent wording, carry those questions into the prompt as next-thread asks instead of answering them here.

## Inputs To Capture

- The task goal and desired completion state.
- The current confirmed state the new thread should trust.
- The next justified step or first unresolved decision.
- The exact repos, files, PRs, tags, releases, images, paths, or automations the next thread is likely to open immediately.
- Any active constraints or instructions that materially affect the work.

Infer missing inputs from the current thread and local state before asking.

## Required Prompt Content

- What we were trying to do
- What has already been established or completed
- What the objective is now
- Unresolved blockers or non-blocking debt, if material
- Exact source-of-truth refs, kept minimal
- Active constraints or instructions that materially affect the work
- The next justified step
- Deferred questions or next-thread asks, if any

## Boundaries

- Use this skill only when the user wants to move the whole task into a different thread.
- If the task should continue in the same thread after a manual stop, restart, or crash, stop and use `$ceratops-thread-resume-manual-stop`.
- If only a newly discovered sub-issue should move to a new thread, stop and use `$ceratops-thread-side-task-handoff`.

## Workflow

### 1. Refresh only first-step-critical state

- Reuse fresh state from the current thread by default.
- Refresh only the local or remote state that would change the first step in the new thread or make the prompt misleading.

### 2. Compress to the current task state

- Prefer direct facts over chronology.
- Keep historical background to the minimum needed to avoid a wrong start.
- Keep refs exact but minimal.

### 3. Emit a paste-ready prompt

- Produce a prompt that can be pasted directly into a new thread.
- Make the objective now and the next justified step explicit.
- Write the prompt as direct instruction to the new thread, not as commentary about a handoff artifact.

## Credential Handling

- Do not ask for credentials unless verifying the handoff requires protected state that cannot be inferred locally.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the prompt includes the required content and enough exact refs to start correctly.
- Verify the prompt does not pretend a fresh re-check happened when it did not.

## Output Contract

Emit one copy-paste prompt for a new thread and nothing extra.

## Example Invocation

`Use $ceratops-thread-full-handoff to create a copy-paste prompt for moving this whole task into a new thread.`
