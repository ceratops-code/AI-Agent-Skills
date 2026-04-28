---
name: ceratops-task-execute-in-stages
description: Drive substantial tasks through staged contingent execution with Ceratops defaults. Use when Codex should diagnose first, prefer the simplest standard fix, advance only to the next justified stage, ask before complex or high-maintenance solutions, and finish with a risk-based closure pass.
---

# Ceratops Task Execute In Stages

Use staged contingent execution for substantial tasks with meaningful side effects or multiple possible solution paths.

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

- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Skill-Specific Rules

- Diagnose first.
- Prefer the simplest standard fix that can credibly solve the problem.
- Advance only to the next justified stage.
- If a stage reveals new in-scope issues, fix them and continue until clean or blocked.
- Before taking a complex, invasive, nonstandard, or high-maintenance path, first rule out simpler options or explain why they are inadequate, then ask before implementing it.
- Minimize routine progress commentary. Interrupt only for blockers, credentials, risky or destructive decisions, material scope changes, or complex-path approval.
- Reuse unchanged state and batch related inspection instead of repeating exploratory probes.
- Do not ask for credentials unless the current justified stage actually requires them.

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
