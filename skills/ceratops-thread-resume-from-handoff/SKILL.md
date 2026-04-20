---
name: ceratops-thread-resume-from-handoff
description: Resume work in a new thread from a pasted handoff bundle. Use when Codex should treat the handoff as working state, refresh only the pieces needed for the next justified stage, and continue without re-checking the whole bundle.
---

# Ceratops Thread Resume From Handoff

Start a new thread from a handoff bundle without re-checking the whole bundle.

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

- Treat the handoff as working state by default, not as something to re-audit end-to-end.
- Validate only what matters for the next stage or final completion.
- Refresh stale pieces narrowly instead of rediscovering the whole task.
- Preserve useful handoff facts; replace only what is stale, wrong, or missing.
- Respect the handoff scope. Do not drift back into issues that the handoff explicitly left in the old thread unless the user broadens scope.
- Treat deferred questions in the handoff as in-scope next-thread work unless the user reprioritizes.

## Inputs To Capture

- The pasted handoff bundle
- Any user note about what changed after the handoff was created
- The next justified step claimed by the handoff
- Any deferred questions or next-thread asks carried by the handoff

## Boundaries

- Use this skill only when work moved into a new thread with a compact handoff bundle.
- If the work should continue in the same thread after a manual stop, stop and use `$ceratops-thread-resume-manual-stop`.
- If the work should continue in the same thread after a restart or crash, stop and use `$ceratops-thread-resume-after-restart`.

## Workflow

### 1. Parse the handoff

- Extract the handoff scope, any remaining scope left in the old thread, the current goal, claimed current state, unresolved issues, deferred questions, retained items, source-of-truth entities, and proposed next step.

### 2. Refresh only next-step dependencies

- Check only the repos, files, branches, PRs, releases, images, automations, or runtime signals that matter to the next step or final answer.
- Mark a handoff claim as stale, partially stale, or unverifiable only when that classification is needed to proceed safely or correct the answer.

### 3. Repair stale handoff state

- Refresh only the parts that changed or are needed to proceed safely.
- Remove low-risk stale leftovers that the handoff no longer needs.

### 4. Continue from the next justified stage

- Resume the task from the earliest unconfirmed or unfinished stage.
- Answer or execute deferred questions when they are part of the handed-off issue and no newer priority overrides them.
- Before completion, run the narrowest justified closure pass for the resumed task.

## Credential Handling

- Do not ask for credentials unless validating the handoff or continuing the task actually requires them.
- If credentials are required, ask only for the missing credential, why it is needed now, where it will be stored, and the exact command or setting the user must use.

## Completion Gate

- Verify the resumed task relies only on handoff claims that are still usable as-is or were refreshed narrowly where needed.
- Verify the resumed task state is coherent enough for the next action or final answer.

## Output Contract

Report only:

- any handoff claims that mattered and were stale or wrong
- the corrected current state
- the resumed stage or completed outcome
- unresolved blockers or non-blocking debt
- intentionally retained items with reasons, if material
- anything important not verified

## Example Invocation

`Use $ceratops-thread-resume-from-handoff to continue this pasted handoff in a new thread and refresh only what the next stage depends on.`
