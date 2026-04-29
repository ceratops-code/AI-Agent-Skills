---
name: ceratops-skill-create
description: Create a brand-new Ceratops skill in `AI-Agent-Skills`, integrate it into the shared section system and repo metadata, validate the result with the needed checks, and make it available locally through the runtime `release/*` branch by default. Use when the user asks for a new Ceratops skill rather than an update to an existing one.
---

# Ceratops Skill Create

Create a brand-new Ceratops skill as a complete repo-integrated addition instead of leaving it as an isolated scaffold. Use `$skill-creator` only when raw scaffolding is needed, then integrate the new skill into the Ceratops section model, docs, metadata, and local runtime preview flow.

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
- Blocking: For skill runtime workflows, invoke shared helpers through installed console commands or `python -m <module>` entrypoints; do not locate shared helpers by absolute paths, by the repo's parent directory, or by per-skill `scripts` junctions.
- Blocking: When a Ceratops skill-maintenance workflow explicitly needs a repo-maintenance script, treat `scripts/<name>` paths as relative to the active `AI-Agent-Skills` checkout root; resolve that root from the current worktree with `git rev-parse --show-toplevel` or from the installed skill junction under `$CODEX_HOME/skills/<skill-name>`, and stop as blocked if neither resolves to a checkout containing `skills/`, `templates/`, and `scripts/`.
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
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Skill-Specific Rules

- Treat new-skill creation as complete only when the new skill folder, section assignments, generated shared block, metadata, and repo docs are aligned.
- Use `$skill-creator` only as the internal scaffolding step when a new folder or starter metadata is needed. Do not stop after scaffolding.
- Keep the new skill as delta-only as practical: reuse existing shared sections first, and add a new shared section only when it clearly reduces duplication or drift across multiple skills.
- Set both `interface.icon_small` and `interface.icon_large` in `agents/openai.yaml` to the shared Ceratops icon path `../../assets/ceratops-logo-500.png`.
- Use the default maintenance-check policy recorded in `templates/skill-sections.json` instead of making the user specify commands.
- Local runtime availability is part of completion by default. After the new skill validates, make an intentional commit on the worktree branch and continue with `$ceratops-codex-skill-stage-release` unless the user explicitly opts out.
- Do not publish to GitHub unless the user explicitly asked for shipping.

## Inputs To Capture

- The new skill's purpose, trigger conditions, and likely shared-section needs.
- Whether the new skill needs bundled scripts, references, or helper-runtime changes.
- Which repo surfaces must be updated: `skills/<name>/`, `templates/skill-sections.json`, `templates/sections/`, repo docs, sync or validation scripts, and any helper-runtime claims.
- Whether local runtime availability should be skipped despite the default.

Infer missing inputs from the repo's current structure and the user request before asking.

## Boundaries

- Use this skill when the task is creating a brand-new Ceratops skill in this repo.
- If the task is updating an existing Ceratops skill or the shared maintenance layer, stop and use `$ceratops-skill-update`.
- If the task is generic non-Ceratops skill scaffolding outside this repo, stop and use `$skill-creator`.
- If the task is only staging or shipping already-prepared changes, stop and use `$ceratops-codex-skill-stage-release` or `$ceratops-gh-codex-skill-ship`.

## Workflow

### 1. Design the new skill in repo context

- Inspect the current Ceratops skill family, shared sections, manifest assignments, repo docs, and any adjacent helper-runtime claims the new skill may touch.
- Decide whether the new skill can reuse existing sections or truly needs a new shared section.
- Decide whether raw scaffolding through `$skill-creator` is necessary or whether direct creation is cheaper and clearer.

### 2. Create the new skill and integrate it

- Scaffold the new skill folder when needed.
- Create or update `SKILL.md`, `agents/openai.yaml`, and any bundled resources, including the shared Ceratops icon metadata.
- Add the new skill to `templates/skill-sections.json`, assign the right shared sections, and update repo docs so the new skill is discoverable and described correctly.
- Update sync or validation scripts only when the new skill exposes a real gap in the current maintenance model.

### 3. Run the needed checks

- Because a new skill changes shared assignments, run the shared-source check path from `templates/skill-sections.json`: sync first, then validate.
- If helper-runtime code or claims changed, also run the helper-runtime smoke path from `templates/skill-sections.json`.
- Re-open the changed files from disk and confirm the generated shared block, manifest assignment, metadata, and docs all align.

### 4. Make it available locally

- Make an intentional commit on the worktree branch for the new skill once the local repo state is ready.
- Continue with `$ceratops-codex-skill-stage-release` so the new skill becomes available through the runtime `release/*` branch and installed local skill paths, unless the user explicitly opted out.
- If staging is blocked, report the blocker instead of presenting the new skill as locally available.

## Completion Gate

- Verify the new skill folder, manifest assignment, generated shared block, `agents/openai.yaml`, shared icon metadata, and repo docs all align.
- Verify the required sync or validation path ran successfully.
- Verify the new skill was committed and staged into the runtime local preview flow, unless the user explicitly opted out or a blocker prevented it.

## Output Contract

Report only:

- the new skill created
- any new shared sections or helper updates added with reasons
- unresolved blockers or non-blocking debt
- intentionally retained exceptions with reasons
- anything important not verified

## Example Invocation

`Use $ceratops-skill-create to create a new Ceratops skill for X, integrate it into the repo, run the needed checks, and make it available locally through the runtime release branch.`
