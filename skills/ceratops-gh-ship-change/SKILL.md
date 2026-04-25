---
name: ceratops-gh-ship-change
description: Ship local repository changes through GitHub and any relevant artifact registry with Ceratops defaults, using scripted live repo and PR checks before merge decisions.
---

# Ceratops GH Ship Change

Take an existing published repo from local changes to a verified merged result. Publish external artifacts only when the change affects a releasable package, image, module, binary, or other public artifact. Verify machine-checkable GitHub state through the bundled helper scripts before trusting prose or stale screenshots.

<!-- CERATOPS_SHARED_SECTIONS_START -->
<!-- SECTION SOURCE: templates/sections/minimal.md -->

## Core Rules

- Everything in this section is mandatory unless explicitly marked optional or inapplicable.
- Before completion, verify the work against this `SKILL.md` and any governing files already used in the run. Re-open only files changed in this run or whose current contents remain concretely in doubt.
- Use local state, local files, installed tools, and other direct evidence first. Check current official docs or other live official sources only when the task depends on unstable external behavior and the available direct evidence still leaves a concrete task-blocking ambiguity or material conflict.
- Do not do generalized best-practice refresh, reference-repo comparison, or skill-maintenance work during routine runs.
- Do not update this `SKILL.md` during routine runs unless the user explicitly asked for skill maintenance or the current task cannot be completed safely without a narrow in-scope fix.
- Inspect local state and local auth before asking for credentials or making assumptions.
- When editing an existing text file, preserve its current line-ending convention unless intentional normalization is part of the task.
- Classify each touched artifact, external entity, and side effect as active, intentionally retained with reason, stale and removed, not applicable, or blocked.
- In user-facing answers, keep routine success reporting implicit. Omit PR metadata, commit IDs, check lists, cleanup logs, and exact local paths unless they materially change the user's next action, explain a blocker, or were explicitly requested.
- If any required item is unmet or unverifiable, report the blocker instead of claiming completion.

<!-- SECTION SOURCE: templates/sections/credentials.md -->

## Credential Handling

- Do not ask for credentials unless they are truly required after local checks.
- If credentials are truly required after local checks, report only:

1. which credential or login is missing
2. why it is needed
3. where it will be stored
4. the exact command the user should run
5. whether it goes into a local credential store, config file, keyring, CI secret, registry setting, connector, or another exact target

<!-- SECTION SOURCE: templates/sections/gh-current-state.md -->

## GH Current State

- Use the shared helper package `ceratops_gh_current_state` for bundled GitHub current-state checks when it covers the next decision.
- Use `gh`, GitHub API, and `ceratops_gh_current_state` as first-pass evidence for current GitHub state before checking official docs or `gh` help.
- Prefer current GitHub state over memory, prose summaries, or stale screenshots.
- Start with the narrowest live check that answers the next decision: bundled helper script, targeted `gh` query, or focused API call.
- Check current official GitHub docs or `gh` help only when the next decision remains concretely ambiguous after targeted live GitHub evidence, or when those sources materially conflict.
- Compare at most 1-2 strong current reference repos only for concrete ambiguous GitHub workflow, security, release, or packaging patterns that official docs and current GitHub state do not settle.
- Re-run the relevant live check after any GitHub change that could affect the specific result being relied on.

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
- For PyPI publishes, prefer Trusted Publishing or another short-lived identity path over repository-stored long-lived tokens when supported, build the intended sdist and wheel, publish the intended version, verify the live PyPI version, install that exact version from PyPI locally, and run the smoke or documented consumer check against the published artifact instead of an editable checkout.
- For PyPI publishes that emit attestations or provenance, verify the metadata through PyPI or the selected verifier instead of relying only on upload success.
- For Docker or OCI image publishes, build locally, run a smoke test, publish the intended tags or digests, verify the live registry state, and pull or consume the published image when relevant.

<!-- SECTION SOURCE: templates/sections/gh-findings.md -->

## GH Findings

- Classify only findings actually inspected in this run. Do not expand reporting to untouched queues unless they become the next actionable work or the user explicitly asked for full coverage.
- For each inspected finding, decide whether it is safe, fix low-risk items directly when in scope, and for every finding left open report its name or id, whether it is blocking, why it remains open, and the concrete work needed to clear it.
- Do not collapse retained findings into a generic healthy result.
- Re-check findings whose status may have changed because of actions taken in this run.
<!-- CERATOPS_SHARED_SECTIONS_END -->

## Script Bundle

- Repo settings check: `python -m ceratops_gh_current_state repo-health --repo OWNER/REPO`
- PR readiness check: `python -m ceratops_gh_current_state pr-readiness --pr NUMBER_OR_URL`

## Inputs To Capture

- Intended change scope, issue or PR reference, target branch, repo owner and name, and merge preference.
- Any missing inputs required by the GH artifact contract.
- Required local checks, CI checks, security gates, branch protection, release workflow, and package verification commands.
- Whether the run touches GitHub Actions workflows or repo Actions permissions, and whether the repo already enforces SHA pinning.
- Topics, CODEOWNERS, SECURITY instructions, README examples, and local consumer paths affected by the change.

Infer missing inputs from local files and live repo state before asking.

## Boundaries

- Use this skill when the repo already exists and there are actual local changes to complete, merge, and optionally release.
- If the repo is not yet published or lacks a usable remote, stop and use `$ceratops-gh-repo-create-and-publish`.
- If the task is only repo validation or stale-state cleanup with no content changes, stop and use `$ceratops-gh-repo-health-audit`.
- If only PR finalization remains, no content changes are needed, and no release or artifact publish is required after merge, stop this workflow immediately and continue with `$ceratops-gh-merge-pr`, even when this workflow created or updated the PR.

