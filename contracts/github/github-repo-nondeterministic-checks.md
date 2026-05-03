# GitHub Repo Health Non-Deterministic Checks

This file complements `github-repo-contract.json`. The JSON contains machine-checkable repository health checks; this file contains review checks that require judgment, current-doc interpretation, web UI confirmation, or artifact-specific evidence.

## Evidence Bundle

Use one bundled evidence command for the repo ND checks instead of running a command per check:

```powershell
python scripts/github_nd_evidence.py --scope repo --repo OWNER/REPO --local-repo-path PATH --json
```

The report maps each ND check ID to evidence keys and includes the bundled GitHub endpoint data, local scan summary, detected repo types, registry metadata discovered for artifact signals, and deterministic repo finding counts.

## Review Result Values

- `pass`: reviewer found the intent satisfied and recorded evidence.
- `fail`: reviewer found a concrete mismatch.
- `approved_drift`: mismatch is allowed by the contract's approved drift profile.
- `blocked`: review needs unavailable permission, paid feature, missing artifact access, or missing product decision.
- `not_applicable`: repository type or source line does not apply.

## Non-Deterministic Check Definitions

| ID | Applies when | Review required |
| --- | --- | --- |
| `ND.repo.public-contract-accuracy` | Non-archived repos, especially public repos | Confirm the repository purpose, description, README, topics, homepage, support route, and visible release posture are accurate, current, and not misleading. |
| `ND.repo.release-posture-fit` | Repos with releases, tags, changelog, or published artifacts | Confirm the release policy, tag style, changelog or release-note source, rollback or restore expectations, and user-facing release text match the real project. |
| `ND.repo.merge-branch-policy-fit` | Non-archived, non-fork repos | Confirm required checks match real CI, required review count is appropriate, bypass/admin exceptions are deliberately approved, and private-plan branch protection gaps are classified rather than hidden. |
| `ND.actions.workflow-intent-and-pin-verification` | Repos with `.github/workflows/*` | Confirm every workflow still has a valid purpose, release workflows match artifact surfaces, full-SHA action comments point to the intended release, and reusable workflow tag refs are deliberate. |
| `ND.security.reporting-and-paid-surface-fit` | Security settings, public repos, private repos with paid-feature responses | Confirm `SECURITY.md` or private vulnerability reporting gives a usable route, paid security controls are classified correctly, and churn-prone controls are not enabled without explicit approval. |
| `ND.security.dependabot-policy-fit` | Package manifests or `.github/dependabot.yml` are present | Confirm detected ecosystems, grouping, open-PR limits, private registries, labels, and update cadence fit the repo instead of only being syntactically present. |
| `ND.content.community-file-quality` | Repos where community or intake files are expected | Confirm README, license, security policy, contributing guide, code of conduct, issue forms, PR templates, examples, and install docs contain repo-specific usable content rather than placeholders. |
| `ND.content.support-routing-quality` | Repos with homepage, support links, discussions, issues, or `SUPPORT.md` | Confirm support routing sends users to an active channel and does not conflict with issue templates or security reporting. |
| `ND.artifact.real-deliverable-scope` | Any repo with package, image, module, binary, release asset, docs publish, Pages publish, or registry signals | Confirm the real deliverable surface and registry target instead of assuming Docker, PyPI, npm, or no artifact from file presence alone. |
| `ND.artifact.no-artifact-consistency` | Repos classified as `no_artifact` | Confirm README, workflows, skills, release notes, tags, and docs do not imply an unsupported artifact. |
| `ND.artifact.docker-policy-fit` | Docker or OCI image repos | Confirm Dockerfile and workflow choices are appropriate: build context, base-image pinning strategy, non-root execution practicality, multi-stage use, ports or health checks, image tags, local smoke checks, and publish target. |
| `ND.artifact.python-package-policy-fit` | Python package or PyPI repos | Confirm `pyproject.toml` owns metadata, long description renders from the README when used, license metadata is current, trusted publishing is feasible for the runner, and sdist/wheel install smoke checks are meaningful. |
| `ND.artifact.npm-package-policy-fit` | npm package repos | Confirm package contents, access mode, scope, dist-tag policy, Node/npm trusted-publishing prerequisites, provenance behavior, and consumer smoke-install guidance. |
| `ND.artifact.other-registry-policy-fit` | Maven, NuGet, crates.io, RubyGems, PowerShell Gallery, GitHub Packages, binary, or other artifact repos | Confirm the ecosystem-specific manifest, metadata, build, publish, versioning, verification, and smoke-check expectations for the actual deliverable. |
| `ND.artifact.provenance-verification` | Workflows that emit provenance, SBOMs, or GitHub artifact attestations | Confirm the published artifact can be verified with GitHub or registry-specific tooling and that attestation metadata does not expose secrets through build arguments. |
| `ND.stale-state.intent-classification` | Open PRs, extra branches, tags, releases, generated files, local references, old automation references, alerts, or maturity/process findings are present | Confirm each item is active, intentionally retained, approved drift, stale, or blocked before removal or repair. |
| `ND.sources.current-doc-recheck` | Exact feature availability, paid/free status, or API behavior matters and local/API evidence is ambiguous | Recheck official GitHub, Docker, PyPI, npm, OCI, or relevant registry documentation before deciding drift. |
| `ND.ceratops.skill-delta-only` | Maintaining Ceratops skills, helpers, docs, or automations | This is not a target-repo health check; use it only to record proposed skill-family changes for explicit approval. |
| `ND.reference-repo.comparator-only` | A reference repository is consulted | Record the exact standards question answered by the reference repo and do not audit or repair that reference repo. |
