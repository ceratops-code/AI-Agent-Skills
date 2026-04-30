# Ceratops GH Skill Best-Practice Baseline

Use this repo-root file as the bounded audit map for `ceratops-gh-skills-standards-update`. It is a checklist, not a frozen truth source. When the next decision matters, confirm the current state from the evidence sources required by the skill.

## 1. GitHub Repo Contract

- Verify the repo's public contract: purpose, visibility, default branch, description, topics, homepage, and release posture when those details are user-facing.
- Verify the merge surface: allowed merge methods, auto-merge, delete-branch-on-merge, update-branch behavior, and whether rulesets or classic branch protection are the active enforcement layer.
- Verify the protected-branch or ruleset posture that the Ceratops GH skills claim to expect: required checks, strict checks, required reviews, stale-review dismissal, conversation resolution, bypass scope, admin enforcement, force-push bans, and deletion bans.
- Verify Actions posture when relevant: permissions model, SHA pinning or equivalent immutable-action policy, and any live setting that the GH helper runtime reports.
- Verify security and moderation posture for public repos when relevant: code scanning or equivalent custom setup, secret scanning, push protection, Dependabot security updates, private vulnerability reporting or an explicit reporting path, and community or moderation surfaces that the skill family claims to audit.
- Prefer GitHub code security configurations for org-wide defaults and existing-repo attachment when the task is about org-wide or new-repo security posture; classify missing `admin:org` or security-manager access separately from paid-product blockers.
- Verify the no-extra-cost dependency security baseline for every non-archived repo when available: dependency graph, Dependabot alerts, Dependabot security updates, and open Dependabot alert or PR queues.
- For private or internal repos on plans without GitHub Code Security or GitHub Secret Protection, classify code scanning, secret scanning, push protection, dependency review enforcement, generic secret detection, non-provider patterns, and validity checks as paid requirements rather than missing no-cost settings.
- Surface optional paid or churn-prone settings when relevant: dependency graph automatic dependency submission, secret scanning non-provider patterns, validity checks, extended metadata, generic secret detection, delegated bypass or dismissal, dependency review enforcement, and grouped Dependabot security updates.
- Do not silently enable grouped Dependabot security updates or automatic dependency submission when doing so could close and reopen existing PRs, add workflow runs, consume Actions minutes, require private registry access, or create noisy low-value checks.

## 2. Repo Contents And Community Files

