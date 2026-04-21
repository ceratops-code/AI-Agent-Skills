#!/usr/bin/env python3
"""Machine-check live GitHub repo and PR state for scripted Ceratops skills."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from dataclasses import asdict, dataclass

from .gh_live import CommandError, current_branch, detect_repo, gh_api, gh_pr_view


@dataclass(frozen=True)
class Finding:
    level: str
    check: str
    message: str
    actual: object | None = None
    expected: object | None = None


def add(
    findings: list[Finding],
    level: str,
    check: str,
    message: str,
    *,
    actual: object | None = None,
    expected: object | None = None,
) -> None:
    findings.append(Finding(level=level, check=check, message=message, actual=actual, expected=expected))


def repo_health(repo: str, cwd: pathlib.Path | None) -> tuple[dict[str, object], list[Finding]]:
    repo_info_result = gh_api(f"repos/{repo}", cwd=cwd)
    if not repo_info_result.ok or not isinstance(repo_info_result.data, dict):
        raise CommandError(f"gh api repos/{repo}: {repo_info_result.stderr}")

    repo_info = repo_info_result.data
    findings: list[Finding] = []
    default_branch = str(repo_info["default_branch"])
    owner = repo_info.get("owner", {})
    owner_type = owner.get("type")
    is_public = not bool(repo_info.get("private"))
    is_archived = bool(repo_info.get("archived"))

    actions_permissions_result = gh_api(f"repos/{repo}/actions/permissions", cwd=cwd)
    if actions_permissions_result.ok and isinstance(actions_permissions_result.data, dict):
        sha_pinning_required = actions_permissions_result.data.get("sha_pinning_required")
        if sha_pinning_required is True:
            add(findings, "PASS", "sha_pinning_required", "Actions SHA pinning is enforced in live repo settings.")
        else:
            add(
                findings,
                "WARN",
                "sha_pinning_required",
                "Actions SHA pinning is not enforced. Prefer enabling it after external workflow actions are pinned to verified full SHAs.",
                actual=sha_pinning_required,
                expected=True,
            )
    else:
        add(
            findings,
            "WARN",
            "sha_pinning_required",
            "Could not verify the live Actions SHA-pinning setting.",
            actual=actions_permissions_result.stderr or actions_permissions_result.status,
            expected="enabled or intentionally retained false",
        )

    profile_result = gh_api(f"repos/{repo}/community/profile", cwd=cwd)
    profile = profile_result.data if profile_result.ok and isinstance(profile_result.data, dict) else {}
    if is_public and owner_type == "Organization" and not is_archived:
        if not profile_result.ok:
            add(
                findings,
                "FAIL",
                "content_reports_enabled",
                "Could not read the live community profile needed to verify reported-content health.",
                actual=profile_result.stderr,
                expected="community/profile API response",
            )
        else:
            enabled = profile.get("content_reports_enabled")
            if enabled is True:
                add(findings, "PASS", "content_reports_enabled", "Reported-content moderation is enabled.")
            else:
                add(
                    findings,
                    "FAIL",
                    "content_reports_enabled",
                    "Organization-owned public repos should keep reported-content moderation enabled.",
                    actual=enabled,
                    expected=True,
                )
    else:
        add(
            findings,
            "SKIP",
            "content_reports_enabled",
            "Reported-content moderation is only enforced for non-archived organization-owned public repos.",
            actual={"owner_type": owner_type, "private": repo_info.get("private"), "archived": is_archived},
        )

    protection_result = gh_api(f"repos/{repo}/branches/{default_branch}/protection", cwd=cwd)
    if is_archived:
        add(findings, "SKIP", "branch_protection", "Archived repos do not require active branch protection.")
    elif not protection_result.ok or not isinstance(protection_result.data, dict):
        add(
            findings,
            "FAIL",
            "branch_protection",
            "The default branch is missing readable protection settings.",
            actual=protection_result.stderr or protection_result.status,
            expected=f"live protection on {default_branch}",
        )
    else:
        protection = protection_result.data
        add(findings, "PASS", "branch_protection", "Default-branch protection is present.", actual=default_branch)
        required_checks = protection.get("required_status_checks") or {}
        if required_checks.get("strict") is True:
            add(findings, "PASS", "strict_status_checks", "Strict status checks are enabled.")
        else:
            add(
                findings,
                "FAIL",
                "strict_status_checks",
                "Default-branch protection should require strict status checks.",
                actual=required_checks.get("strict"),
                expected=True,
            )
        checks = required_checks.get("checks") or []
        contexts = required_checks.get("contexts") or []
        if checks or contexts:
            add(findings, "PASS", "required_checks", "Required status checks are configured.", actual=checks or contexts)
        else:
            add(
                findings,
                "FAIL",
                "required_checks",
                "Default-branch protection should require at least one real status check.",
                actual=[],
                expected="one or more required checks",
            )
        reviews = protection.get("required_pull_request_reviews") or {}
        approvals = reviews.get("required_approving_review_count")
        if isinstance(approvals, int) and approvals >= 1:
            add(findings, "PASS", "required_approvals", "At least one PR approval is required.", actual=approvals)
        else:
            add(
                findings,
                "WARN",
                "required_approvals",
                "No approving review is required on the default branch. Keep this only when the repo policy intentionally allows maintainer-only merges.",
                actual=approvals,
                expected=">= 1",
            )
        if reviews.get("dismiss_stale_reviews") is True:
            add(findings, "PASS", "dismiss_stale_reviews", "Stale review dismissal is enabled.")
        else:
            add(
                findings,
                "FAIL",
                "dismiss_stale_reviews",
                "Stale review dismissal should stay enabled on the default branch.",
                actual=reviews.get("dismiss_stale_reviews"),
                expected=True,
            )
        if (protection.get("required_conversation_resolution") or {}).get("enabled") is True:
            add(findings, "PASS", "conversation_resolution", "Conversation resolution is required.")
        else:
            add(
                findings,
                "FAIL",
                "conversation_resolution",
                "Conversation resolution should be required on the default branch.",
                actual=(protection.get("required_conversation_resolution") or {}).get("enabled"),
                expected=True,
            )
        if (protection.get("enforce_admins") or {}).get("enabled") is True:
            add(findings, "PASS", "enforce_admins", "Admin enforcement is enabled.")
        else:
            add(
                findings,
                "FAIL",
                "enforce_admins",
                "Admin enforcement should stay enabled.",
                actual=(protection.get("enforce_admins") or {}).get("enabled"),
                expected=True,
            )
        for check_name, expected, message in (
            ("allow_force_pushes", False, "Force pushes should stay disabled."),
            ("allow_deletions", False, "Branch deletions should stay disabled."),
        ):
            value = (protection.get(check_name) or {}).get("enabled")
            if value is expected:
                add(findings, "PASS", check_name, message, actual=value)
            else:
                add(findings, "FAIL", check_name, message, actual=value, expected=expected)

    security = repo_info.get("security_and_analysis") or {}
    if is_public and not is_archived:
        code_scanning_result = gh_api(f"repos/{repo}/code-scanning/default-setup", cwd=cwd)
        if code_scanning_result.ok and isinstance(code_scanning_result.data, dict):
            state = code_scanning_result.data.get("state")
            if state == "configured":
                add(findings, "PASS", "code_scanning_default_setup", "Code scanning default setup is configured.", actual=state)
            else:
                alerts_result = gh_api(f"repos/{repo}/code-scanning/alerts?per_page=1", cwd=cwd)
                if alerts_result.ok:
                    add(
                        findings,
                        "PASS",
                        "code_scanning_default_setup",
                        "Code scanning is available through a non-default setup.",
                        actual=state,
                        expected="configured or equivalent custom setup",
                    )
                else:
                    add(
                        findings,
                        "FAIL",
                        "code_scanning_default_setup",
                        "Public repos should keep code scanning configured through default setup or an equivalent custom setup.",
                        actual=state,
                        expected="configured or equivalent custom setup",
                    )
        else:
            add(
                findings,
                "WARN",
                "code_scanning_default_setup",
                "Could not verify code scanning default setup from the live API.",
                actual=code_scanning_result.stderr or code_scanning_result.status,
                expected="configured or explicit custom setup",
            )
        for check_name, api_key, expected in (
            ("secret_scanning", "secret_scanning", "enabled"),
            ("secret_scanning_push_protection", "secret_scanning_push_protection", "enabled"),
            ("dependabot_security_updates", "dependabot_security_updates", "enabled"),
        ):
            status = (security.get(api_key) or {}).get("status")
            if status == expected:
                add(findings, "PASS", check_name, f"{check_name} is enabled.", actual=status)
            else:
                add(
                    findings,
                    "FAIL",
                    check_name,
                    f"{check_name} should be enabled for public repos.",
                    actual=status,
                    expected=expected,
                )
    else:
        add(findings, "SKIP", "security_and_analysis", "Security-setting enforcement is only applied to non-archived public repos.")

    for check_name, field_name, expectation in (
        ("allow_auto_merge", "allow_auto_merge", True),
        ("delete_branch_on_merge", "delete_branch_on_merge", True),
    ):
        actual = repo_info.get(field_name)
        if actual is expectation:
            add(findings, "PASS", check_name, f"{check_name} is enabled.", actual=actual)
        else:
            add(
                findings,
                "WARN",
                check_name,
                f"{check_name} is not enabled in live repo settings.",
                actual=actual,
                expected=expectation,
            )

    reporting_result = gh_api(f"repos/{repo}/private-vulnerability-reporting", cwd=cwd)
    if is_public and not is_archived:
        if reporting_result.ok and isinstance(reporting_result.data, dict):
            enabled = reporting_result.data.get("enabled")
            if enabled is True:
                add(findings, "PASS", "private_vulnerability_reporting", "Private vulnerability reporting is enabled.")
            else:
                add(
                    findings,
                    "WARN",
                    "private_vulnerability_reporting",
                    "Private vulnerability reporting is not enabled. Keep an explicit private reporting path if you retain this state.",
                    actual=enabled,
                    expected=True,
                )
        else:
            add(
                findings,
                "WARN",
                "private_vulnerability_reporting",
                "Could not verify private vulnerability reporting from the live API.",
                actual=reporting_result.stderr or reporting_result.status,
                expected="enabled or explicit alternate reporting path",
            )
    else:
        add(findings, "SKIP", "private_vulnerability_reporting", "Private vulnerability reporting is only checked for non-archived public repos.")

    summary = {
        "repo": repo,
        "visibility": repo_info.get("visibility"),
        "owner_type": owner_type,
        "default_branch": default_branch,
        "archived": is_archived,
    }
    return summary, findings


def status_rollup_findings(pr_data: dict[str, object], findings: list[Finding]) -> None:
    raw_rollup = pr_data.get("statusCheckRollup") or []
    if not isinstance(raw_rollup, list):
        add(findings, "WARN", "status_checks", "Could not parse status-check rollup.", actual=type(raw_rollup).__name__)
        return

    if not raw_rollup:
        add(findings, "WARN", "status_checks", "No status checks are attached to this PR.")
        return

    failed: list[str] = []
    pending: list[str] = []
    passed: list[str] = []
    for item in raw_rollup:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("context") or item.get("workflowName") or "unnamed-check")
        conclusion = item.get("conclusion")
        status = item.get("status")
        if conclusion in {"FAILURE", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED", "NEUTRAL", "STALE"}:
            failed.append(name)
        elif status in {"IN_PROGRESS", "QUEUED", "PENDING", "WAITING"} or conclusion is None:
            pending.append(name)
        else:
            passed.append(name)

    if failed:
        add(findings, "FAIL", "status_checks", "One or more status checks are failing.", actual=failed)
    elif pending:
        add(findings, "WARN", "status_checks", "Status checks are still pending.", actual=pending)
    else:
        add(findings, "PASS", "status_checks", "All visible status checks are passing.", actual=passed)


def pr_readiness(selector: str | None, cwd: pathlib.Path | None) -> tuple[dict[str, object], list[Finding]]:
    pr_data = gh_pr_view(selector, cwd=cwd)
    findings: list[Finding] = []

    if pr_data.get("state") == "OPEN":
        add(findings, "PASS", "state", "PR is open.")
    else:
        add(findings, "FAIL", "state", "PR is not open.", actual=pr_data.get("state"), expected="OPEN")

    if pr_data.get("isDraft") is True:
        add(findings, "FAIL", "draft", "PR is still marked draft.", actual=True, expected=False)
    else:
        add(findings, "PASS", "draft", "PR is ready for review.")

    mergeable = pr_data.get("mergeable")
    if mergeable == "CONFLICTING":
        add(findings, "FAIL", "mergeable", "PR has merge conflicts.", actual=mergeable)
    elif mergeable == "MERGEABLE":
        add(findings, "PASS", "mergeable", "PR is mergeable.", actual=mergeable)
    else:
        add(findings, "WARN", "mergeable", "PR mergeability needs a live re-check.", actual=mergeable)

    review_decision = pr_data.get("reviewDecision")
    if review_decision in {"APPROVED", None, ""}:
        add(findings, "PASS", "review_decision", "No blocking review decision is present.", actual=review_decision)
    elif review_decision == "REVIEW_REQUIRED":
        add(
            findings,
            "FAIL",
            "review_decision",
            "PR still requires review before merge.",
            actual=review_decision,
            expected="APPROVED",
        )
    else:
        add(
            findings,
            "FAIL",
            "review_decision",
            "PR has a blocking review decision.",
            actual=review_decision,
            expected="APPROVED",
        )

    status_rollup_findings(pr_data, findings)

    auto_merge_request = pr_data.get("autoMergeRequest")
    if auto_merge_request:
        add(findings, "PASS", "auto_merge_request", "Auto-merge is already configured.", actual=True)
    else:
        add(findings, "WARN", "auto_merge_request", "Auto-merge is not configured.", actual=False)

    summary = {
        "number": pr_data.get("number"),
        "url": pr_data.get("url"),
        "base": pr_data.get("baseRefName"),
        "head": pr_data.get("headRefName"),
    }
    return summary, findings


def emit(summary: dict[str, object], findings: list[Finding], *, as_json: bool) -> int:
    counts = {"FAIL": 0, "WARN": 0, "PASS": 0, "SKIP": 0}
    for finding in findings:
        counts[finding.level] = counts.get(finding.level, 0) + 1

    payload = {
        "summary": summary,
        "counts": counts,
        "findings": [asdict(finding) for finding in findings],
    }

    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"summary: {json.dumps(summary, sort_keys=True)}")
        print(f"counts: {json.dumps(counts, sort_keys=True)}")
        for finding in findings:
            print(f"[{finding.level}] {finding.check}: {finding.message}")
            if finding.actual is not None:
                print(f"  actual: {json.dumps(finding.actual, sort_keys=True)}")
            if finding.expected is not None:
                print(f"  expected: {json.dumps(finding.expected, sort_keys=True)}")

    return 1 if counts.get("FAIL", 0) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", type=pathlib.Path, default=pathlib.Path.cwd(), help="Repo working directory used for git and gh context.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    repo_parser = subparsers.add_parser("repo-health", help="Check live repo settings and moderation or security posture.")
    repo_parser.add_argument("--repo", help="GitHub repo in OWNER/REPO form. Defaults to the current git origin remote.")

    pr_parser = subparsers.add_parser("pr-readiness", help="Check live PR readiness for merge.")
    pr_parser.add_argument("--pr", help="PR number, URL, or branch. Defaults to the PR attached to the current branch.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    cwd = args.cwd

    try:
        if args.command == "repo-health":
            repo = args.repo or detect_repo(cwd)
            summary, findings = repo_health(repo, cwd)
            return emit(summary, findings, as_json=args.json)

        selector = args.pr
        if selector is None:
            branch = current_branch(cwd)
            selector = branch if branch else None
        summary, findings = pr_readiness(selector, cwd)
        return emit(summary, findings, as_json=args.json)
    except CommandError as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
