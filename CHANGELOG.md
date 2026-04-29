# Changelog

## Unreleased

- Clarified that `ceratops-gh-skills-standards-update` owns standards upkeep only, not per-repo health audits, and added bounded third-party GitHub reference-repo comparison to its baseline workflow.
- Added linked-artifact metadata permission checks to the GH skills standards baseline for GitHub Actions attestation workflows.
- Renamed `ceratops-gh-standards-update` to `ceratops-gh-skills-standards-update` and updated skill metadata, docs, section assignments, and references.
- Clarified that `ceratops-automation-run` is for recurring automation runs, treats delegated skill or helper prompts as task-specific deltas, and leaves automation prompt edits to control-file maintenance workflows.
- Added npm Trusted Publishing plus conditional provenance and attestation checks to the GH artifact contract and standards baseline.
- Added the missing release-branch staging helper used by `ceratops-codex-skill-stage-release`.
- Added the missing runtime-restore helper used by `ceratops-gh-codex-skill-ship`.
- Clarified that Ceratops cleanup flows should reuse fresh same-run branch and worktree removal evidence instead of rerunning cleanup checks for already-removed items.
- Made Ceratops staging and shipping cleanup remove merged task worktrees, task branches, and release branches automatically when safe, with explicit retention required for exceptions.
- Changed repo-health checks to classify plan-limited private-repo branch protection or rulesets as an informational paid requirement instead of a missing-protection failure.
- Clarified that `ceratops-skill-update` should not rerun shared-section sync after a successful sync unless the shared-source delta changed again.
- Clarified that merge-only PR finalization must hand off to `ceratops-gh-ship-change` when merging creates an immediate release or artifact-publish obligation.
- Split repeated GitHub repo-health and artifact-publish expectations into shared generated sections for the GH skill family.
- Refreshed Ceratops GitHub artifact-publishing guidance for current PyPI Trusted Publishing and attestation expectations while keeping provenance checks conditional on the real publish flow.
- Added Ceratops GitHub guidance to create or verify the `dependencies` repo label when Dependabot config explicitly uses it, and aligned dependency-update self-review admin merges with the merge skill.
- Renamed the shared build-time layer from `fragments` to `sections`, dropped the `core-` prefixes, and updated the sync or validation tooling plus generated skill markers and source comments to match.
- Split Ceratops skill authoring into `ceratops-skill-create` and `ceratops-skill-update`, added manifest-driven maintenance workflow hints, and made new-skill creation stage into the local runtime preview flow by default.
- Moved credential handling into one shared section across the skill family, removed duplicated per-skill credential sections, and trimmed GH skill sections that only restated shared rules or workflow steps.
- Split the synced shared skill core into six build-time sections with an explicit per-skill manifest, and made generated `SKILL.md` blocks show source comments for each shared section.
- Renamed the GH helper surface from `gh_live*` to `gh_current_state*`, removed the old compatibility aliases, and updated docs and packaging to point only at the current-state names.
- Widened `ceratops-gh-skills-standards-update` artifact coverage from Docker or PyPI examples to the full artifact scope used by the Ceratops publish and ship skills.
- Reframed `ceratops-gh-skills-standards-update` around a bounded best-practice audit: routine runs now start from current GitHub repo, settings, workflow, and relevant artifact guidance before deciding whether the Ceratops GH skill family needs updates.
- Replaced direct runtime-preview work with a local `release/*` runtime branch flow, added `ceratops-codex-skill-stage-release`, and rewrote `ceratops-gh-codex-skill-ship` around staging batches into the runtime checkout and restoring clean `main` after shipping.
- Renamed `ceratops-gh-best-practice-update` to `ceratops-gh-skills-standards-update`, `ceratops-consistency-audit` to `ceratops-code-consistency-audit`, and `ceratops-codex-skill-ship` to `ceratops-gh-codex-skill-ship`.
- Removed `ceratops-thread-resume-after-restart` and folded same-thread restart or crash recovery into `ceratops-thread-resume-manual-stop`.
- Added `ceratops-automation-run` so recurring automations can share one reusable policy layer for prompt or helper re-open checks, clean-run silence, no-memory defaults, and explicit conflict reporting.
- Cleaned up editable-install `egg-info` artifacts automatically during skill installs and ignored stray `*.egg-info/` folders as a backstop.
- Added staged-task, same-thread resume, split handoff, and skill-shipping Ceratops skills for recurring Codex workflow management.
- Split the old handoff flow into `ceratops-thread-full-handoff` and `ceratops-thread-side-task-handoff`, removed `ceratops-thread-resume-from-handoff`, and made both handoff skills emit copy-paste prompts instead of resumable bundles.
- Narrowed the shared external-research rule so local workflow skills do not spend credits checking current docs unless the task actually depends on unstable external guidance.
- Switched the Ceratops GitHub merge-capable skills to explicit `gh pr merge --admin` direct-merge guidance.
- Renamed `ceratops-gh-repo-push-to-remote` to `ceratops-gh-ship-change` to clarify that it owns the full ship-change workflow, not just remote finalization.
- Explicitly required `ceratops-gh-ship-change` to remove temporary worktrees and branches during end-of-run cleanup unless intentionally retained.
- Added a Ceratops SHA-pinning policy for GitHub Actions: publish and workflow-change runs must end on verified full SHAs, audit runs must surface missing enforcement explicitly, and repo-health now reports the live `sha_pinning_required` setting.
- Added a shared Ceratops skill-core rule to preserve existing text-file line endings unless normalization is intentional.
- Split the synced Ceratops core into a GH-family variant, moved routine GH-skill standards refresh into the dedicated `ceratops-gh-skills-standards-update` skill, and narrowed routine GH task-skill runs to task-specific live evidence checks.
- Refactored core sync so GH skills inherit the base Ceratops core plus a GH-only overlay, moved generic routine-run rules back into the base core, and limited live community-profile checks to audit and publish workflows.
- Collapsed the one-line GH overlay back into `templates/common-core.md`, deleted `templates/common-core-gh.md`, and simplified sync and validation to use one shared core template. This was later replaced by the sections manifest and `templates/sections/`.

## 0.1.2 - 2026-04-19

- Required all Ceratops GitHub workflow skills to report each retained security, code-scanning, maturity, or process alert with name or id, blocking status, defer reason, and concrete clearance work.
- Expanded `ceratops-gh-repo-health-audit` to perform an explicit end-to-end alert audit and forbid collapsing retained alerts into a generic healthy result.

## 0.1.1 - 2026-04-18

- Tightened publication checks across the publish, ship, audit, and merge skills.
- Added explicit retained-state reporting for Scorecard maturity gaps in publish, ship, and audit flows.
- Compressed repeated skill policy text into a synced shared core block.
- Added explicit skill boundaries and handoff rules between publish, ship, audit, dependency-update, and merge flows.
- Added `templates/common-core.md` and `scripts/sync-skill-core.py` so shared policy text stays consistent across skills.
- Updated validation and CI to enforce common-core sync.
- Narrowed `ceratops-code` ownership preference to explicit Ceratops context instead of acting as a universal default.

## 0.1.0 - 2026-04-18

- Initial public release of five Ceratops GitHub workflow skills.
- Added Codex metadata for each skill.
- Added repository validation, GitHub Actions CI, CodeQL workflow, Dependabot config, security policy, contribution docs, issue forms, pull request template, and CODEOWNERS.
