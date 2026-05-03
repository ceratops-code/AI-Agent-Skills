---
name: ceratops-gh-skills-standards-update
description: Review the Ceratops GitHub org, repo, and artifact health contracts against current GitHub and registry standards, then report proposed contract or checker updates for explicit approval.
---

# Ceratops GH Skills Standards Update

Review the Ceratops GitHub and artifact health contracts deliberately instead of letting normal GH task skills drift into generalized upkeep. Compare current official GitHub and registry behavior against `contracts/`, then report proposed contract or checker deltas for explicit approval before any repo changes are applied.

## Script Bundle

- Shared-sections sync: `python scripts/sync-skill-sections.py`
- Skill validation: `python scripts/validate-skills.py`
- Org contract checker: `python scripts/github_org_contract.py --help`
- Repo and artifact contract checker: `python scripts/github_repo_artifact_contract.py --help`

## References

- Source-doc registry: `contracts/source-docs.json`
- Org deterministic contract: `contracts/github/github-org-contract.json`
- Repo deterministic contract: `contracts/github/github-repo-contract.json`
- Artifact deterministic contract: `contracts/artifacts/artifact-contract.json`
- Non-deterministic review prompts: `contracts/github/*-nondeterministic-checks.md` and `contracts/artifacts/*-nondeterministic-checks.md`

## Skill-Specific Rules

- Mandatory: For this skill, the shared section rule against generalized best-practice refresh during routine runs is inapplicable. Routine runs must perform a bounded contract review across GitHub org, repo, workflow, security, and artifact-publishing surfaces already represented in `contracts/`.
- Blocking: Do not use this skill to audit or repair the health of a specific repository. Use `$ceratops-gh-repo-health-audit` for repo-health checks, and use live GitHub, registry, official-doc, or reference-repo evidence here only when needed to decide whether a contract claim is current.
- Blocking: Review current official docs, live product behavior, official API or registry metadata, and at most 2-3 current public third-party GitHub reference repositories relevant to the standards question. Use reference repositories only as pattern examples, not as health-audit targets, and separate no-extra-cost defaults from paid GitHub Code Security or Secret Protection features.
- Mandatory: Treat artifact surfaces as in scope only when `contracts/artifacts/artifact-contract.json`, `ceratops-gh-repo-create-and-publish`, or `ceratops-gh-ship-change` claims to cover them.
- Blocking: Keep durable standards in the contracts and `contracts/source-docs.json`; do not recreate a separate standards checklist file.

## Inputs To Capture

- Whether the run is routine automation upkeep or an explicit user-requested contract refresh.
- Blocking: Current target scope inside `AI-Agent-Skills`: `contracts/`, `scripts/github_org_contract.py`, `scripts/github_repo_artifact_contract.py`, `scripts/github_nd_evidence.py`, `scripts/validate-skills.py`, `templates/sections/gh-repo-health-contract.md`, `templates/sections/gh-artifact-contract.md`, and repo docs that describe the contract structure.
- Which contract surfaces are actually in scope: GitHub org settings, repo-content expectations, repo-settings concepts, workflow hardening, release posture, artifact types supported by `ceratops-gh-repo-create-and-publish` or `ceratops-gh-ship-change`, or a documented no-artifact posture.
- The reference repositories used for standards comparison and which specific standards question each one informed.
- Which proposed changes require explicit approval and which findings require no repo change.
- Whether the current task should only stage updates into the active local `release/*` batch or also ship them through GitHub now.

Infer missing inputs from local repo state, installed skill state, live GitHub evidence, and the active automation prompt before asking.

## Boundaries

- Use this skill when the work is to refresh the Ceratops GitHub health contracts against current GitHub repository-management, settings, workflow, release, or artifact-publishing best practices.
- If the task is normal repo shipping, PR handling, dependency updates, or repo-health work rather than GitHub health contract upkeep, stop and use the matching `ceratops-gh-*` task skill.
- If the work is only shipping already-prepared skill changes with no further upkeep analysis, stop and use `$ceratops-gh-codex-skill-ship`.
- If the requested change would widen contract scope beyond the supported GH health surfaces, change default GitHub policy, change merge or review posture, change security posture, add mandatory paid features, or materially alter checker behavior, report the recommendation as approval-required and do not apply it without explicit approval.

## Workflow

### 1. Inspect local contract state

