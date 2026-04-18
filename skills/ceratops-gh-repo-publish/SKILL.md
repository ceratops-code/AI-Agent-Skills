---
name: ceratops-gh-repo-publish
description: Create, fork, or production-harden a local software project as a public GitHub repository and publish the correct public artifact registry output with Ceratops defaults. Use when Codex must inspect a local project, create or update a GitHub repo, preserve an upstream fork when appropriate, configure topics, branch protection, CODEOWNERS, security, CI, release tags, and publish Docker Hub images, PyPI packages, npm packages, Maven artifacts, NuGet packages, crates, RubyGems, PowerShell Gallery modules, GitHub Packages, or another ecosystem registry selected from the project type.
---

# Ceratops GH Repo Publish

## Overview

Turn the current local project into a real publishable GitHub repo and the right registry artifact with minimal back-and-forth. Default to a public GitHub repo when the project can safely be public; public means anyone can view and only the owner, org members, or collaborators with permission can write.

Prefer the zero-cost path. For Ceratops-owned GitHub repos, prefer the `ceratops-code` org when local auth proves it is accessible at no extra cost; otherwise use the authenticated personal account unless the user specified a different owner.

## Hard Requirements

- Treat every bullet in `Hard Requirements`, `Inputs To Capture`, `Workflow`, `Credential Handling`, `Completion Gate`, and `Output Contract` as mandatory unless explicitly inapplicable. Do not treat examples as exhaustive.
- Before completion, re-open this `SKILL.md` and run a line-by-line closure pass over every mandatory bullet. Classify each item internally as satisfied, not applicable with reason, blocked with exact blocker, or intentionally retained side effect.
- Keep this checklist explicit and living. For every run, check current official docs and, when useful, 2-3 strong current reference repos of the same type. If runtime research reveals a durable, broadly relevant repo, packaging, security, release, or registry expectation missing from this skill, update this `SKILL.md` with the smallest general rule, validate the skill, and report the skill maintenance. Do not update for one-off preferences, speculative trends, paid-only practices, or project-specific conventions.
- Inspect local project state before assuming repo name, owner, visibility, package layout, build system, test commands, versioning, or publish target.
- Inspect local auth before asking for credentials. Check `gh`, Git Credential Manager, git remotes, credential helpers, env vars, Docker Desktop, Docker credential helpers, package-registry configs, keyrings, trusted publishing configs, existing sessions, and connected tooling available in the environment.
- If `gh` is missing, install it from the official GitHub source. If Docker Desktop is required and not running, start it. Verify whether apparent failures are sandbox or execution-context issues before calling the machine broken.
- Honor explicit user visibility requirements. If unspecified, default GitHub visibility to public only after checking the repo has no secrets, private data, internal-only code, or licensing blocker.
- Do not choose a paid plan or paid feature unless it is already available on this machine or account with no extra cost. If payment is required, stop and report the exact product or plan, why it is needed, and the price.
- Select the correct distribution target from the project type instead of forcing Docker. Use Docker Hub for containerized deliverables, PyPI for Python libraries or CLIs, npm for Node packages, Maven Central or relevant Maven registry for JVM artifacts, NuGet for .NET packages, crates.io for Rust crates, RubyGems for Ruby gems, PowerShell Gallery for reusable PowerShell modules, GitHub Packages when it is the appropriate existing target, and both or multiple registries only when the project clearly ships multiple first-class artifacts.
- Distinguish official requirements, ecosystem conventions, and repo-specific cleanup choices. Do not overstate local preference as an official requirement.
- Work autonomously until the GitHub repo and relevant registry artifact are live, or until a real blocker remains.
- Stop only for missing credentials after local checks, ambiguous ownership, destructive risk, legal or licensing ambiguity, secrets or private data that cannot safely be removed, paid requirements, or an irreversible action requiring explicit approval.

## Inputs To Capture

Find these from the user request, local repo, existing remote state, or authenticated accounts:

- GitHub owner or org, with `ceratops-code` preferred for Ceratops-owned repos when available at no extra cost.
- Repo name, default branch, branch naming conventions, and whether the repo should be a fork.
- Visibility constraints and any public-read/write-permission expectations.
- Docker image name, package name, module name, artifact coordinates, namespace, registry owner, and registry visibility.
- Version source, release policy, tag style, changelog or release-note source, and first-release expectations.
- License intent, topics, CODEOWNERS owners, security contact or private reporting path, support route, and contribution model.
- Local consumers of the project path such as shortcuts, scheduled tasks, automation configs, services, shell profiles, docs, tests, generated runtime paths, or Docker MCP overrides.

