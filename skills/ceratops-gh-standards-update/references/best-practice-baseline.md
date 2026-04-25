# Best-Practice Baseline

Use this file as the bounded audit map for `ceratops-gh-standards-update`. It is a checklist, not a frozen truth source. When the next decision matters, confirm the current state from official docs, live GitHub behavior, package metadata, and registry endpoints.

## 1. GitHub Repo Contract

- Verify the repo's public contract: purpose, visibility, default branch, description, topics, homepage, and release posture when those details are user-facing.
- Verify the merge surface: allowed merge methods, auto-merge, delete-branch-on-merge, update-branch behavior, and whether rulesets or classic branch protection are the active enforcement layer.
- Verify the protected-branch or ruleset posture that the Ceratops GH skills claim to expect: required checks, strict checks, required reviews, stale-review dismissal, conversation resolution, bypass scope, admin enforcement, force-push bans, and deletion bans.
- Verify Actions posture when relevant: permissions model, SHA pinning or equivalent immutable-action policy, and any live setting that the GH helper runtime reports.
- Verify security and moderation posture for public repos when relevant: code scanning or equivalent, secret scanning, push protection, Dependabot security updates, private vulnerability reporting, and community or moderation surfaces that the skill family claims to audit.

## 2. Repo Contents And Community Files

- Verify whether the repo should contain `README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `.github/CODEOWNERS`, issue forms or templates, pull request template, `CODE_OF_CONDUCT.md`, changelog or release notes, support routing, and examples or install docs.
- Treat required-file expectations as contextual. Public open-source repos usually need more community files than internal or one-off repos.
- When the GH skill family tells another agent that a repo "should contain" a file, verify that claim against current GitHub and ecosystem expectations before preserving it.

## 3. Workflow, Release, And Supply-Chain Hardening

- Verify CI, lint, test, and release workflow expectations only where the GH skill family makes claims about them.
- Verify mutable external action refs, workflow permissions, required checks, release tagging, and post-publish verification guidance where relevant.
- Treat artifact attestations, provenance, SBOM, or other supply-chain extras as conditional and artifact-specific. Verify them when the selected publish workflow already emits them or the artifact contract makes provenance part of the deliverable; otherwise report them as an optional hardening path rather than a default requirement.

## 4. Artifact Surfaces

- Audit only the artifact surfaces that the GH skill family, repo docs, or helper claims actually touch.
- Use `ceratops-gh-repo-create-and-publish` and `ceratops-gh-ship-change` as the scope boundary for artifact types. That boundary includes packages, images, modules, binaries, and other public artifacts, including Docker or OCI registries, PyPI, npm, Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, and another relevant registry when the publish or ship skills would treat it as a real deliverable.
- If the repo explicitly publishes no artifacts, verify that the docs and skill wording stay consistent with that no-artifact posture.

### Docker Or OCI Images

- Verify whether the repo publishes Docker or OCI images at all, and where.
- When Docker or OCI publishing is in scope, verify Dockerfile and publish guidance around `.dockerignore`, build context scope, base-image pinning strategy, non-root execution when practical, multi-stage builds when useful, exposed ports or health checks only when appropriate, documented image tags, and local build or smoke-check expectations.
- Use current official Docker, OCI, registry, and GitHub Actions docs for the exact policy questions that matter. Do not cargo-cult every hardening option into a universal default.

### PyPI Or Python Packages

- Verify whether the repo publishes to PyPI at all, and which package metadata files own that contract.
- When PyPI publishing is in scope, verify `pyproject.toml` metadata, README or long-description expectations, license metadata, `requires-python`, build backend, sdist and wheel expectations, Trusted Publishing or another short-lived identity path when supported, version verification, smoke-install guidance, and attestation or provenance behavior from the selected publisher.
- Use current official PyPI and Python packaging docs for publish and verification expectations. Do not preserve stale `setup.py`, twine-only, or long-lived-token guidance when the current official path has moved.

### Other Registries Or Public Artifacts

- When another registry or public artifact type is in scope, use the exact artifact contract from the repo and the corresponding publish or ship workflow instead of forcing Docker or PyPI assumptions onto it.
- Verify the ecosystem-standard manifest, metadata, build, release, publish, and smoke-check expectations for the real deliverable, such as npm packages, Maven artifacts, NuGet packages, crates.io crates, RubyGems gems, PowerShell Gallery modules, GitHub Packages outputs, standalone binaries, or another supported public artifact.
- Prefer current official ecosystem docs and live registry behavior for the touched artifact type. Keep the standards audit anchored to artifact types the Ceratops publish or ship skills actually support.

## 5. Ceratops Delta Check

- After the baseline is current, inspect `skills/ceratops-gh-*`, shared section references, helper-runtime claims, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and the installed automation prompt.
- Update safe low-risk wording, file references, and helper claims directly.
- Report approval-bound changes separately when the baseline implies stricter default merge, review, security, paid-feature, or recurring-cost posture than Ceratops currently assumes.
