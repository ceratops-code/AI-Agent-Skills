---
name: ceratops-gh-repo-create-and-publish
description: Create, fork, or production-harden a local software project as a public GitHub repository and publish the correct public artifact registry output with Ceratops defaults, using live scripted GitHub checks before closing.
---

# Ceratops GH Repo Create And Publish

Turn a local project into a real public GitHub repository and the right published artifact with minimal back-and-forth. Use the free path by default, prefer public visibility only after verifying the project is safe to expose, and prove machine-checkable live GitHub settings with the bundled helper scripts before closing.

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

## Script Bundle

- Shared helper path relative to this skill: `..\ceratops-gh-runtime\scripts\gh_live_checks.py`
- Repo settings check: `python <resolved-helper-path> repo-health --repo OWNER/REPO`

## Inputs To Capture

- GitHub owner or org. Prefer `ceratops-code` only when user or existing org context explicitly indicates Ceratops ownership and access is available at no extra cost.
- Repo name, default branch, visibility, branch naming, and whether the repo should remain a fork.
- Maintainer merge policy: by Ceratops default, require 1 approving review on the default branch and add a pull-request-only bypass for the authenticated maintainer role or account so the owner can still self-ship; only choose a different review policy when the user explicitly asks for it.
- Actions policy: by Ceratops default, pin every non-local action to a full commit SHA with a same-line release comment and enable the repo-level SHA-pinning setting once the workflows are compliant; only keep a weaker posture when the user explicitly chooses it.
- Package or image identity for the real deliverable: Docker, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or another relevant registry.
- Version source, release policy, tag style, changelog or release-note source, and first-release expectations.
- License intent, topics, CODEOWNERS owners, support route, and security reporting path.
- Local consumers of the project path such as shortcuts, automation configs, services, tests, docs, generated runtime paths, or Docker MCP overrides.

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

### 2. Research and decide

- Check current official docs for GitHub community health, moderation, Actions, branch protection, code scanning, Dependabot, secret scanning, private vulnerability reporting, releases, and the selected registry or packaging ecosystem.
- Compare 2-3 strong reference repos only when that will catch relevant missing repo structure, security, release, or packaging expectations for this project type.
- Select the actual distribution target from the project type instead of forcing Docker everywhere.
- Do not choose paid features unless they are already available at no extra cost.

### 3. Make the repo publishable

- Add or update only the relevant repo files and workflows for the project type.
- In repo-owned workflows, pin every non-local action to a full commit SHA and keep the intended release tag or version on the same line in a comment so Dependabot can keep updating it.
- For first-time public repos, add the standard public-repo community files unless a stronger project-specific alternative already exists: `README`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, and at least one issue or pull-request intake template.
- Replace internal, misleading, or broken defaults before publication.
- Add ecosystem-standard manifests and metadata only when relevant to the actual project type.
- Prefer a real private reporting path for vulnerabilities and enable no-cost security controls when available and relevant.

### 4. Configure GitHub and prove the result

- Create or fork the GitHub repo, preserve upstream linkage when needed, push the repo, and verify the live endpoint.
- Set precise topics. Keep `CODEOWNERS` minimal and accurate.
- Turn off unused live features such as wiki or projects when the repo does not actually use them.
- Configure default-branch protection with real required checks, strict status checks, PR flow, `required_approving_review_count: 1`, stale review dismissal, conversation resolution, admin enforcement, no force pushes, and no deletions when available at no extra cost.
- When the host supports repository rulesets, implement the maintainer exception as a pull-request-only ruleset bypass for the authenticated maintainer role or account instead of relying only on classic branch-protection bypass allowances.
- Enable `sha_pinning_required` once the repo workflows are compliant. Treat an unpinned external action as a blocking publish hardening gap unless the user explicitly accepts the weaker tradeoff.
- Enable auto-merge and delete-branch-on-merge when compatible with the workflow.
- Run the bundled repo-health script after GitHub settings changes and before closing publish work.
- Treat the script findings as the first source of truth for settings such as `content_reports_enabled`, branch protection, strict checks, required approvals, stale review dismissal, code scanning default setup, secret scanning, push protection, Dependabot security updates, `sha_pinning_required`, delete-branch-on-merge, and auto-merge.
- Verify branch protection, security controls, community health, moderation or reported-content health, and alert state from live endpoints. Do not assume repo-creation defaults already produced the intended moderation settings.
- For first-time public publish, also check the live community profile and do not close while the remaining gap is a safe standard-file addition you can still make directly.

### 5. Validate and publish

- Run the relevant local validation, ensure the latest relevant CI and code-scanning runs on the default branch are green, and publish the real external artifact only when the project actually has one.
- Verify live GitHub, release, and registry endpoints instead of trusting only local CLI success.
- If a single-maintainer fixture or sandbox repo needs one last hardening PR and GitHub self-approval rules would otherwise deadlock the run, merge that PR with `gh pr merge --admin` using the allowed method instead of weakening the steady-state review rule, then verify the final live state.

### 6. Tag and release

- Create and push a release tag only when the repo is publishable and the version source is clear.
- Prefer existing version metadata from manifests, release config, changelog, or tag series.
- Skip tagging when version semantics are unclear without invention, and report the skip precisely.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists. Do not prefer connector storage over normal local credential stores.

## Completion Gate

- Verify the final GitHub setting claims are backed by a fresh `python <resolved-helper-path> repo-health` run.
- Verify live review protection still shows `required_approving_review_count: 1` and the intended maintainer bypass actor unless the user explicitly chose a different merge policy.
- Verify the maintainer bypass is implemented through a live pull-request-only ruleset when the platform supports it.
- Verify live Actions permissions still show `sha_pinning_required: true` whenever the repo uses external actions and the user did not explicitly choose a weaker policy.
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
