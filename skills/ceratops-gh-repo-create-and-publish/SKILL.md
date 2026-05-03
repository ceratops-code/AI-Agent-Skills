---
name: ceratops-gh-repo-create-and-publish
description: Create, fork, or production-harden a local software project as a public GitHub repository and publish the correct public artifact registry output with Ceratops defaults, using live scripted GitHub checks before closing.
---

# Ceratops GH Repo Create And Publish

Turn a local project into a real public GitHub repository and the right published artifact with minimal back-and-forth. Use the free path by default, prefer public visibility only after verifying the project is safe to expose, and prove machine-checkable live GitHub settings with the contract checker before closing.

## Skill-Specific Rules

- Do not prefer connector storage over normal local credential stores.

## Script Bundle

- Repo and artifact setup check: `python scripts/github_repo_artifact_contract.py --repo OWNER/REPO --scope all --preset create`
- Optional org posture check: `python scripts/github_org_contract.py --org ORG`

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
- Compare at most 1-2 strong reference repos only for a concrete ambiguous repo-structure, security, release, or packaging question. Do not do broad GitHub health contract maintenance during routine publish runs.
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

- Verify the final GitHub setting claims are backed by a fresh relevant `scripts/github_repo_artifact_contract.py` run.
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