## Workflow

### 1. Inspect state and scope

- Inspect git status, diff, untracked files, remotes, current branch, upstream, open PRs, tags, releases, CI config, manifests, lockfiles, docs, generated files, and registry metadata.
- Refresh remote refs with `git fetch --prune origin` before relying on remote-tracking branch presence, cleanup status, or branch-reuse decisions.
- Prefer the same local and remote branch name by default. Do not use `local:remote` branch-name remapping unless there is a concrete benefit and the user explicitly wants that tradeoff.
- Identify whether the change is code, docs, config, dependency, release, packaging, security, CI, or generated-artifact work.
- Confirm no secrets, private data, machine-local paths, or internal-only references are being introduced.
- Reuse an existing branch or PR when appropriate instead of creating duplicates.

### 2. Research only when the next decision needs it

- Default to the narrowest evidence that answers the next shipping decision: local repo files and bundled live checks first, then touched-registry or GitHub docs only when needed.
- Check current official docs for GitHub PR, Actions, security, release behavior, and any touched registry or package-manager workflow only when the next task decision remains concretely ambiguous after local state, `gh`, GitHub API, or script output, or when those sources materially conflict.
- Compare at most 1-2 strong reference repos only for a concrete ambiguous docs, security, CI, release, or packaging question. Do not do broad GH-skill best-practice maintenance during routine shipping runs.

### 3. Prove live GitHub state with scripts

- Run the bundled repo-health script only when the run changes or explicitly verifies repo posture surfaces such as branch protection or rulesets, review policy, Actions permissions or SHA pinning, security controls, moderation or community reporting, or other repo-health claims that the final answer will rely on.
- Do not run the repo-health script for pure code, docs, tests, packaging, or artifact-publish work when those repo posture surfaces are untouched.
- Run the bundled PR-readiness script before merge or auto-merge decisions instead of relying on prose summaries of checks, reviews, or mergeability.
- Re-run the relevant script after any live GitHub change that could affect a reported repo-health or PR-readiness result.

### 4. Complete the change

- Finish in-scope code, docs, tests, generated files, and packaging metadata.
- If the run touches workflow files or GitHub Actions settings, pin every non-local action in the changed workflows to a verified full SHA with a same-line version comment and do not introduce new mutable refs.
- Add regression tests or regression checks for meaningful behavior fixes or behavior changes.
- Update README, examples, install or run commands, SECURITY, CONTRIBUTING, changelog, release notes, package metadata, topics, CODEOWNERS, CI, and artifact metadata only when the change makes them stale.

### 5. Validate locally

- Run the relevant local checks: format, lint, tests, smoke tests, build, packaging, generated-file checks, container build, or security checks.
- Execute the local-verification parts of the GH artifact contract when artifact publishing might be required.
- Fix in-scope failures instead of stopping at the first error.

### 6. PR, CI, and merge

- Create or update a branch and commit intentionally.
- Push the branch and create or update a PR with concise change and validation evidence.
- If the push or PR update leaves no remaining code, docs, CI, packaging, or generated-file edits, stop this workflow and continue with `$ceratops-gh-merge-pr` for review, CI, merge, and cleanup instead of continuing to finalization here.
- Wait for required CI, code scanning, and branch protection checks, and fix in-scope failures.
- Use the live script findings plus current GitHub state to decide whether to merge now, enable auto-merge, or stop on a blocker.
- When this skill merges the PR directly, use `gh pr merge --admin` with the allowed merge-method flag and `--delete-branch` when cleanup is intended and allowed.
- Use `gh pr merge --auto` only when GitHub should wait for remaining requirements instead of closing the PR immediately.
- Reuse fresh same-run evidence for local branch and worktree cleanup state; do not rerun removal or verification commands for branches or worktrees already known removed unless the state is uncertain, plausibly changed, or required fresh by another active instruction.
- Delete the local and remote branch when safe, remove any temporary worktree created or used for the run as soon as its branch is no longer needed, sync the local default branch, prune stale refs, and keep a safety branch or worktree only when needed with an explicit reason.

### 7. Publish artifacts when relevant

- Execute the publish and live-verification parts of the GH artifact contract.
- Re-run the repo-health script after any live GitHub setting change and the PR-readiness script immediately before the final merge action.

## Completion Gate

- Verify the merge decision is backed by a fresh `python -m ceratops_gh_current_state pr-readiness` run.
- Verify live GitHub state for the repo with `python -m ceratops_gh_current_state repo-health` when repo settings or process health were part of the run.
- Verify changed workflow files still use the intended full-SHA action refs when the run touched GitHub Actions workflows or settings.
- Verify local state: default branch, worktree, remotes, refs, generated files, artifacts, temp paths, caches, credential changes, and local consumer paths.
- Verify any temporary branch or worktree created or used for the run was removed unless intentionally retained with an explicit active-workflow reason.

## Output Contract

Report only:

- overall shipping outcome
- released or published artifact details when materially relevant to downstream use
- unresolved blockers or non-blocking debt
- intentionally retained branches, PRs, files, temp paths, or side effects with reasons
- anything important not verified
- exact credential step or paid requirement if blocked

## Example Invocation

`Use $ceratops-gh-ship-change to ship these local changes through GitHub with the bundled live checks, publish any relevant artifacts, verify them locally, and clean up state.`
