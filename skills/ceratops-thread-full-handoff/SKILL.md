---
name: ceratops-thread-full-handoff
description: Create a copy-paste prompt for moving a whole task into a new thread. Use when Codex should compress the goal, current confirmed state, critical refs, and next step without re-auditing the whole task.
---

# Ceratops Thread Full Handoff

Produce one copy-paste prompt for continuing the whole task in a new thread.

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

<!-- SECTION SOURCE: templates/sections/thread-first-step.md -->

## First-Step State Refresh

- Reuse fresh state already established in the current thread by default.
- Refresh only facts whose staleness would change or misdirect the first step in the new thread.
- Keep refs exact but limited to the entities the next thread is likely to open first.
<!-- CERATOPS_SHARED_SECTIONS_END -->

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
