---
name: ceratops-gh-repo-health-audit
description: Audit and repair GitHub repository health with Ceratops defaults, using scripted live checks first for machine-checkable GitHub settings.
---

# Ceratops GH Repo Health Audit

Validate that an existing GitHub repo is clean, current, secure, documented, published, and not carrying leftover workflow debris. Apply low-risk safe fixes directly and report risky, ambiguous, destructive, paid, or credential-bound fixes precisely. Treat the bundled GitHub helper scripts as the first source of truth for machine-checkable live settings.

<!-- CERATOPS_COMMON_CORE_START -->
## Core Rules

- Everything in this skill is mandatory unless explicitly marked optional or inapplicable.
- Before completion, re-open this `SKILL.md` and verify the work line by line against `Core Rules`, `Inputs To Capture`, `Boundaries`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract`.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- For GitHub or registry tasks only, use `gh`, GitHub API, and `ceratops_gh_runtime` as part of the first-pass direct evidence before checking current official docs or `gh` help.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- For every open security, code-scanning, maturity, or process alert you inspect, decide whether it is safe, fix low-risk items directly, and for every alert not fixed report its name or id, whether it is blocking, why it is not being fixed now, and the concrete work needed to clear it. Do not collapse retained alerts into a generic healthy result.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.
<!-- CERATOPS_COMMON_CORE_END -->

## Script Bundle

- Shared helper package: `ceratops_gh_runtime`
- Repo settings and moderation check: `python -m ceratops_gh_runtime repo-health --repo OWNER/REPO`
- Add `--json` when another step needs structured findings.

## Inputs To Capture

- Repo owner or name, default branch, intended visibility, intended owner or org, and whether Ceratops ownership is actually desired.
- Expected artifacts and registries, if any.
- Expected branch protection, CI checks, release policy, dependency update policy, security posture, topics, CODEOWNERS, and support path.
- Actions policy, including whether unpinned action refs are accepted debt for now or should be brought to full-SHA enforcement in this run.
- Local repo path, local consumer paths, generated files, shortcuts, services, shell profiles, Docker MCP overrides, and automation configs tied to the repo.

Infer missing inputs from live repo state and local files before asking.

## Boundaries

- Use this skill when the task is primarily validation, stale-state cleanup, or safe repo-health repair and the repo has live GitHub state worth machine-checking.
- If the repo is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-repo-create-and-publish`.
- If a safe fix turns into a content change that should go through normal PR and release flow, stop audit-only mode and use `$ceratops-gh-ship-change`.
- If only PR finalization remains after prior fixes, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect local and live state

- Inspect git status, remotes, branches, refs, tags, releases, generated files, artifacts, temp paths, package outputs, and local consumer references.
- Inspect live GitHub repo metadata, topics, description, default branch, open PRs, branches, tags, releases, Actions runs, code scanning, Dependabot, security settings, branch protection, rulesets, and community profile.
- Inspect local workflow files when they are available so mutable external action refs are classified instead of inferred from repo settings alone.
- For public repos, inspect live community-profile moderation signals such as reported-content health and `content_reports_enabled`, not just file completeness and security alerts.
- Inspect published packages or images relevant to the repo.

### 2. Run live repo checks first

- Run the bundled repo-health script before treating GitHub settings as healthy.
- Treat the script output as the source of truth for machine-checkable live settings such as `content_reports_enabled`, default-branch protection, strict status checks, required PR approvals, stale review dismissal, conversation resolution, admin enforcement, force-push or deletion bans, code scanning default setup, secret scanning, push protection, Dependabot security updates, `sha_pinning_required`, delete-branch-on-merge, auto-merge, and private vulnerability reporting state.
- If the script reports a warning or blind spot, decide whether the gap is acceptable, needs a manual follow-up, or should be fixed now.

### 3. Research only when the next decision needs it

- Check current official docs for GitHub community health, moderation, branch protection or rulesets, Actions, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and each relevant ecosystem or registry only where the next fix or decision needs that evidence or where live scripted state and docs appear to disagree.
- Compare 2-3 strong current reference repos only for a concrete ambiguous files, metadata, workflow, security, or release question. Do not do broad GH-skill best-practice maintenance during routine repo audits.
- Use prose-only checks or the web UI only for settings that the bundled script or free APIs cannot currently verify.

### 4. Audit repo health

- Verify README accuracy, install or run instructions, release notes, changelog, support path, and registry links.
- When repo-tracked docs, configs, workflows, or automation prompts are intended for public GitHub, treat user-local absolute filesystem paths as a health gap and replace them with repo-relative paths or portable variables such as `$CODEX_HOME` unless an external runtime explicitly requires a local absolute path.
- Verify `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, issue intake, pull request template, support routing, CI, release workflows, dependency update automation, and code scanning config when relevant.
- Verify public repo security posture: private vulnerability reporting or an explicit private reporting path, Dependabot security updates, secret scanning, push protection, code scanning, dependency graph, and current alert state when available at no extra cost.
- Verify default-branch protection with real checks, strict status checks, PR flow, review policy, stale review dismissal, conversation resolution, admin enforcement, no force pushes, and no deletions as appropriate for the repo.
- Audit `.github/workflows` for mutable external action refs. Treat non-SHA action refs as a hardening gap, and treat them as an active breakage if `sha_pinning_required` is already enabled. Reusable workflows referenced by tag are allowed by GitHub's enforcement but should still be classified deliberately.
- Verify topics are precise and current, and CODEOWNERS contains only valid current owners.
- Verify versions, tags, releases, package metadata, image digests, and latest-release pointers match intended state.
- Audit the repo end to end for open security, code-scanning, maturity, and process alerts from GitHub, CI, dependency tooling, scorecards, and equivalent live signals relevant to the repo.
- Decide whether each alert is safe, fix low-risk items directly, and for every alert left open report its name or id, blocking status, why it is not being fixed now, and the concrete work needed to clear it.
- Verify no stale PRs, branches, tags, releases, generated files, local path references, or old automation references remain unclassified.

### 5. Repair safe gaps

- Apply low-risk fixes directly, re-run the script after each live GitHub change, and keep the final result grounded in fresh script output rather than stale notes.
- When the repo is available locally, pin safe external action refs to verified upstream SHAs with same-line release comments before enabling the repo-level SHA-pinning setting.
- Open or update a PR for repo changes when branch protection or repo policy requires it.
- Do not delete tags, releases, packages, protected branches, backup branches, or external artifacts unless the stale classification is proven and the action is safe or explicitly approved.

### 6. Validate and close

- Run the local checks needed to prove any repo-file changes are still valid.
- Verify live GitHub and registry state after each external change.
- Re-check PRs, branches, releases, tags, security settings, CI, code scanning, topics, community files, package endpoints, and local cleanliness after fixes.
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

- Verify the final answer is backed by a fresh run of `python -m ceratops_gh_runtime repo-health`.
- Verify any Actions hardening claim is backed by a fresh local workflow scan when the repo files were available in the run.
- Verify live state for every touched repo setting, security control, branch protection rule, PR, branch, tag, release, workflow, code scanning result, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact, temp path, cache, credential change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.

## Output Contract

Report only:

- health gaps fixed
- alerts or findings left open with name or id, blocking status, why they remain open, and the concrete work needed to clear them
- health gaps intentionally retained with exact reasons
- remaining blockers or credential steps
- anything important not verified
- paid requirement with product, reason, and price if encountered

## Example Invocation

`Use $ceratops-gh-repo-health-audit. Run the bundled live GitHub checks first, fix safe repo-health gaps, and report only real blockers.`
