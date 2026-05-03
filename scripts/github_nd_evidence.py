#!/usr/bin/env python3
"""Collect bundled evidence for non-deterministic GitHub health checks.

The Markdown ND contracts ask a reviewer to make judgment calls. This helper
keeps that review cheap and repeatable by collecting one evidence bundle per
scope (org, repo, or artifact) and mapping each ND check ID to the evidence keys
it should inspect. It does not decide intent-quality checks by itself.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
from typing import Any


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
# The evidence script shares the contract fetching, local scanning, classifier,
# and registry helpers with the deterministic checker. Importing from the script
# directory keeps the command usable from any current working directory.
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import github_repo_artifact_contract as core  # noqa: E402


def compact_api(result: core.ApiResult) -> dict[str, Any]:
    """Drop raw stdout/stderr so evidence JSON stays compact and readable."""
    return {
        "ok": result.ok,
        "method": result.method,
        "endpoint": result.endpoint,
        "status": result.status,
        "message": result.message,
        "data": result.data,
    }


def build_org_params(args: argparse.Namespace, contract: dict[str, Any]) -> dict[str, Any]:
    """Build org-scope parameters from contract defaults plus CLI overrides."""
    if not args.org:
        raise SystemExit("--org is required for --scope org")
    params: dict[str, Any] = {"org_login": args.org}
    for key, spec in contract.get("parameters", {}).items():
        if "default" in spec and key not in params:
            params[key] = spec["default"]
    for item in args.param or []:
        key, value = parse_param(item)
        params[key] = value
    return params


def parse_param(item: str) -> tuple[str, Any]:
    """Parse `--param KEY=VALUE`, accepting JSON values where possible."""
    if "=" not in item:
        raise SystemExit(f"--param must be KEY=VALUE, got {item!r}")
    key, raw = item.split("=", 1)
    try:
        return key, json.loads(raw)
    except json.JSONDecodeError:
        return key, raw


def org_evidence(args: argparse.Namespace) -> dict[str, Any]:
    """Fetch org contract endpoints and group them by ND org check ID."""
    contract = core.load_json(args.org_contract)
    params = build_org_params(args, contract)
    fetched = core.fetch_contract_requests(contract, params)
    endpoints = {result.endpoint: compact_api(result) for result in fetched.values()}
    nd_checks = {
        "ND.org.identity-screen-parity": [
            f"/orgs/{params['org_login']}"
        ],
        "ND.org.logo-visual-confirmation": [
            f"/orgs/{params['org_login']}"
        ],
        "ND.org.member-role-intent": [
            f"/orgs/{params['org_login']}/members",
            f"/orgs/{params['org_login']}/outside_collaborators",
            f"/orgs/{params['org_login']}/invitations",
            f"/orgs/{params['org_login']}/failed_invitations",
            f"/orgs/{params['org_login']}/organization-roles",
            f"/orgs/{params['org_login']}/custom-repository-roles",
            f"/orgs/{params['org_login']}/security-managers",
        ],
        "ND.org.team-purpose-and-permission-fit": [
            f"/orgs/{params['org_login']}/teams"
        ],
        "ND.org.webhook-and-integration-intent": [
            f"/orgs/{params['org_login']}/hooks",
            f"/orgs/{params['org_login']}/actions/secrets",
            f"/orgs/{params['org_login']}/actions/variables",
            f"/orgs/{params['org_login']}/dependabot/secrets",
            f"/orgs/{params['org_login']}/private-registries",
        ],
        "ND.org.actions-policy-fit": [
            f"/orgs/{params['org_login']}/actions/permissions",
            f"/orgs/{params['org_login']}/actions/permissions/workflow",
            f"/orgs/{params['org_login']}/actions/runner-groups",
            f"/orgs/{params['org_login']}/actions/runners",
            f"/orgs/{params['org_login']}/actions/oidc/customization/sub",
        ],
        "ND.org.security-configuration-intent": [
            f"/orgs/{params['org_login']}/code-security/configurations",
            f"/orgs/{params['org_login']}/code-security/configurations/defaults",
            f"/orgs/{params['org_login']}/security-managers",
        ],
        "ND.org.dependabot-private-registry-fit": [
            f"/orgs/{params['org_login']}/dependabot/repository-access",
            f"/orgs/{params['org_login']}/dependabot/secrets",
            f"/orgs/{params['org_login']}/private-registries",
        ],
        "ND.org.dependabot-queue-fit": [
            f"/orgs/{params['org_login']}/dependabot/alerts?state=open&per_page=100",
            f"/search/issues?q=org:{params['org_login']}+is:pr+is:open+author:app/dependabot&per_page=100",
        ],
        "ND.org.custom-property-schema-fit": [
            f"/orgs/{params['org_login']}/properties/schema"
        ],
        "ND.org.moderation-and-community-fit": [
            f"/orgs/{params['org_login']}/blocks",
            f"/orgs/{params['org_login']}/interaction-limits",
            f"/orgs/{params['org_login']}/issue-types",
            f"/orgs/{params['org_login']}/issue-fields",
            f"/orgs/{params['org_login']}/announcement",
        ],
        "ND.org.ruleset-and-token-request-fit": [
            f"/orgs/{params['org_login']}/rulesets",
            f"/orgs/{params['org_login']}/personal-access-token-requests",
        ],
        "ND.org.paid-feature-classification": [
            "*failed_or_plan_limited_endpoints"
        ],
        "ND.org.source-doc-recheck": [
            "source-docs.json"
        ],
    }
    return {
        "scope": "org",
        "org": params["org_login"],
        "contract": os.path.abspath(args.org_contract),
        "evidence_command": f"python scripts/github_nd_evidence.py --scope org --org {params['org_login']} --json",
        "fetched_endpoints": endpoints,
        "failed_or_plan_limited_endpoints": [item for item in endpoints.values() if not item["ok"]],
        "nd_checks": {check_id: {"evidence_keys": keys, "evidence": [endpoints.get(key) for key in keys if key in endpoints]} for check_id, keys in nd_checks.items()},
    }


def repo_or_artifact_evidence(args: argparse.Namespace, scope: str) -> dict[str, Any]:
    """Build repo/artifact evidence once, then expose ND check mappings."""
    repo_contract = core.load_json(args.repo_contract)
    artifact_contract = core.load_json(args.artifact_contract)
    params = core.build_params(args, repo_contract, artifact_contract)
    local = core.scan_local(params.get("local_repo_path"))
    repo_findings, repo_context = core.compare_repo_contract(repo_contract, params, local)
    registries = core.registry_metadata(params, artifact_contract, local)
    endpoints = {result.endpoint: compact_api(result) for result in repo_context["fetched"].values()}
    common = {
        "repo": f"{params['owner']}/{params['repo']}",
        "repo_contract": os.path.abspath(args.repo_contract),
        "artifact_contract": os.path.abspath(args.artifact_contract),
        "types": repo_context["types"],
        "local_scan": {
            "available": local.get("available"),
            "root": local.get("root"),
            "files": local.get("files", [])[:500],
            "file_count": len(local.get("files", [])),
            "errors": local.get("errors", []),
        },
        "fetched_endpoints": endpoints,
        "registry_metadata": registries,
        "repo_findings_summary": core.summarize(repo_findings),
    }
    if scope == "repo":
        nd_checks = {
            "ND.repo.public-contract-accuracy": ["repo", "topics", "community_profile", "README"],
            "ND.repo.release-posture-fit": ["releases", "tags", "workflows", "registry_metadata"],
            "ND.repo.merge-branch-policy-fit": ["branch_protection", "rulesets", "expected_required_checks"],
            "ND.actions.workflow-intent-and-pin-verification": ["workflow_files", "actions_permissions"],
            "ND.security.reporting-and-paid-surface-fit": ["security_and_analysis", "alerts", "SECURITY.md"],
            "ND.security.dependabot-policy-fit": ["dependabot.yml", "manifests", "labels", "dependabot_pr_queue", "registry_metadata"],
            "ND.content.community-file-quality": ["community_profile", "README", "LICENSE", "CONTRIBUTING", "CODE_OF_CONDUCT"],
            "ND.content.support-routing-quality": ["homepage", "SUPPORT.md", "issue_templates", "discussions"],
            "ND.artifact.real-deliverable-scope": ["types", "manifests", "releases", "registry_metadata"],
            "ND.artifact.no-artifact-consistency": ["types", "release_assets", "workflows", "docs"],
            "ND.artifact.docker-policy-fit": ["Dockerfile", ".dockerignore", "registry_metadata.dockerhub"],
            "ND.artifact.python-package-policy-fit": ["pyproject.toml", "registry_metadata.pypi"],
            "ND.artifact.npm-package-policy-fit": ["package.json", "registry_metadata.npm"],
            "ND.artifact.other-registry-policy-fit": ["manifests", "registry_metadata"],
            "ND.artifact.provenance-verification": ["workflow_files", "attestation_permissions"],
            "ND.stale-state.intent-classification": ["pulls", "branches", "tags", "releases", "local_scan"],
            "ND.sources.current-doc-recheck": ["source-docs.json"],
            "ND.ceratops.skill-delta-only": ["not_target_repo_health"],
            "ND.reference-repo.comparator-only": ["reference_repository_question"],
        }
        evidence_command = f"python scripts/github_nd_evidence.py --scope repo --repo {params['owner']}/{params['repo']} --local-repo-path <PATH> --json"
    else:
        nd_checks = {
            "ND.artifact.scope-fit": ["types", "artifact_contracts", "task_flags"],
            "ND.artifact.real-deliverable-intent": ["types", "manifests", "workflows", "releases", "registry_metadata"],
            "ND.artifact.identity-contract-fit": ["artifact_contracts", "manifests", "registry_metadata"],
            "ND.artifact.audit-boundary": ["audit_only", "remediation_policy"],
            "ND.artifact.local-smoke-sufficiency": ["post_publish_consumer_bundle", "local_scan"],
            "ND.artifact.publish-necessity": ["merged_change_requires_release", "release_policy", "tags"],
            "ND.artifact.version-policy-fit": ["manifests", "tags", "releases", "registry_metadata"],
            "ND.artifact.live-endpoint-sufficiency": ["registry_metadata", "releases"],
            "ND.artifact.identity-path-fit": ["workflow_files", "trusted_publishing_sources"],
            "ND.artifact.provenance-fit": ["workflow_files", "registry_metadata", "attestation_permissions"],
            "ND.pypi.package-contract-quality": ["pyproject.toml", "workflow_files", "registry_metadata.pypi", "trusted_publisher_configuration"],
            "ND.npm.package-contract-quality": ["package.json", "workflow_files", "registry_metadata.npm", "trusted_publisher_configuration"],
            "ND.docker.image-contract-quality": ["Dockerfile", ".dockerignore", "registry_metadata.dockerhub"],
            "ND.maven.package-contract-quality": ["pom.xml", "build.gradle"],
            "ND.nuget.package-contract-quality": ["*.csproj", "*.nuspec"],
            "ND.crates.package-contract-quality": ["Cargo.toml"],
            "ND.rubygems.package-contract-quality": ["*.gemspec"],
            "ND.powershell.package-contract-quality": ["*.psd1"],
            "ND.github-packages.contract-quality": ["github_packages_bundle"],
            "ND.release-assets.contract-quality": ["releases", "release_assets"],
            "ND.docs-site.contract-quality": ["pages", "docs_site"],
            "ND.iac-module.contract-quality": ["*.tf", "Chart.yaml"],
            "ND.sources.current-doc-recheck": ["source-docs.json"],
        }
        evidence_command = f"python scripts/github_nd_evidence.py --scope artifact --repo {params['owner']}/{params['repo']} --local-repo-path <PATH> --json"
    common.update(
        {
            "scope": scope,
            "evidence_command": evidence_command,
            "nd_checks": {check_id: {"evidence_keys": keys} for check_id, keys in nd_checks.items()},
        }
    )
    return common


def main() -> int:
    """CLI entrypoint for org, repo, or artifact evidence collection."""
    parser = argparse.ArgumentParser(description="Collect one bundled evidence report for ND GitHub health checks.")
    parser.add_argument("--scope", choices=["org", "repo", "artifact"], required=True)
    parser.add_argument("--org")
    parser.add_argument("--repo")
    parser.add_argument("--org-contract", default=core.default_contract_path("github-org-contract.json"))
    parser.add_argument("--repo-contract", default=core.default_contract_path("github-repo-contract.json"))
    parser.add_argument("--artifact-contract", default=core.default_contract_path("artifact-contract.json"))
    parser.add_argument("--local-repo-path")
    parser.add_argument("--param", action="append", help="Additional parameter as KEY=VALUE. VALUE may be JSON.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.scope == "org":
        report = org_evidence(args)
    else:
        if not args.repo:
            raise SystemExit("--repo is required for repo and artifact scopes")
        report = repo_or_artifact_evidence(args, args.scope)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Scope: {report['scope']}")
        print(f"Evidence command: {report['evidence_command']}")
        print(f"ND checks: {len(report['nd_checks'])}")
        if "fetched_endpoints" in report:
            print(f"Fetched endpoints: {len(report['fetched_endpoints'])}")
        if report.get("registry_metadata"):
            print("Registry metadata keys:", ", ".join(k for k, v in report["registry_metadata"].items() if v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
