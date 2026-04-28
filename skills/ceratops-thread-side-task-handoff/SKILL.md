---
name: ceratops-thread-side-task-handoff
description: Create a minimal copy-paste prompt for spinning a newly discovered side task into another thread. Use when Codex should ignore most of the original task and capture only the side task's origin, conclusion, current objective, minimal refs, and next step.
---

# Ceratops Thread Side-Task Handoff

Produce one minimal copy-paste prompt for starting a side task in a new thread.

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

- Treat the original task as background. Include it in one short line only when needed.
- Optimize for the side task only. Ignore most of the original task unless it directly constrains the new thread.
- Produce a prompt, not a bundle and not instructions to use a follow-up handoff skill.
- Prefer the discovered conclusion and current objective over chronology.
- Include what stays in the current thread only when it matters for scope control.
- Keep refs exact but minimal.
- Treat `source-of-truth refs` as the minimum exact entities the new thread is likely to open immediately because they directly govern, define, or evidence the side task itself.
- Do not list general process instructions, generic runtime constraints, or merely helpful background artifacts as `source-of-truth refs` unless the side task is specifically about them or the first next step depends on opening them.
- Put active instructions or process constraints under constraints, not under `source-of-truth refs`, unless those instruction files are themselves part of the side task.
- If the user says `include the following questions`, `including the questions`, or equivalent wording, carry those questions into the prompt as next-thread asks instead of answering them here.
- Do not ask for credentials unless verifying the handoff requires protected state that cannot be inferred locally.

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

### 3. Emit a paste-ready prompt

- Make the current objective and first next step explicit.
- Write the prompt as direct instruction to the new thread, not as commentary about a handoff artifact.

## Completion Gate

- Verify the prompt includes the required content and enough exact refs to start correctly.
- Verify the prompt excludes irrelevant branches of the original task unless they materially constrain the side task.
- Verify each listed `source-of-truth ref` is first-step-relevant and authoritative for the side task itself, not just a generic constraint or a maybe-useful artifact.
- Verify the prompt does not pretend a fresh re-check happened when it did not.

## Output Contract

Emit one copy-paste prompt for a new thread and nothing extra.

## Example Invocation

`Use $ceratops-thread-side-task-handoff to create a copy-paste prompt for spinning this side issue into a new thread and keep the main task out unless it directly matters.`
