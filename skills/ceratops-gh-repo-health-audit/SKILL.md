---
name: ceratops-gh-repo-health-audit
description: Audit and repair GitHub repository health with Ceratops defaults, using scripted live checks first for machine-checkable GitHub settings.
---

# Ceratops GH Repo Health Audit

Validate that an existing GitHub repo is clean, current, secure, documented, published, and not carrying leftover workflow debris. Apply low-risk safe fixes directly and report risky, ambiguous, destructive, paid, or credential-bound fixes precisely. Treat the bundled GitHub helper scripts as the first source of truth for machine-checkable live settings.

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

<!-- SECTION SOURCE: templates/sections/gh-current-state.md -->

## GH Current State

- Use the shared helper package `ceratops_gh_current_state` for bundled GitHub current-state checks when it covers the next decision.
- Use `gh`, GitHub API, and `ceratops_gh_current_state` as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.

<!-- SECTION SOURCE: templates/sections/gh-repo-health-contract.md -->

## GH Repo Health Contract

- Apply this contract to repo creation, first-time hardening, repo-health audit, and repo-health repair. For normal ship, dependency-update, or merge runs, apply only the parts made stale by the current change or needed for a final repo-health claim.
- Capture or verify the repo identity and public contract: owner, name, default branch, visibility, topics, homepage, support route, CODEOWNERS owners, and local consumers tied to the repo path.
- Execute or verify public repo files when relevant: `README`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, issue intake, pull request intake, support routing, CI, release workflows, dependency update automation, and code scanning config.
- Execute or verify GitHub process settings when relevant: default-branch protection or rulesets, real required checks, strict status checks, pull-request flow, required reviews, stale review dismissal, conversation resolution, admin enforcement, force-push bans, deletion bans, auto-merge, and delete-branch-on-merge.
- For private repos where GitHub returns a plan-limited branch-protection or rulesets response, classify the paid requirement explicitly instead of treating the repo as proven unprotected; do not make or imply a clean protection claim until an eligible paid plan, public visibility, or another live enforcement source verifies it.
- Execute or verify public-repo security and moderation when available at no extra cost: private vulnerability reporting or an explicit private reporting path, Dependabot security updates, dependency graph, secret scanning, push protection, code scanning, community profile, and reported-content or moderation health.
- Execute or verify workflow hardening when repo workflows are present: every non-local action should use a verified full SHA with a same-line release comment, `sha_pinning_required` should be enabled once workflows are compliant, and reusable workflow tag refs should be classified deliberately.
- When `.github/dependabot.yml` explicitly assigns `labels: dependencies`, create or verify the live repo label `dependencies`.
- Run the bundled repo-health script after GitHub settings changes that could affect a reported check and whenever the final answer relies on repo-health settings.
- Verify or classify stale PRs, branches, tags, releases, generated files, local path references, old automation references, security alerts, code-scanning alerts, maturity findings, and process alerts when they are in scope.

<!-- SECTION SOURCE: templates/sections/gh-artifact-contract.md -->

## GH Artifact Contract

- Apply this contract only when the repo has an external artifact, the current change affects a releasable artifact, or the final answer makes an artifact or no-artifact claim.
- Identify the real deliverable from the project instead of forcing Docker, PyPI, or any other registry by default.
- Capture or verify the artifact identity, registry target, version source, release policy, tag style, changelog or release-note source, and post-publish consumer check.
- In audit-only flows, verify and classify artifact state; do not publish or mutate registry artifacts unless the workflow explicitly moves into a ship or publish skill.
- Build, package, install, pull, run, or consume local artifacts enough to catch packaging and runtime failures before publishing or before making a local artifact-health claim.
- Publish external artifacts only when repo policy and the merged change require a release, tag, package, image, module, binary, or other public artifact.
- Derive versions from trustworthy project metadata and tag history instead of inventing semantics.
- Verify live release and registry endpoints after publishing or when auditing artifact state, including tags, digests, package pages, release pages, and published artifacts.
- Prefer registry-supported trusted publishing, OIDC, or another short-lived identity path over repository-stored long-lived publish tokens when supported by the real registry; keep any token-based fallback explicit and scoped.
- For PyPI publishes, prefer Trusted Publishing or another short-lived identity path over repository-stored long-lived tokens when supported, build the intended sdist and wheel, publish the intended version, verify the live PyPI version, install that exact version from PyPI locally, and run the smoke or documented consumer check against the published artifact instead of an editable checkout.
- For PyPI publishes that emit attestations or provenance, verify the metadata through PyPI or the selected verifier instead of relying only on upload success.
- For npm publishes, prefer trusted publishing when the package and runner meet current npm prerequisites, run the package's build and test path, publish the intended version, verify the live npm package and version, and verify provenance when npm generated it.
- For Docker or OCI image publishes, build locally, run a smoke test, publish the intended tags or digests, verify the live registry state, pull or consume the published image when relevant, and verify provenance or SBOM attestations when the selected publish flow emits them.

