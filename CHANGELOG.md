# Changelog

## Unreleased

- Added staged-task, same-thread resume, handoff, and skill-shipping Ceratops skills for recurring Codex workflow management.
- Switched the Ceratops GitHub merge-capable skills to explicit `gh pr merge --admin` direct-merge guidance.
- Renamed `ceratops-gh-repo-push-to-remote` to `ceratops-gh-ship-change` to clarify that it owns the full ship-change workflow, not just remote finalization.
- Explicitly required `ceratops-gh-ship-change` to remove temporary worktrees and branches during end-of-run cleanup unless intentionally retained.
- Added a Ceratops SHA-pinning policy for GitHub Actions: publish and workflow-change runs must end on verified full SHAs, audit runs must surface missing enforcement explicitly, and repo-health now reports the live `sha_pinning_required` setting.
- Added a shared Ceratops skill-core rule to preserve existing text-file line endings unless normalization is intentional.

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
