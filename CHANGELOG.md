# Changelog

## 0.1.1 - 2026-04-18

- Compressed repeated skill policy text into a synced shared core block.
- Added explicit skill boundaries and handoff rules between publish, ship, audit, dependency-update, and merge flows.
- Added `templates/common-core.md` and `scripts/sync-skill-core.py` so shared policy text stays consistent across skills.
- Updated validation and CI to enforce common-core sync.
- Narrowed `ceratops-code` ownership preference to explicit Ceratops context instead of acting as a universal default.

## 0.1.0 - 2026-04-18

- Initial public release of five Ceratops GitHub workflow skills.
- Added Codex metadata for each skill.
- Added repository validation, GitHub Actions CI, CodeQL workflow, Dependabot config, security policy, contribution docs, issue forms, pull request template, and CODEOWNERS.
