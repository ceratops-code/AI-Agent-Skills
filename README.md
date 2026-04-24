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
| `ceratops-gh-standards-update` | Audit the Ceratops GitHub skill family against current GitHub and relevant artifact best practices, then refresh safe deltas. |
| `ceratops-automation-run` | Run recurring automations with shared Ceratops alert, memory, and completion policy. |
| `ceratops-task-execute-in-stages` | Drive substantial tasks stage by stage, preferring the simplest standard fix and asking before complex paths. |
| `ceratops-code-consistency-audit` | Audit merged refactors for contradictions, docs drift, stale follow-through, and merged-only edge cases. |
| `ceratops-thread-resume-manual-stop` | Resume a same-thread task from current local state after a stop, restart, or crash without rebuilding everything from scratch. |
| `ceratops-thread-full-handoff` | Create a copy-paste prompt for moving a whole task into a new thread without re-auditing the whole task. |
| `ceratops-thread-side-task-handoff` | Create a minimal copy-paste prompt for spinning a newly discovered side task into a new thread. |
| `ceratops-codex-skill-stage-release` | Merge ready skill branches into the runtime `release/*` branch, switch the runtime checkout there, and validate the staged batch locally. |
| `ceratops-gh-codex-skill-ship` | Ship a staged runtime skill batch through GitHub, then restore the runtime checkout and installed skills to clean `main`. |

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
templates/
  skill-fragments.json
  fragments/
    core-minimal.md
    core-credentials.md
    core-gh-current-state.md
    core-gh-findings.md
    core-release-branch-runtime.md
    core-thread-first-step.md
src/
  ceratops_gh_runtime/
    __main__.py
    gh_current_state.py
    gh_current_state_checks.py
```

`SKILL.md` is the portable source of truth. `agents/openai.yaml` is Codex UI metadata and may be ignored by other agents.
`src/ceratops_gh_runtime/` is the local helper package used by the Ceratops GitHub skill family.
`skills/ceratops-gh-standards-update/` is the source of truth for deliberate GH-family best-practice audits and for the recurring automation that invokes them.

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

- installs the local GH helper package from this checkout with `python -m pip install --editable .`
- junctions each skill folder into `$CODEX_HOME/skills/`

Installed Ceratops skills should keep pointing at the runtime checkout path. That checkout may sit on local `main` tracking `origin/main` or on a local `release/*` branch for an active unpublished batch. After the runtime checkout changes branches, rerun `scripts/install-skills.ps1` so new, renamed, or deleted skill junctions and the editable helper package match the active repo snapshot.
When shipping a staged batch, reuse the same `release/local` branch name locally and remotely by default. GitHub may delete the remote `release/local` after merge; the next batch simply recreates that same remote branch from the current local `release/local`.

Restart Codex after adding new skill folders if the app does not pick them up automatically.

## Install For Claude Code

Claude Code uses the same core `SKILL.md` folder format. Copy or link a skill folder into:

```text
$HOME/.claude/skills/<skill-name>/SKILL.md
```

If you plan to use the Ceratops GitHub skill family outside Codex, also install the local GH helper package from the repo checkout:

```powershell
python -m pip install --editable .
```

Invoke skills directly with `/skill-name` in Claude Code. In Codex, invoke them with `$skill-name`.

## Validate

Run:

```powershell
python -m pip install .
python .\scripts\sync-skill-core.py --check
python .\scripts\validate-skills.py
python -m ceratops_gh_runtime --help
```

The sync check composes each skill's shared block from `templates/skill-fragments.json` and `templates/fragments/`, and each generated `SKILL.md` block includes source comments so the origin of every shared section stays visible in the skill file itself. The validator checks skill frontmatter, folder/name consistency, fragment assignments, generated-block drift, Codex metadata, placeholder leftovers, README coverage, and high-confidence secret patterns.
The GH helper package smoke test confirms the packaged runtime entrypoint is importable. With working GitHub auth, you can also run `python -m ceratops_gh_runtime repo-health --repo ceratops-code/codex-skills`.

## Releases

Releases use `vMAJOR.MINOR.PATCH` tags. See `CHANGELOG.md` for release notes.

## Artifact Publishing

This repository publishes skill source files only. It does not publish Docker images, the local GH helper package to PyPI, npm packages, or other runtime artifacts.
