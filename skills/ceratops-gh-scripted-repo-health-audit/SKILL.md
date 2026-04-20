---
name: ceratops-gh-scripted-repo-health-audit
description: Audit and repair GitHub repository health with a scripted live-check layer first, keeping the original Ceratops GH skill family intact alongside this parallel variant.
---

# Ceratops GH Scripted Repo Health Audit

Use the same repo-health scope as `$ceratops-gh-repo-health-audit`, but treat the bundled GitHub helper scripts as the first source of truth for machine-checkable live settings.

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
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper path relative to this skill: `..\ceratops-gh-scripted-runtime\scripts\gh_live_checks.py`
- Repo settings and moderation check: `python <resolved-helper-path> repo-health --repo OWNER/REPO`
- Add `--json` when another step needs structured findings.

## Inputs To Capture

- Repo owner or name, default branch, intended visibility, intended owner or org, and whether Ceratops ownership is actually desired.
- Expected artifacts and registries, if any.
- Expected branch protection, CI checks, release policy, dependency update policy, security posture, topics, CODEOWNERS, and support path.
- Local repo path, local consumer paths, generated files, shortcuts, services, shell profiles, Docker MCP overrides, and automation configs tied to the repo.

Infer missing inputs from live repo state and local files before asking.

## Boundaries

- Use this skill when the task is primarily validation, stale-state cleanup, or safe repo-health repair and the repo has live GitHub state worth machine-checking.
- If the repo is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-scripted-repo-publish`.
- If a safe fix turns into a content change that should go through normal PR and release flow, stop audit-only mode and use `$ceratops-gh-scripted-repo-ship-change`.
- If only PR finalization remains after prior fixes, stop and use `$ceratops-gh-scripted-merge-pr`.

## Workflow

### 1. Inspect local scope

- Inspect git status, remotes, branches, refs, tags, releases, generated files, artifacts, temp paths, and local consumer references before deciding what needs repair.

### 2. Run live repo checks first

- Run the bundled repo-health script before treating GitHub settings as healthy.
- Treat the script output as the source of truth for machine-checkable live settings such as `content_reports_enabled`, default-branch protection, strict status checks, required PR approvals, stale review dismissal, conversation resolution, admin enforcement, force-push or deletion bans, code scanning default setup, secret scanning, push protection, Dependabot security updates, delete-branch-on-merge, auto-merge, and private vulnerability reporting state.
- If the script reports a warning or blind spot, decide whether the gap is acceptable, needs a manual follow-up, or should be fixed now.

### 3. Research only what the script cannot prove

- Check current official docs for GitHub community health, moderation, branch protection or rulesets, Actions, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and each relevant ecosystem or registry only where the next fix or decision needs that evidence.
- Use prose-only checks or the web UI only for settings that the bundled script or free APIs cannot currently verify.

### 4. Repair safe gaps

- Apply low-risk fixes directly, re-run the script after each live GitHub change, and keep the final result grounded in fresh script output rather than stale notes.
- Open or update a PR for repo changes when branch protection or repo policy requires it.

### 5. Validate and close

- Run the local checks needed to prove any repo-file changes are still valid.
- Re-run the repo-health script at the end and classify every remaining failure or warning as fixed, intentionally retained, blocked, or not applicable.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which GitHub or registry credential is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists.

## Completion Gate

- Verify the final answer is backed by a fresh run of `python <resolved-helper-path> repo-health`.
- Verify local state for every touched repo, worktree, generated file, artifact, temp path, cache, credential change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.

## Output Contract

Report only:

- health gaps fixed
- live GitHub findings fixed and findings left open with check name, blocking status, why they remain open, and the concrete work needed to clear them
- health gaps intentionally retained with exact reasons
- remaining blockers or credential steps
- live GitHub, security, CI, release, and registry verification results
- branches, PRs, tags, releases, local paths, temp paths, or artifacts removed or retained
- paid requirement with product, reason, and price if encountered

## Example Invocation

`Use $ceratops-gh-scripted-repo-health-audit. Run the bundled live GitHub checks first, fix safe repo-health gaps, and report only real blockers.`
