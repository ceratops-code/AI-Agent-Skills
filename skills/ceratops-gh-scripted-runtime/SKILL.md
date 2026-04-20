---
name: ceratops-gh-scripted-runtime
description: Shared runtime helper bundle for the parallel scripted Ceratops GitHub skill family. Use when maintaining the bundled live GitHub check scripts themselves.
---

# Ceratops GH Scripted Runtime

Maintain the shared helper scripts consumed by the parallel scripted Ceratops GitHub skill family.

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

## Inputs To Capture

- Which scripted Ceratops GH skills depend on the helper change.
- Which machine-checkable GitHub states or PR gates the helper should prove.
- Which current official GitHub docs or live APIs justify the helper behavior.

## Boundaries

- Use this skill only when maintaining the shared helper scripts consumed by the scripted Ceratops GH skill family.
- If the task is about running repo-health, publish, ship, merge, or dependency work itself, stop and use the corresponding scripted GH skill instead.

## Workflow

### 1. Verify the helper contract

- Re-check the official GitHub docs or live APIs that the helper relies on before changing helper logic.

### 2. Update the shared helper

- Keep the helper focused on machine-checkable live GitHub state.
- Prefer stable read paths and explicit structured output over prose parsing.

### 3. Validate dependents

- Update any scripted GH skills or local repo wrappers that depend on the helper path or behavior.
- Run the local validation commands needed to prove the helper still works.

## Credential Handling

- Do not ask for credentials unless validating the helper actually requires live GitHub state that cannot be read through the existing local auth path.

## Completion Gate

- Verify the helper still works from the repo-local wrapper path and the bundled skill-runtime path.
- Verify each dependent scripted skill still points at the correct helper location.

## Output Contract

Report only:

- helper behavior changed
- dependent scripted skills updated
- unresolved blockers or non-blocking debt
- anything important not verified
