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
| `ceratops-gh-best-practice-update` | Refresh the Ceratops GitHub skill family against current GitHub best practices and live GitHub behavior. |
| `ceratops-automation-run` | Run recurring automations with shared Ceratops alert, memory, and completion policy. |
| `ceratops-task-execute-in-stages` | Drive substantial tasks stage by stage, preferring the simplest standard fix and asking before complex paths. |
| `ceratops-consistency-audit` | Audit merged refactors for contradictions, docs drift, stale follow-through, and merged-only edge cases. |
| `ceratops-thread-resume-manual-stop` | Resume a same-thread task after a manual stop or pause without rebuilding everything from scratch. |
| `ceratops-thread-resume-after-restart` | Reconstruct and resume a same-thread task after Codex restarted, crashed, or was hard-stopped. |
| `ceratops-thread-full-handoff` | Create a copy-paste prompt for moving a whole task into a new thread without re-auditing the whole task. |
| `ceratops-thread-side-task-handoff` | Create a minimal copy-paste prompt for spinning a newly discovered side task into a new thread. |
| `ceratops-codex-skill-ship` | Validate, publish, and locally install changed Ceratops skills from the `codex-skills` repo. |

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
templates/
  common-core.md
  common-core-gh.md
src/
  ceratops_gh_runtime/
    __main__.py
    gh_live.py
    gh_live_checks.py
```

`SKILL.md` is the portable source of truth. `agents/openai.yaml` is Codex UI metadata and may be ignored by other agents.
`src/ceratops_gh_runtime/` is the local helper package used by the Ceratops GitHub skill family.
`skills/ceratops-gh-best-practice-update/` is the source of truth for deliberate GH-family best-practice refresh work and for the recurring automation that invokes it.

## Install For Codex

Codex discovers personal skills from:

```text
C:\Users\<you>\.codex\skills\<skill-name>\SKILL.md
```

Run one explicit bootstrap step from the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-skills.ps1
```

That bootstrap does two things explicitly:

- installs the local GH helper package from this checkout with `python -m pip install --editable .`
- junctions each skill folder into `C:\Users\<you>\.codex\skills\`

Restart Codex after adding new skill folders if the app does not pick them up automatically.

## Install For Claude Code

Claude Code uses the same core `SKILL.md` folder format. Copy or link a skill folder into:

```text
~/.claude/skills/<skill-name>/SKILL.md
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

The sync check enforces the shared Ceratops core block by composing the base core with the GH-family overlay when applicable. The validator checks skill frontmatter, folder/name consistency, Codex metadata, placeholder leftovers, README coverage, and high-confidence secret patterns.
The GH helper package smoke test confirms the packaged runtime entrypoint is importable. With working GitHub auth, you can also run `python -m ceratops_gh_runtime repo-health --repo ceratops-code/codex-skills`.

## Releases

Releases use `vMAJOR.MINOR.PATCH` tags. See `CHANGELOG.md` for release notes.

## Artifact Publishing

This repository publishes skill source files only. It does not publish Docker images, the local GH helper package to PyPI, npm packages, or other runtime artifacts.
