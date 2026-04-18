# Ceratops Codex Skills

Reusable Ceratops skills for Codex and other `SKILL.md`-compatible agents.

## Skills

| Skill | Purpose |
| --- | --- |
| `ceratops-gh-repo-publish` | Create or production-harden a public GitHub repo and publish the right artifact target when relevant. |
| `ceratops-gh-repo-ship-change` | Ship local repo changes through PR, CI, merge, artifact publishing when relevant, and cleanup. |
| `ceratops-gh-repo-dependency-update` | Process Dependabot, Renovate, security, and manual dependency update work recursively. |
| `ceratops-gh-repo-health-audit` | Audit and repair GitHub repo health, security posture, stale state, and publication gaps. |
| `ceratops-gh-merge-pr` | Safely merge a GitHub PR, verify checks/protection, clean up branches, and sync local state. |

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
```

`SKILL.md` is the portable source of truth. `agents/openai.yaml` is Codex UI metadata and may be ignored by other agents.

## Install For Codex

Codex discovers personal skills from:

```text
C:\Users\<you>\.codex\skills\<skill-name>\SKILL.md
```

Recommended local development setup on Windows is to keep this repo as the source of truth and junction each skill folder into the Codex runtime folder:

```powershell
$repo = "$env:USERPROFILE\CodexProjects\codex-skills"
$runtime = "$env:USERPROFILE\.codex\skills"

foreach ($skill in Get-ChildItem "$repo\skills" -Directory) {
  $link = Join-Path $runtime $skill.Name
  if (-not (Test-Path -LiteralPath $link)) {
    New-Item -ItemType Junction -Path $link -Target $skill.FullName | Out-Null
  }
}
```

Restart Codex after adding new skill folders if the app does not pick them up automatically.

## Install For Claude Code

Claude Code uses the same core `SKILL.md` folder format. Copy or link a skill folder into:

```text
~/.claude/skills/<skill-name>/SKILL.md
```

Invoke skills directly with `/skill-name` in Claude Code. In Codex, invoke them with `$skill-name`.

## Validate

Run:

```powershell
python .\scripts\validate-skills.py
```

The validator checks skill frontmatter, folder/name consistency, Codex metadata, placeholder leftovers, README coverage, and high-confidence secret patterns.

## Releases

Releases use `vMAJOR.MINOR.PATCH` tags. See `CHANGELOG.md` for release notes.

## Artifact Publishing

This repository publishes skill source files only. It does not publish Docker images, PyPI packages, npm packages, or other runtime artifacts.
