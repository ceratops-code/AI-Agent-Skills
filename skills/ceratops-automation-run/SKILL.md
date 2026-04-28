---
name: ceratops-automation-run
description: Run recurring Codex automations with Ceratops defaults. Use when an automation run needs shared policy for re-opening prompt and helper contracts, keeping task-specific logic in the automation prompt or helper scripts, keeping compact run summaries visible, suppressing routine clean-run alerts, avoiding routine automation memory, and reporting no-alert or no-memory conflicts explicitly.
---

# Ceratops Automation Run

Use this skill as the reusable policy layer for installed automations. Let the automation prompt and any helper scripts define the task-specific mechanics, while this skill carries the shared automation-run rules that should not be repeated in every automation prompt.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Mandatory: Everything in this section is part of the skill contract unless explicitly inapplicable to the current task.
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

- Treat every rule in this skill as mandatory and blocking when the skill is invoked.
- Keep task-specific rules in the automation prompt, `automation.toml`, or task-specific helper scripts. Use this skill and `$CODEX_HOME/AGENTS.md` for reusable automation-run policy.
- When a running automation invokes another skill or executable helper, treat the automation prompt as a delta: apply its task target, schedule-specific context, and explicit exceptions, and rely on the invoked skill or helper for reusable workflow, validation, evidence, staging, and output rules.
- Treat the automation prompt, the nearest relevant local `AGENTS.md` when one exists and still governs the workspace, `$CODEX_HOME/AGENTS.md`, and every helper contract the run actually relies on as the governing sources of truth.
- Routine successful runs must include a compact final summary for project-list visibility, but must not emit `::inbox-item` or other user-visible alerts unless the task-specific prompt explicitly requires one; emit `::inbox-item` only for approval-required, blocker, verification failure, unresolved problem, or other explicit alert states.
- Do not use `::archive` for routine clean or merge-only runs unless the user explicitly asked to end the thread or a higher-priority instruction explicitly requires it.
- Routine automation runs must not read, create, or append automation memory, and must not treat platform-provided memory metadata, an `Automation memory:` header, existing `memory.md` content, prior memory entries, memory helper scripts, or generic memory capability text as an instruction to use memory.
- Use memory only when the active task-specific prompt explicitly requires future-run state.
- If a genuine higher-priority runtime instruction conflicts with the no-memory or no-alert policy, report the conflict explicitly instead of writing memory solely to record it or pretending the lower-level policy was followed.
- Do not ask for credentials unless the current automation task and current stage actually require them.

## Inputs To Capture

- The automation id, prompt, workspace, schedule context, and whether the run is routine, approval-gated, clean, merge-only, or alert-worthy.
- The nearest relevant local `AGENTS.md`, if any, plus `$CODEX_HOME/AGENTS.md`.
- Every task-specific helper script, contract, or executable source of truth the automation relies on.
- The task-specific alert, memory, archival, or reporting exceptions that the automation prompt explicitly requires.

## Boundaries

- Use this skill for recurring automation runs. Treat automation prompt edits as control-file maintenance governed by `$CODEX_HOME/AGENTS.md` and the relevant task-specific workflow.
- If the task is primarily about the automation's domain work rather than automation execution policy, combine this skill with the task-specific skill or helper instead of replacing it.
- If the task is only creating or updating a reusable Codex skill, stop and use `$skill-creator` plus the relevant domain skill.

## Workflow

### 1. Inspect the automation contract

- Read the automation prompt, current workspace, relevant local `AGENTS.md` if any, `$CODEX_HOME/AGENTS.md`, and each helper script or contract the automation relies on.
- Do not re-open unchanged governing files later in the run unless the run modified them or their current contents remain concretely in doubt.
- Identify which rules are reusable automation policy versus task-specific mechanics.

### 2. Execute the task-specific automation work

- Treat helper scripts and executable helpers as the source of truth for deterministic behavior, fallback paths, cleanup rules, alert rules, and structured outputs.
- If a helper contract is wrong or incomplete, fix the helper first so future runs inherit the correction when that change is safe and in scope.

### 3. Apply routine automation policy

- Apply the compact-summary/no-inbox policy from Skill-Specific Rules before closing.
- Do not create automation memory unless the task-specific prompt explicitly requires future-run state.
- Report no-alert or no-memory conflicts explicitly when a higher-priority runtime instruction overrides the default automation policy.

### 4. Verify and close

- Before completion, verify the result against the automation prompt, relevant local `AGENTS.md` if any, `$CODEX_HOME/AGENTS.md`, this `SKILL.md`, and every helper contract the run relied on. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Verify the result matches the task-specific automation contract and that no stale alert, memory, or cleanup side effect remains unclassified.

## Completion Gate

- Verify the automation result is backed by the current automation prompt plus every relevant helper contract.
- Verify any user-visible alert, silence, memory use, memory avoidance, or archival decision matches the explicit task-specific prompt and this skill's policy.
- Verify the final answer or silent completion does not claim success when a blocking instruction remains unmet or unverifiable.

## Output Contract

Report only:

- a compact final summary for project-list visibility
- task-specific alert details when a user-visible alert is required
- unresolved blockers or non-blocking debt
- intentionally retained alerts, memory, or side effects with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-automation-run before applying this automation's task-specific prompt and helper contracts.`