- Mandatory: Inspect current repo branch, worktree state, `contracts/`, the contract checker scripts, contract shared sections, repo docs, and the installed automation prompt when this run came from automation.
- Check GitHub auth, local git auth, and installed tooling before asking for credentials.
- Classify current differences as stale local dirt, proposed in-scope change, approval-required change, or not applicable.

### 2. Refresh current source evidence

- Blocking: Read `contracts/source-docs.json` and the affected contract files at the start of the audit and use them as the bounded checklist for the next evidence-gathering steps.
- Use local files, `gh`, GitHub API, `gh` help, package metadata, release metadata, and registry endpoints as the first-pass evidence for the GitHub or artifact behavior that the contracts encode.
- Check current official GitHub docs for repository-management settings, workflow policy, rulesets, actions, security, release behavior, and repository-content expectations wherever the next contract decision depends on them.
- Check current official Docker, GHCR, PyPI, or Python packaging docs only for artifact surfaces that are actually in scope.
### 3. Audit the contracts

- Blocking: Review `contracts/`, the checker scripts, and the contract shared sections only where a contract claim depends on them.
- Look for duplicate guidance, contradictory defaults, stale GitHub setting names, stale required-file assumptions, stale repository-health expectations, stale workflow hardening guidance, stale artifact-publishing guidance, partial follow-through, or logic that belongs in a contract rather than prose.
- Keep repo docs aligned when stale: `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.

### 4. Prepare approval request

- Prepare exact proposed contract or checker updates that align behavior with current official GitHub or registry terms.
- Prepare exact proposed file-reference updates when standard repo files, GitHub settings, workflow surfaces, or artifact-publish expectations were added, removed, or renamed.
- Prepare exact proposed low-risk deduplication or refactoring inside the contracts that preserves behavior and clarifies ownership between deterministic JSON, non-deterministic review prompts, shared sections, and checker scripts.
- Prepare exact proposed source-doc registry updates when the contract needs a durable source that would otherwise bloat `SKILL.md`.
- Blocking: Do not edit the runtime checkout directly. For repo changes, use the worktree path required by the active repo-level instructions for the `AI-Agent-Skills` checkout.
- Blocking: Do not apply any proposed change until the user explicitly approves that change.

### 5. Validate and align

- If explicitly approved changes alter `templates/sections/` or `templates/skill-sections.json`, run the shared-source maintenance workflow recorded in `templates/skill-sections.json`.
- Mandatory: If explicitly approved changes stay inside skill-local text, `agents/openai.yaml`, repo docs, or `contracts/`, run the skill-local-or-metadata maintenance workflow recorded in `templates/skill-sections.json`.
- Mandatory: If explicitly approved changes alter copied helper scripts or helper-runtime claims, also run the helper-runtime maintenance workflow recorded in `templates/skill-sections.json`.
- Verify changed `SKILL.md` files, `agents/openai.yaml`, repo docs, contracts, and the installed automation prompt all point at the current source of truth.

### 6. Stage or ship and sync local runtime

- If explicitly approved updates were applied and staging was requested, use `$ceratops-codex-skill-stage-release` to merge the ready worktree branch into the runtime `release/*` branch, rerun the installer from the runtime checkout, and verify generated installed skill copies.
- Use `$ceratops-gh-codex-skill-ship` only when the current task explicitly expects GitHub publication after the standards refresh.
- If approval-required changes were found, report them without applying them.
- For routine automation runs with no repo change and no recommendation, complete without opening an inbox item.

## Completion Gate

- Verify every changed in-scope skill validates locally when explicitly approved changes were applied.
- Verify repo changes are staged into the active local `release/*` batch or shipped only when explicitly requested by the current task.
- Verify generated installed `ceratops-gh-*` skill copies after staging or shipping when contract payloads or GH skill behavior changed.
- Verify the automation prompt, this `SKILL.md`, and the active instruction sources remain aligned.

## Output Contract

Report only:

- applied explicitly approved contract or checker updates
- approval-required recommendations, blockers, or non-blocking debt
- intentionally retained leftovers or exceptions with reasons
- anything important not verified

For routine automation runs with no repo change and no recommendation, do not open an inbox item.

## Example Invocation

`Use $ceratops-gh-skills-standards-update to review the GitHub health contracts against current GitHub and registry standards, then report proposed contract or checker updates for explicit approval.`