Infer the safest practical default instead of asking unless the choice is risky, materially ambiguous, destructive, or credential-bound.

## Workflow

### 1. Inspect Local State

- Inspect git status, remotes, branches, tags, ignored files, generated artifacts, and release metadata.
- Inspect manifests, lockfiles, Dockerfiles, compose files, package metadata, README, license, CI files, tests, scripts, docs, security files, contribution files, templates, generated files, and existing registry config.
- Identify build, lint, test, format, package, publish, container, and release commands from local files.
- Identify whether the project is a library, app, CLI, service, module, template, fork, patch, or internal snapshot.
- If renaming or moving anything, audit and update local consumers before closing. Verify the new path works and the old path is absent or intentionally retained.

### 2. Inspect Auth And Runtime

- Check GitHub auth with `gh auth status`, git credential config, remotes, credential helpers, env vars, and connected GitHub tooling.
- Check Docker auth with Docker config, credential helpers, Docker Desktop, and existing sessions.
- Check package-registry auth for the selected ecosystem: `.pypirc`, PyPI trusted publishing, npm config, Maven credentials, NuGet sources, Cargo credentials, RubyGems credentials, PowerShell Gallery keys, GitHub Packages tokens, keyrings, env vars, and CI OIDC settings as applicable.
- Ask for credentials only after all usable local auth paths fail.

### 3. Research Current Standards

- Check current official docs at runtime for GitHub community health, Actions, code scanning, Dependabot, secret scanning, branch protection, releases, package registry publishing, and the project's language or framework packaging expectations.
- Compare with 2-3 strong current reference repos of the same project type when it can catch relevant missing repo structure, CI/CD, security, release, packaging, maintenance, or metadata practices.
- Infer newly common files, folders, metadata, workflows, security controls, or release practices not named in this skill, then apply only those relevant to this project.
- Skip and report anything optional, outdated, unusually heavy, not relevant, paid, or unsupported by the current account.

### 4. Make The Repo Publishable

- Add or update relevant repo files: `README`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, pull request template, issue templates or forms, support/contact routing, `.gitignore`, `.dockerignore`, CI workflows, release or publish workflows, dependency update config, code scanning config, tests, regression checks, build instructions, run instructions, package install instructions, Docker publish instructions, and registry publishing instructions.
- Replace or adapt upstream, internal, misleading, broken, org-specific, or private-contact files before making the repo public.
- Add ecosystem-standard manifests and metadata only when relevant, such as `pyproject.toml`, package entry points, package data declarations, npm `package.json` metadata, Maven coordinates, NuGet metadata, Cargo metadata, gemspec, PowerShell `.psd1`, Docker labels, SBOM/provenance config, or release config.
- For public repos, ensure `SECURITY.md` has a real private reporting path or explicit private vulnerability reporting instructions. Prefer GitHub private vulnerability reporting when available at no extra cost.
- For public repos, prefer enabling Dependabot security updates, secret scanning, push protection, code scanning, and private vulnerability reporting when available at no extra cost and relevant.
- Verify GitHub community-health recognition from the live endpoint when possible.
- Verify labels referenced by issue forms or templates exist in the target repository.
- If the project fixes a bug, add a regression test or regression check.

### 5. Configure Metadata And Governance

- Set GitHub topics when possible. Use user-supplied topics exactly unless clearly wrong or redundant; otherwise infer a precise set, usually 3-8 topics. A valid user-supplied set can be `asar`, `automation`, `codex`, `electron`, `powershell`, `windows`.
- Keep `CODEOWNERS` minimal and accurate. Remove stale upstream owners, dead teams, and internal org references. Use only owners that exist and should receive ownership.
- Configure default-branch protection after checking available no-cost features. Preferred solo-maintainer baseline: required real CI checks, strict status checks, pull-request flow required, zero required approvers unless requested, stale reviews dismissed, conversation resolution required, admins enforced, no force pushes, and no deletions.
- Enable auto-merge and delete-branch-on-merge when compatible with the repo workflow and available at no extra cost.
- Verify branch protection, security controls, topics, community files, code scanning status, Dependabot security updates, secret scanning, push protection, private vulnerability reporting, and alert counts from live endpoints.
- Distinguish broken security controls from non-blocking maturity or process alerts such as Scorecard-only signals. Report retained items and the not-performed work explicitly instead of collapsing them into a generic healthy/published result.