- Verify whether the repo should contain `README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `.github/CODEOWNERS`, issue forms or templates, pull request template, `CODE_OF_CONDUCT.md`, changelog or release notes, support routing, and examples or install docs.
- Treat required-file expectations as contextual. Public open-source repos usually need more community files than internal or one-off repos.
- When the GH skill family tells another agent that a repo "should contain" a file, verify that claim against current GitHub and ecosystem expectations before preserving it.

## 3. Workflow, Release, And Supply-Chain Hardening

- Verify CI, lint, test, and release workflow expectations only where the GH skill family makes claims about them.
- Verify mutable external action refs, workflow permissions, required checks, release tagging, and post-publish verification guidance where relevant.
- Keep non-local GitHub Actions pinned to verified full SHAs with same-line version comments whenever the workflow hardening policy applies.
- Prefer trusted publishing, OIDC, provenance or attestation verification, and post-publish consumer checks only for the real artifact surfaces a skill claims to publish.
- Treat public artifact release requirements, registry identity, tag policy, changelog source, and restore or rollback state as part of shipping only when the repo actually publishes that artifact.
- Treat artifact attestations, provenance, SBOM, or other supply-chain extras as conditional and artifact-specific. Verify them when the selected publish workflow already emits them or the artifact contract makes provenance part of the deliverable; otherwise report them as an optional hardening path rather than a default requirement.
- When GitHub Actions artifact attestations are in scope, verify that the workflow grants only the needed permissions for attestation generation and that the published artifact can be verified with GitHub or registry-specific tooling.
- When an attestation workflow intentionally records linked-artifact metadata, verify that `artifact-metadata: write` is scoped only to the job that needs it and is not treated as required for ordinary attestation generation.

## 4. Artifact Surfaces

- Audit only the artifact surfaces that the GH skill family, repo docs, or helper claims actually touch.
- Use `ceratops-gh-repo-create-and-publish` and `ceratops-gh-ship-change` as the scope boundary for artifact types. That boundary includes packages, images, modules, binaries, and other public artifacts, including Docker or OCI registries, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, and another relevant registry when the publish or ship skills would treat it as a real deliverable.
- If the repo explicitly publishes no artifacts, verify that the docs and skill wording stay consistent with that no-artifact posture.

### Docker Or OCI Images

- Verify whether the repo publishes Docker or OCI images at all, and where.
- When Docker or OCI publishing is in scope, verify Dockerfile and publish guidance around `.dockerignore`, build context scope, base-image pinning strategy, non-root execution when practical, multi-stage builds when useful, exposed ports or health checks only when appropriate, documented image tags, local build or smoke-check expectations, and provenance or SBOM attestations emitted by the selected publish flow.
- When Docker or OCI provenance is emitted, verify that build arguments are not being misused for secrets that would leak through attestation metadata.
- Use current official Docker, OCI, registry, and GitHub Actions docs for the exact policy questions that matter. Do not cargo-cult every hardening option into a universal default.

### PyPI Or Python Packages

- Verify whether the repo publishes to PyPI at all, and which package metadata files own that contract.
- When PyPI publishing is in scope, verify `pyproject.toml` metadata, README or long-description expectations, `license` or `license-files` metadata, `requires-python`, build backend, sdist and wheel expectations, Trusted Publishing or another short-lived identity path when supported, version verification, smoke-install guidance, and attestation or provenance behavior from the selected publisher.
- Use current official PyPI and Python packaging docs for publish and verification expectations. Do not preserve stale `setup.py`, twine-only, or long-lived-token guidance when the current official path has moved.

### npm Packages

- Verify whether the repo publishes to npm at all, and which package metadata files own that contract.
- When npm publishing is in scope, verify `package.json` metadata, package contents, lockfile and build commands, public or scoped access, version and dist-tag expectations, Trusted Publishing or another short-lived identity path when supported, current npm and Node prerequisites for trusted publishing, live package-version verification, consumer smoke-install guidance, and provenance behavior from the selected publisher.
- Use current official npm docs and live npm registry behavior for publish and verification expectations. Do not preserve stale long-lived-token guidance when npm Trusted Publishing is supported for the real publish environment.

### Other Registries Or Public Artifacts

- When another registry or public artifact type is in scope, use the exact artifact contract from the repo and the corresponding publish or ship workflow instead of forcing Docker, PyPI, or npm assumptions onto it.
- Verify the ecosystem-standard manifest, metadata, build, release, publish, and smoke-check expectations for the real deliverable, such as npm packages, Maven artifacts, NuGet packages, crates.io crates, RubyGems gems, PowerShell Gallery modules, GitHub Packages outputs, standalone binaries, or another supported public artifact.
- Prefer current official ecosystem docs and live registry behavior for the touched artifact type. Keep the standards audit anchored to artifact types the Ceratops publish or ship skills actually support.

## 5. Current Official Sources To Recheck

- GitHub REST code security configurations docs.
- GitHub Dependabot alerts, security updates, grouped security updates, and dependency graph docs.
- GitHub code scanning, dependency review, automatic dependency submission, secret scanning, and GitHub Code Security or Secret Protection availability docs.
- GitHub repository rulesets, branch protection, Actions policy, artifact attestation, release, and community profile docs wherever those surfaces affect a standards decision.
- Current registry docs for each touched artifact surface, such as PyPI, npm, Docker, GHCR, OCI, or another supported registry, only when that artifact surface is in scope.

## 6. Ceratops Delta Check

- After the baseline is current, inspect `skills/ceratops-gh-*`, shared section references, helper-runtime claims, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and the installed automation prompt.
- Report every proposed Ceratops skill, shared-section, checklist, helper, repo-doc, or automation-prompt change for explicit user approval before applying it.
- Separate no-extra-cost maintenance recommendations from paid, security-posture, merge-policy, review-posture, artifact-publishing, recurring-cost, or helper-runtime recommendations.

## 7. Reference Repository Use

- Use the skill-required reference repositories as standards comparators only; do not audit or repair their repo health.
- Prefer repositories that visibly exercise the standards surface under review, such as workflow hardening, release posture, community files, or artifact publishing.
- Inspect only the files, metadata, visible settings, or release artifacts needed for the standards question, and record which question each reference repository informed.
