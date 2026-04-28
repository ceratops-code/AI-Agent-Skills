---
name: ceratops-gh-repo-create-and-publish
description: Create, fork, or production-harden a local software project as a public GitHub repository and publish the correct public artifact registry output with Ceratops defaults, using live scripted GitHub checks before closing.
---

# Ceratops GH Repo Create And Publish

Turn a local project into a real public GitHub repository and the right published artifact with minimal back-and-forth. Use the free path by default, prefer public visibility only after verifying the project is safe to expose, and prove machine-checkable live GitHub settings with the bundled helper scripts before closing.

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

## Skill-Specific Rules

- Do not prefer connector storage over normal local credential stores.

## Script Bundle

- Repo settings check: `python -m ceratops_gh_current_state repo-health --repo OWNER/REPO`

## Inputs To Capture

- GitHub owner or org. Prefer `ceratops-code` only when user or existing org context explicitly indicates Ceratops ownership and access is available at no extra cost.
- Repo name, default branch, visibility, branch naming, and whether the repo should remain a fork.
- Maintainer merge policy: by Ceratops default, require 1 approving review on the default branch and add a pull-request-only bypass for the authenticated maintainer role or account so the owner can still self-ship; only choose a different review policy when the user explicitly asks for it.
- Any missing inputs required by the GH repo health contract or GH artifact contract.

Infer the safest practical default unless the choice is risky, destructive, ambiguous, or credential-bound.

## Boundaries

- Use this skill for first-time publication, repo creation or forking, visibility decisions, initial hardening, and first release setup.
- If the repo already exists and only local changes or a normal release need shipping, stop and use `$ceratops-gh-ship-change`.
- If the user only wants a state check, stale-item cleanup, or settings validation on an existing repo, stop and use `$ceratops-gh-repo-health-audit`.
- If only PR finalization remains, stop and use `$ceratops-gh-merge-pr`.

## Workflow

### 1. Inspect local state

- Inspect git state, tags, branches, remotes, ignored files, generated artifacts, README, license, CI files, docs, security files, manifests, lockfiles, package metadata, and existing release data.
- Identify the real build, lint, test, package, publish, and release commands from local files.
- Identify whether the project is a library, app, CLI, service, module, template, fork, or internal snapshot that needs cleanup before publishing.
- If renaming or moving anything, audit and update local consumers before closing.

### 2. Research and decide only where the next choice needs it

- Default to the narrowest evidence that answers the next publish or hardening decision: local project files first, then the selected registry or GitHub docs for the actual project type.
- Check current official docs only where a repo-health or artifact-contract decision remains unresolved by local files and live state.
- Compare at most 1-2 strong reference repos only for a concrete ambiguous repo-structure, security, release, or packaging question. Do not do broad GH-skill best-practice maintenance during routine publish runs.
- Do not choose paid features unless they are already available at no extra cost.

### 3. Execute repo and artifact contracts

- Execute the GH repo health contract as creation and hardening work, not as passive audit.
- Execute the GH artifact contract only for the real deliverable.
- Replace internal, misleading, or broken defaults before publication.
- Add ecosystem-standard manifests and metadata only when relevant to the actual project type.

### 4. Configure GitHub and prove the result

- Create or fork the GitHub repo, preserve upstream linkage when needed, push the repo, and verify the live endpoint.
- Turn off unused live features such as wiki or projects when the repo does not actually use them.
- When the host supports repository rulesets, implement the maintainer exception as a pull-request-only ruleset bypass for the authenticated maintainer role or account instead of relying only on classic branch-protection bypass allowances.
- Do not assume repo-creation defaults already produced the intended repo-health settings.

### 5. Validate and publish

- Run the relevant local validation, ensure the latest relevant CI and code-scanning runs on the default branch are green, and publish the real external artifact only when the project actually has one.
- If a single-maintainer fixture or sandbox repo needs one last hardening PR and GitHub self-approval rules would otherwise deadlock the run, merge that PR with `gh pr merge --admin` using the allowed method instead of weakening the steady-state review rule, then verify the final live state.

### 6. Tag and release

- Skip tagging when version semantics are unclear without invention, and report the skip precisely.

## Completion Gate

- Verify the final GitHub setting claims are backed by a fresh `python -m ceratops_gh_current_state repo-health` run.
- Verify live review protection still shows `required_approving_review_count: 1` and the intended maintainer bypass actor unless the user explicitly chose a different merge policy.
- Verify the maintainer bypass is implemented through a live pull-request-only ruleset when the platform supports it.
- Verify live external state for every touched repo, protection rule, security setting, release, package, image, CI run, code scanning result, PR state, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact directory, cache, temp path, credential or config change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.
- Ensure the local repo is clean on the default branch and tracking the remote default branch. If a squash merge or history rewrite would strand useful local work, keep one clearly named safety branch and report it.

## Output Contract

Report only:

- what was created or changed
- new repo or published artifact details when materially relevant to downstream use
- unresolved blockers or non-blocking debt
- intentionally retained branches, PRs, temp files, or side effects with reasons
- anything important not verified
- exact credential step or paid requirement if blocked

## Example Invocation

`Use $ceratops-gh-repo-create-and-publish for this project. Create or harden the GitHub repo, then publish the right public artifact and prove live GitHub settings with the bundled checks before closing.`
