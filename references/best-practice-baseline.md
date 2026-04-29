# Ceratops GH Skill Best-Practice Baseline

Use this file as the bounded starting checklist for `ceratops-gh-skills-standards-update`. Refresh current facts from official docs and live GitHub state before changing skill behavior.

## Repository Security

- Mandatory: Prefer GitHub code security configurations for org-wide defaults and existing-repo attachment when the task is about org-wide or new-repo security posture; classify missing `admin:org` or security-manager access separately from paid-product blockers.
- Mandatory: Verify the no-extra-cost dependency security baseline for every non-archived repo when available: dependency graph, Dependabot alerts, Dependabot security updates, and open Dependabot alert or PR queues.
- Mandatory: For public repos, verify code scanning through default setup or an equivalent custom setup, secret scanning, push protection, private vulnerability reporting or an explicit reporting path, and reported-content moderation for non-fork organization repos.
- Mandatory: For private or internal repos on plans without GitHub Code Security or GitHub Secret Protection, classify code scanning, secret scanning, push protection, dependency review enforcement, generic secret detection, non-provider patterns, and validity checks as paid requirements rather than missing no-cost settings.
- Mandatory: Surface optional paid or churn-prone settings when relevant: secret scanning non-provider patterns, validity checks, generic secret detection, delegated bypass or dismissal, dependency review enforcement, automatic dependency submission, and grouped Dependabot security updates.
- Mandatory: Do not silently enable grouped Dependabot security updates or automatic dependency submission when doing so could close and reopen existing PRs, add workflow runs, consume Actions minutes, require private registry access, or create noisy low-value checks.

## Workflow And Release

- Mandatory: Keep non-local GitHub Actions pinned to verified full SHAs with same-line version comments whenever the workflow hardening policy applies.
- Mandatory: Prefer trusted publishing, OIDC, provenance or attestation verification, and post-publish consumer checks only for the real artifact surfaces a skill claims to publish.
- Mandatory: Treat public artifact release requirements, registry identity, tag policy, changelog source, and restore or rollback state as part of shipping only when the repo actually publishes that artifact.

## Current Official Sources To Recheck

- Mandatory: GitHub REST code security configurations docs.
- Mandatory: GitHub Dependabot alerts, security updates, grouped security updates, and dependency graph docs.
- Mandatory: GitHub code scanning, dependency review, automatic dependency submission, secret scanning, and GitHub Advanced Security availability docs.
- Mandatory: Current registry docs for each touched artifact surface, such as PyPI, npm, Docker, GHCR, or OCI, only when that artifact surface is in scope.
