---
name: ceratops-gh-repo-health-audit
description: Audit and repair GitHub repository health with Ceratops defaults, using scripted live checks first for machine-checkable GitHub settings.
---

# Ceratops GH Repo Health Audit

Validate that an existing GitHub repo is clean, current, secure, documented, published, and not carrying leftover workflow debris. Apply low-risk reversible fixes directly and report risky, ambiguous, destructive, paid, or credential-bound fixes precisely. Treat the GitHub repo and artifact contracts as the first source of truth for machine-checkable live settings.

## Script Bundle

- Repo and artifact contract check: `python scripts/github_repo_artifact_contract.py --repo OWNER/REPO --scope all --preset health`
- Optional org contract check when org posture is in scope: `python scripts/github_org_contract.py --org ORG`
- Add `--json` when another step needs structured findings, and add `--check-id` or a narrower `--preset` when only a subset is relevant.

## Inputs To Capture

- Target repo and any expected posture that differs from the GH repo health contract or GH artifact contract.
- Local repo path and local consumers needed to classify stale or risky side effects.

Infer missing inputs from live repo state and local files before asking.

## Boundaries

- Use this skill when the task is primarily validation, stale-state cleanup, or safe repo-health repair and the repo has live GitHub state worth machine-checking.
- Do not use this skill as a routine rubber-stamp closeout pass after normal ship, dependency-update, or merge flows. Those skills should run only the narrow repo-health checks their own result actually needs.
- If the repo is not yet published or still needs first-time hardening, stop and use `$ceratops-gh-repo-create-and-publish`.
- If a safe fix turns into a content change that should go through normal PR and release flow, stop audit-only mode and use `$ceratops-gh-ship-change`.
- If only PR finalization remains after prior fixes, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect local and live state

- Inspect git status, remotes, branches, refs, tags, releases, generated files, artifacts, temp paths, package outputs, and local consumer references.
- Capture only the live GitHub metadata needed to run and interpret the contract check: default branch, visibility, security settings, branch protection or rulesets, and community profile when relevant.
- Inspect local workflow files when they are available so mutable external action refs are classified instead of inferred from repo settings alone.
- Expand to open PRs, releases, tags, branches, Actions runs, moderation detail, or published artifacts only when the script output, repo type, touched files, or the user's request makes them relevant.

### 2. Run live contract checks first

- Run the repo and artifact contract checker before treating GitHub settings as healthy.
- Blocking: Treat the contract checker output as the source of truth for machine-checkable live settings such as default-branch protection, branch protection or rulesets, required PR approvals, dependency graph, Dependabot alerts, Dependabot security updates, code scanning posture, secret scanning posture, workflow permission posture, delete-branch-on-merge, auto-merge, private vulnerability reporting state, community profile, repo content posture, stale queues, and artifact registry evidence.
- If the checker reports a warning, manual finding, or blind spot, decide whether the gap is acceptable, needs a manual follow-up, or should be fixed now.

### 3. Research only when the next decision needs it

- Check current official docs only where local files, live contract state, and the shared contracts leave the next fix or decision unresolved.
- Compare at most 1-2 strong current reference repos only for a concrete ambiguous files, metadata, workflow, security, or release question. Do not do broad GitHub health contract maintenance during routine repo audits.
- Use prose-only checks or the web UI only for settings that the bundled script or free APIs cannot currently verify.

### 4. Audit repo health

- Verify the GH repo health contract and GH artifact contract for the in-scope repo.
- When repo-tracked docs, configs, workflows, or automation prompts are intended for public GitHub, treat user-local absolute filesystem paths as a health gap and replace them with repo-relative paths or portable variables such as `$CODEX_HOME` unless an external runtime explicitly requires a local absolute path.

### 5. Repair safe gaps

- Apply low-risk reversible fixes directly, re-run the contract checker after each live GitHub change that could affect a reported repo-health check, and keep the final result grounded in fresh checker output rather than stale notes.
- Open or update a PR for repo changes when branch protection or repo policy requires it.
- Do not delete tags, releases, packages, protected branches, backup branches, or external artifacts unless the stale classification is proven and the action is safe or explicitly approved.

### 6. Validate and close

- Run the local checks needed to prove any repo-file changes are still valid.
- Verify live GitHub and registry state after each external change.
- Re-run the relevant contract checks at the end and classify every remaining failure, warning, or manual finding as fixed, intentionally retained, blocked, or not applicable.

## Completion Gate

- Verify the final answer is backed by a fresh relevant run of `scripts/github_repo_artifact_contract.py`.
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

`Use $ceratops-gh-repo-health-audit. Run the GitHub health contract checks first, fix safe repo-health gaps, and report only real blockers.`
