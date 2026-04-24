---
name: ceratops-task-execute-in-stages
description: Drive substantial tasks through staged contingent execution with Ceratops defaults. Use when Codex should diagnose first, prefer the simplest standard fix, advance only to the next justified stage, ask before complex or high-maintenance solutions, and finish with a risk-based closure pass.
---

# Ceratops Task Execute In Stages

Use staged contingent execution for substantial tasks with meaningful side effects or multiple possible solution paths.

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
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Diagnose first.
- Prefer the simplest standard fix that can credibly solve the problem.
- Advance only to the next justified stage.
- If a stage reveals new in-scope issues, fix them and continue until clean or blocked.
- Before taking a complex, invasive, nonstandard, or high-maintenance path, first rule out simpler options or explain why they are inadequate, then ask before implementing it.
- Minimize routine progress commentary. Interrupt only for blockers, credentials, risky or destructive decisions, material scope changes, or complex-path approval.
- Reuse unchanged state and batch related inspection instead of repeating exploratory probes.

## Inputs To Capture

- The concrete problem, desired outcome, and completion standard.
- The candidate stages that may become relevant: diagnosis, local fix, local verification, publish or install, upstreaming, and closure.
- The current local and remote entities most likely to constrain the next stage.

## Stage Model

Choose only the stages the task actually justifies:

1. Diagnose and narrow the problem.
2. Implement the simplest credible local fix.
3. Verify locally.
4. Publish, install, or use the published artifact locally when the task requires it.
5. Upstream or propagate the relevant change when justified.
6. Run the narrowest justified closure pass and remove low-risk stale leftovers.

## Boundaries

- Use this skill for substantial tasks with multiple justified stages or multiple plausible solution paths.
- If the task is only same-thread resume after a manual stop, restart, or crash, stop and use `$ceratops-thread-resume-manual-stop`.
- If the task is only moving a whole task to a new thread, stop and use `$ceratops-thread-full-handoff`.
- If the task is only spinning a sub-issue into a new thread, stop and use `$ceratops-thread-side-task-handoff`.

## Workflow

### 1. Diagnose

- Identify the concrete failure, desired outcome, and plausible solution range.
- Gather only the evidence needed to choose the next justified stage.

### 2. Prefer the simplest credible path

- Try the simplest standard fix first when it has a realistic chance to work.
- If simpler options fail, keep the evidence that justifies escalating.

### 3. Execute stage by stage

- Do not publish before local verification unless the environment makes that impossible.
- Do not upstream before the local or published fix is credible.
- Do not stop at diagnosis if the task remains fixable.

### 4. Close with the right scope

- Choose the narrowest justified closure scope based on side effects and stale-state surface.
- Report only unresolved blockers, unresolved non-blocking debt, intentionally retained items, and anything important not verified.

## Credential Handling

- Do not ask for credentials unless the current justified stage actually requires them.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the task reached the furthest justified clean stage or an explicit blocker.
- Verify the final answer reports only unresolved blockers, unresolved non-blocking debt, intentionally retained items, and anything important not verified.

## Best Uses

- New bugs or regressions where the right fix is not yet known
- Dependency or security update work
- Tooling, packaging, publishing, or runtime problems
- Multi-stage tasks that may require research, implementation, publish, verification, cleanup, and upstream follow-through

## Example Invocation

`Use $ceratops-task-execute-in-stages to handle this substantial task end to end, trying the simplest standard fix first and asking before any complex path.`
