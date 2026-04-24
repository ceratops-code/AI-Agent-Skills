---
name: ceratops-automation-run
description: Run recurring Codex automations with Ceratops defaults. Use when an automation prompt needs shared policy for re-opening prompt and helper contracts, keeping task-specific logic in the automation prompt or helper scripts, suppressing routine clean-run alerts, avoiding routine automation memory, and reporting no-alert or no-memory conflicts explicitly.
---

# Ceratops Automation Run

Use this skill as the reusable policy layer for installed automations. Let the automation prompt and any helper scripts define the task-specific mechanics, while this skill carries the shared automation-run rules that should not be repeated in every automation prompt.

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

<!-- SOURCE: templates/fragments/core-credentials.md -->

## Credential Handling

- Apply this section unless a skill-specific credential rule narrows it further.
- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target
<!-- CERATOPS_COMMON_CORE_END -->

## Skill-Specific Rules

- Treat every rule in this skill as mandatory and blocking when the skill is invoked.
- Keep task-specific rules in the automation prompt, `automation.toml`, or task-specific helper scripts. Use this skill and `$CODEX_HOME/AGENTS.md` for reusable automation-run policy.
- Use the automation prompt, the nearest relevant local `AGENTS.md` when one exists and still governs the workspace, `$CODEX_HOME/AGENTS.md`, and every helper contract the run relies on as source-of-truth inputs. Read each one once when needed, then re-open only files changed in this run or whose current contents remain concretely in doubt.
- Clean and merge-only runs may complete silently or through non-alert bookkeeping, but must not create inbox items or other user-visible alerts unless the task-specific prompt explicitly requires one.
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

- Use this skill for recurring automation runs and for editing automation prompts so shared automation-run policy stays reusable instead of duplicated.
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

- Keep routine clean and merge-only runs quiet unless the task-specific prompt explicitly requires a user-visible alert.
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

- the task-specific automation result when user-visible output is required
- unresolved blockers or non-blocking debt
- intentionally retained alerts, memory, or side effects with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-automation-run before applying this automation's task-specific prompt and helper contracts.`