### 6. Validate Before Publishing

- Run format, lint, test, build, package, generated-file refresh, container build, and release validation commands needed for the detected project.
- Ensure the latest relevant CI run on the default branch is green before claiming publication is complete.
- For Docker, build the image locally, run a smoke test, verify labels/tags, and ensure `.dockerignore` is appropriate.
- For Python, build wheel and sdist, validate metadata and long description, and install the built artifact locally enough to catch packaging failures before upload.
- For other ecosystems, run the official local package validation or dry-run equivalent when available and install or consume the built artifact locally enough to catch obvious failures.
- Resolve or explicitly classify setup PRs, Dependabot PRs, community-file PRs, release PRs, and generated branches created during publication. Do not leave publication-workflow PRs open unless intentionally retained and reported.

### 7. Publish GitHub And Registries

- Create or fork the GitHub repo as appropriate. Preserve upstream linkage when the project should remain a fork.
- Push the repo, configure the default branch, and verify the remote from the real GitHub endpoint.
- If the resolved owner differs from the requested or inferred owner, update remotes and docs and report the actual GitHub URL.
- Publish each relevant artifact to the correct registry with tags or versions derived from trustworthy project metadata.
- Populate Docker Hub description or overview from the README when auth supports it.
- Prefer PyPI trusted publishing when already configured or clearly appropriate at no extra cost; otherwise use existing local token-based auth. Apply analogous official publishing guidance for each selected registry.
- Verify published GitHub, release, Docker Hub, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, or other registry endpoints from live endpoints, not only CLI success.
- Add or update Docker MCP override, catalog, or profile examples only when the project is meant to replace an existing MCP server image.
- For Docker MCP replacement images, import the override when locally applicable, verify the active runtime tool annotations from the MCP client or Docker MCP CLI, and run at least one safe read-only tool call when credentials/config are available.

### 8. Tag And Release

- Create and push an initial or next release tag only when the repo is publishable and the version source is clear.
- Prefer existing version metadata from manifests, release config, changelog, or tag series.
- For public registry artifacts published from a git tag, create or verify a GitHub release for that tag unless the repo has an explicit tags-only policy; include artifact URLs, tags, and digests or package identifiers in the release notes.
- If creating a GitHub release, verify the release page, latest-release pointer, tag, target commit, release notes, and attached artifacts from the live endpoint.
- Skip release tagging when version semantics cannot be derived without invention, and report the skip precisely.

## Credential Handling

If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, or connector

Do not ask for credentials if a working local auth path exists. Do not prefer connector storage over normal local credential stores.

## Completion Gate

- Re-open this `SKILL.md` and validate the completed work line by line against every mandatory section.
- Verify live external state for every touched repo, protection rule, security setting, release, package, image, CI run, code scanning result, PR state, registry artifact, and docs endpoint.
- Verify local state for every touched repo, worktree, generated file, artifact directory, cache, temp path, credential/config change, local consumer path, shortcut, scheduled task, service, shell profile, and cleanup side effect.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked with exact blocker.
- Ensure the local repo is clean on the default branch and tracking the remote default branch. If a squash merge or history rewrite would strand a useful local commit, keep one clearly named safety branch and report it.
- If any mandatory item is unmet or unverifiable, report the blocker instead of claiming completion.

## Output Contract

Report only high-signal status:

- what was created or changed
- exact GitHub repo URL and resolved owner/org
- exact release URL and pushed tags when relevant
- exact Docker Hub image URL, tags, and digest when relevant
- exact package registry URL, package name, version, and artifact details when relevant
- local install or pull verification result
- intentionally retained branches, PRs, temp files, generated artifacts, or side effects with reasons
- remaining blocker, credential step, or paid requirement

If blocked, be precise and minimal. Do not give generic advice.

## Example Invocations

`Use $ceratops-gh-repo-publish for this project. Publish it end-to-end to public GitHub and the right public registry. Use the free path by default.`

`Use $ceratops-gh-repo-publish for this project. Owner: ceratops-code. Topics: asar, automation, codex, electron, powershell, windows.`

`Use $ceratops-gh-repo-publish for this project. It is a Python library, so publish it to GitHub and PyPI.`