<!-- SECTION SOURCE: templates/sections/gh-findings.md -->

## GH Findings

- Classify only findings actually inspected in this run. Do not expand reporting to untouched queues unless they become the next actionable work or the user explicitly asked for full coverage.
- For each inspected finding, decide whether it is safe, fix low-risk items directly when in scope, and for every finding left open report its name or id, whether it is blocking, why it remains open, and the concrete work needed to clear it.
- Do not collapse retained findings into a generic healthy result.
- Re-check findings whose status may have changed because of actions taken in this run.
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Script Bundle

- Repo settings and moderation check: `python -m ceratops_gh_current_state repo-health --repo OWNER/REPO`
- Add `--json` when another step needs structured findings.

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
- Capture only the live GitHub metadata needed to run and interpret the bundled repo-health check: default branch, visibility, security settings, branch protection or rulesets, and community profile when relevant.
- Inspect local workflow files when they are available so mutable external action refs are classified instead of inferred from repo settings alone.
- Expand to open PRs, releases, tags, branches, Actions runs, moderation detail, or published artifacts only when the script output, repo type, touched files, or the user's request makes them relevant.

### 2. Run live repo checks first

- Run the bundled repo-health script before treating GitHub settings as healthy.
- Treat the script output as the source of truth for machine-checkable live settings such as `content_reports_enabled`, default-branch protection, strict status checks, required PR approvals, stale review dismissal, conversation resolution, admin enforcement, force-push or deletion bans, code scanning default setup, secret scanning, push protection, Dependabot security updates, `sha_pinning_required`, delete-branch-on-merge, auto-merge, and private vulnerability reporting state.
- If the script reports a warning or blind spot, decide whether the gap is acceptable, needs a manual follow-up, or should be fixed now.

### 3. Research only when the next decision needs it

- Check current official docs only where local files, live scripted state, and the shared contracts leave the next fix or decision unresolved.
- Compare at most 1-2 strong current reference repos only for a concrete ambiguous files, metadata, workflow, security, or release question. Do not do broad GH-skill best-practice maintenance during routine repo audits.
- Use prose-only checks or the web UI only for settings that the bundled script or free APIs cannot currently verify.

### 4. Audit repo health

- Verify the GH repo health contract and GH artifact contract for the in-scope repo.
- When repo-tracked docs, configs, workflows, or automation prompts are intended for public GitHub, treat user-local absolute filesystem paths as a health gap and replace them with repo-relative paths or portable variables such as `$CODEX_HOME` unless an external runtime explicitly requires a local absolute path.

### 5. Repair safe gaps

- Apply low-risk fixes directly, re-run the script after each live GitHub change that could affect a reported repo-health check, and keep the final result grounded in fresh script output rather than stale notes.
- Open or update a PR for repo changes when branch protection or repo policy requires it.
- Do not delete tags, releases, packages, protected branches, backup branches, or external artifacts unless the stale classification is proven and the action is safe or explicitly approved.

### 6. Validate and close

- Run the local checks needed to prove any repo-file changes are still valid.
- Verify live GitHub and registry state after each external change.
- Re-run the repo-health script at the end and classify every remaining failure or warning as fixed, intentionally retained, blocked, or not applicable.

## Completion Gate

- Verify the final answer is backed by a fresh run of `python -m ceratops_gh_current_state repo-health`.
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
