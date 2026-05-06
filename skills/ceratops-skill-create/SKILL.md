---
name: ceratops-skill-create
description: Create a brand-new Ceratops skill in the skills repo, integrate it into the shared section system and repo metadata, validate the result with the needed checks, and make it available locally through the skills repo `release/*` branch by default. Use when the user asks for a new Ceratops skill rather than an update to an existing one.
---

# Ceratops Skill Create

## Goal

Create a brand-new Ceratops skill as a complete repo-integrated addition instead of leaving it as an isolated scaffold. Use `$skill-creator` only when raw scaffolding is needed, then integrate the new skill into the Ceratops section model, runtime payload model, docs, metadata, and local runtime preview flow.

## Context

### Inputs To Capture

- The new skill's purpose, trigger conditions, and likely shared-section needs.
- Whether the new skill needs bundled scripts, references, or helper-runtime changes.
- Which repo surfaces must be updated: `skills/<name>/`, `templates/skill-sections.json`, `templates/sections/`, runtime payload declarations, repo docs, runtime generation or validation scripts, and any helper-runtime claims.
- Whether local runtime availability should be skipped despite the default.

Infer missing inputs from the repo's current structure and the user request before asking.

## Constraints

### Skill-Specific Rules

- Treat new-skill creation as complete only when the new skill folder, section assignments, runtime-generation inputs, metadata, and repo docs are aligned.
- Use `$skill-creator` only as the internal scaffolding step when a new folder or starter metadata is needed. Do not stop after scaffolding.
- Keep the new source `SKILL.md` delta-only: reuse existing shared sections first, and add a new shared section only when it clearly reduces duplication or drift across multiple skills.
- Copy the repo-root Ceratops icon from `assets/ceratops-logo-500.png` into the new skill at `assets/ceratops-logo-500.png`, and set both `interface.icon_small` and `interface.icon_large` in `agents/openai.yaml` to `./assets/ceratops-logo-500.png`.
- Use the minimal same-surface maintenance-check policy recorded in `templates/skill-sections.json` instead of making the user specify commands.
- Local runtime availability is part of completion by default. After the new skill validates, make an intentional commit on the worktree branch and continue with `$ceratops-codex-skill-stage-release` unless the user explicitly opts out.
- Do not publish to GitHub unless the user explicitly asked for shipping.

### Boundaries

- Use this skill when the task is creating a brand-new Ceratops skill in this repo.
- If the task is generic non-Ceratops skill scaffolding outside this repo, stop and use `$skill-creator`.
- If the task is updating an existing Ceratops skill, maintaining the shared layer, or shipping already-prepared changes, stop because that work is outside this skill's scope.

### Workflow

#### 1. Design the new skill in repo context

- Inspect the current Ceratops skill family, shared sections, manifest assignments, repo docs, and any adjacent helper-runtime claims the new skill may touch.
- Decide whether the new skill can reuse existing sections or truly needs a new shared section.
- Decide whether raw scaffolding through `$skill-creator` is necessary or whether direct creation is cheaper and clearer.

#### 2. Create the new skill and integrate it

- Scaffold the new skill folder when needed.
- Create or update `SKILL.md`, `agents/openai.yaml`, and any bundled resources, including the skill-local Ceratops icon file and metadata.
- Add the new skill to `templates/skill-sections.json`, assign the right shared sections, and update repo docs so the new skill is discoverable and described correctly.
- Update runtime generation or validation scripts only when the new skill exposes a real gap in the current maintenance model.

#### 3. Run the needed checks

- (D) Because a new skill changes shared assignments, run the shared-source check path from `templates/skill-sections.json`.
- (D) If helper-runtime code or claims changed, run only the touched helper's own smoke command when that helper supports one.
- (D) Re-open the changed files from disk and confirm the source skill, runtime-generation inputs, manifest assignment, metadata, and docs all align.

#### 4. Make it available locally

- Make an intentional commit on the worktree branch for the new skill once the local repo state is ready.
- Continue with `$ceratops-codex-skill-stage-release` so the new skill becomes available through the skills repo `release/*` branch and generated local skill copy, unless the user explicitly opted out.
- If staging is blocked, report the blocker instead of presenting the new skill as locally available.

## Done When

### Completion Gate

- Verify the new skill folder, manifest assignment, runtime-generation inputs, `agents/openai.yaml`, skill-local icon file and metadata, and repo docs all align.
- Verify the required generation or validation path ran successfully.
- Verify the new skill was committed and staged into the skills repo local preview flow, unless the user explicitly opted out or a blocker prevented it.

### Output Contract

Report only:

- the new skill created
- any new shared sections or helper updates added with reasons
- unresolved blockers or non-blocking debt
- intentionally retained exceptions with reasons
- anything important not verified

### Example Invocation

`Use $ceratops-skill-create to create a new Ceratops skill for X, integrate it into the repo, run the needed checks, and make it available locally through the skills repo release branch.`
