# Ceratops Codex Skills

Reusable Ceratops skills for Codex and other `SKILL.md`-compatible agents.

## Skills

| Skill | Purpose |
| --- | --- |
| `ceratops-gh-repo-create-and-publish` | Create or production-harden a public GitHub repo and publish the right artifact target when relevant. |
| `ceratops-gh-ship-change` | Ship local repo changes through PR, CI, merge, artifact publishing when relevant, and cleanup. |
| `ceratops-gh-repo-dependency-update` | Process Dependabot, Renovate, security, and manual dependency update work recursively. |
| `ceratops-gh-repo-health-audit` | Audit and repair GitHub repo health, security posture, stale state, and publication gaps. |
| `ceratops-gh-merge-pr` | Safely merge a GitHub PR, verify checks and protection with live scripted readiness checks, clean up branches, and sync local state. |
| `ceratops-gh-skills-standards-update` | Review the GitHub health contracts against current GitHub and registry standards, then report proposed updates for explicit approval. |
| `ceratops-skill-create` | Create a new Ceratops skill, integrate it into the shared section system, and stage it into the local runtime release branch by default. |
| `ceratops-skill-update` | Update existing Ceratops skills, shared sections, runtime generation, validation flow, and related helper or doc alignment while keeping source skills delta-only. |
| `ceratops-automation-run` | Run recurring automations with shared Ceratops alert, memory, and completion policy. |
| `ceratops-task-execute-in-stages` | Drive substantial tasks stage by stage, preferring the simplest standard fix and asking before complex paths. |
| `ceratops-code-consistency-audit` | Audit merged refactors for contradictions, docs drift, comment sufficiency, stale follow-through, and merged-only edge cases. |
| `ceratops-thread-resume-manual-stop` | Resume a same-thread task from current local state after a stop, restart, or crash without rebuilding everything from scratch. |
| `ceratops-thread-full-handoff` | Create a copy-paste prompt for moving a whole task into a new thread without re-auditing the whole task. |
| `ceratops-thread-side-task-handoff` | Create a minimal copy-paste prompt for spinning a newly discovered side task into a new thread. |
| `ceratops-codex-skill-stage-release` | Merge ready skill branches into the runtime `release/*` branch, switch the runtime checkout there, and validate the staged batch locally. |
| `ceratops-gh-codex-skill-ship` | Ship a staged runtime skill batch through GitHub, then restore the runtime checkout and installed skills to clean `main`. |

## Layout

```text
assets/
  ceratops-logo-500.png
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    assets/
      ceratops-logo-500.png
templates/
  skill-sections.json
  sections/
    minimal.md
    credentials.md
    gh-current-state.md
    gh-repo-health-contract.md
    gh-artifact-contract.md
    gh-findings.md
    release-branch-runtime.md
    thread-first-step.md
contracts/
  source-docs.json
  artifacts/
    artifact-contract.json
    artifact-nondeterministic-checks.md
  github/
    github-org-contract.json
    github-repo-contract.json
    github-org-nondeterministic-checks.md
    github-repo-nondeterministic-checks.md
```

Source `SKILL.md` files are portable, delta-only skill definitions. Runtime `SKILL.md` files are generated during install by expanding the shared section assignments from `templates/skill-sections.json`.
`agents/openai.yaml` is Codex UI metadata and may be ignored by other agents.
Each Ceratops skill declares the runtime-local icon path `./assets/ceratops-logo-500.png`. The repo-root `assets/ceratops-logo-500.png` is the source copied into each skill by `scripts/install-skills.ps1`.
GitHub helper logic lives in copied scripts under `scripts/`, not in an installed Python package.
`contracts/` is the source of truth for deterministic GitHub org/repo checks, external artifact registry checks, non-deterministic review prompts, source-doc tracking, and local code-comment standards. `skills/ceratops-gh-skills-standards-update/` reviews and updates the GitHub and registry contracts when official standards change.

## Health Contracts

The health contract structure is split by the surface being checked:

- `contracts/source-docs.json` records official source documents and reference repositories used by the GitHub, repo, and registry contracts.
- `contracts/github/github-org-contract.json` defines deterministic organization settings, policy, identity, security, Dependabot, and default-logo/custom-logo checks.
- `contracts/github/github-repo-contract.json` defines deterministic repository settings, security, branch/ruleset, workflow, content, stale-state, and repo-type checks.
- `contracts/artifacts/artifact-contract.json` defines external artifact checks for PyPI, npm, DockerHub or OCI registries, GitHub Container Registry, GitHub releases, docs sites, and other package registries.
- `contracts/*/*-nondeterministic-checks.md` files capture checks that need intent judgment, prose review, manual browser confirmation, or current-doc interpretation after bundled evidence is collected.

Run deterministic checks with one bundled command per surface instead of one command per setting:

```powershell
python .\scripts\github_org_contract.py --org ORG --preset all
python .\scripts\github_repo_artifact_contract.py --repo OWNER/REPO --scope all --preset health --local-repo-path .
```

Collect review evidence for non-deterministic checks with:

```powershell
python .\scripts\github_nd_evidence.py --scope org --org ORG --json
python .\scripts\github_nd_evidence.py --scope repo --repo OWNER/REPO --local-repo-path . --json
python .\scripts\github_nd_evidence.py --scope artifact --repo OWNER/REPO --local-repo-path . --json
```

`contracts/code-comment-standards.json` is local project policy for comment sufficiency. It avoids repeated live research during code-consistency audits.

## Install For Codex

Codex discovers personal skills from:

```text
$CODEX_HOME/skills/<skill-name>/SKILL.md
```

Run one explicit bootstrap step from the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-skills.ps1
```

That bootstrap does two things explicitly:

- refreshes each skill-local Ceratops icon from the repo-root icon source
- builds managed runtime skill copies under `$CODEX_HOME/skills/`

During migration, it removes old runtime reparse-point installs for the rebuilt skills and replaces them with managed copies.

Installed Ceratops skills should be generated from the runtime checkout path. That checkout may sit on local `main` tracking `origin/main` or on a local `release/*` branch for an active unpublished batch. After the runtime checkout changes branches, rerun `scripts/install-skills.ps1` so new, renamed, or deleted managed skill folders match the active repo snapshot.
When shipping a staged batch, reuse the same `release/local` branch name locally and remotely by default. GitHub may delete the remote `release/local` after merge; the next batch simply recreates that same remote branch from the current local `release/local`.

Restart Codex after adding new skill folders if the app does not pick them up automatically.

## Install For Claude Code

Claude Code uses the same core `SKILL.md` folder format. Copy or link a skill folder into:

```text
$HOME/.claude/skills/<skill-name>/SKILL.md
```

Invoke skills directly with `/skill-name` in Claude Code. In Codex, invoke them with `$skill-name`.

## Validate

Run:

```powershell
python .\scripts\validate-skills.py
```

Run `python .\scripts\sync-skill-sections.py` before validation only when shared section source files or `templates/skill-sections.json` assignments changed. The sync command validates that source skills are delta-only; `scripts/build-runtime-skills.py` performs runtime shared-section expansion during install.
`templates/skill-sections.json` records the default maintenance-check policy so the Ceratops skill-create or update workflows can decide which checks to run without extra user instructions.
The builder composes each runtime skill's shared block from `templates/skill-sections.json` and `templates/sections/`, and each generated runtime `SKILL.md` block includes section-source comments so the origin of every shared section stays visible in the installed skill copy. The validator checks skill frontmatter, folder/name consistency, section assignments, runtime-renderability, Codex metadata, placeholder leftovers, real README skill rows, cross-skill references, maintenance-workflow targets, contract presence, stale active terminology, and high-confidence secret patterns.
Run `python .\scripts\github_pr_readiness.py --help` only when PR-readiness helper code or related skill claims changed. With working GitHub auth, use `scripts/github_org_contract.py` and `scripts/github_repo_artifact_contract.py` for deterministic GitHub and artifact contract checks.

## Releases

Releases use `vMAJOR.MINOR.PATCH` tags. See `CHANGELOG.md` for release notes.

## Artifact Publishing

This repository publishes skill source files only. It does not publish Docker images, PyPI packages, npm packages, or other runtime artifacts.
