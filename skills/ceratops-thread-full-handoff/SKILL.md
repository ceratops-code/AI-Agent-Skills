---
name: ceratops-thread-full-handoff
description: Create a copy-paste prompt for moving a whole task into a new thread. Use when Codex should compress the goal, current confirmed state, critical refs, and next step without re-auditing the whole task.
---

# Ceratops Thread Full Handoff

Produce one copy-paste prompt for continuing the whole task in a new thread.

## Skill-Specific Rules

- Treat this as moving the whole task, not spinning off a side issue.
- Produce a prompt, not a bundle and not instructions to use a follow-up handoff skill.
- Do not broaden work just to make the prompt feel complete.
- Prefer current state, current objective, and next step over chronology.
- Exclude solved branches unless they materially constrain the next step.
- Include only the refs the new thread is likely to need immediately.
- If the user says `include the following questions`, `including the questions`, or equivalent wording, carry those questions into the prompt as next-thread asks instead of answering them here.
- Do not ask for credentials unless verifying the handoff requires protected state that cannot be inferred locally.

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

### 2. Compress to the current task state

- Prefer direct facts over chronology.
- Keep historical background to the minimum needed to avoid a wrong start.
- Keep refs exact but minimal.

### 3. Emit a paste-ready prompt

- Make the objective now and the next justified step explicit.
- Write the prompt as direct instruction to the new thread, not as commentary about a handoff artifact.

## Completion Gate

- Verify the prompt includes the required content and enough exact refs to start correctly.
- Verify the prompt does not pretend a fresh re-check happened when it did not.

## Output Contract

Emit one copy-paste prompt for a new thread and nothing extra.

## Example Invocation

`Use $ceratops-thread-full-handoff to create a copy-paste prompt for moving this whole task into a new thread.`
