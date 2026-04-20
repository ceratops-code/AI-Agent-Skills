---
name: ceratops-task-execute-in-stages
description: Drive substantial tasks through staged contingent execution with Ceratops defaults. Use when Codex should diagnose first, prefer the simplest standard fix, advance only to the next justified stage, ask before complex or high-maintenance solutions, and finish with a risk-based closure pass.
---

# Ceratops Task Execute In Stages

Use staged contingent execution for substantial tasks with meaningful side effects or multiple possible solution paths.

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
- If the task is only same-thread resume after a manual stop, stop and use `$ceratops-thread-resume-manual-stop`.
- If the task is only same-thread resume after a restart or crash, stop and use `$ceratops-thread-resume-after-restart`.
- If the task is only moving work to a new thread, stop and use `$ceratops-thread-create-handoff` or `$ceratops-thread-resume-from-handoff` as appropriate.

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
