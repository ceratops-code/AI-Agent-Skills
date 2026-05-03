#!/usr/bin/env python3
"""Check current GitHub pull-request readiness for Ceratops merge workflows.

This script is intentionally narrow. Repository health and artifact posture are
owned by the JSON contract checkers; this helper only answers the merge decision
question that still needs live PR state close to the final action.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Any


class CommandError(RuntimeError):
    """Raised when a required local command fails."""


@dataclass(frozen=True)
class Finding:
    """One machine-readable readiness finding."""

    level: str
    check: str
    message: str
    actual: object | None = None
    expected: object | None = None


def run_command(args: list[str], cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    """Run a command without shell expansion and keep stdout/stderr separate."""

    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def require_command(args: list[str], cwd: pathlib.Path) -> str:
    """Run a command and return stdout, raising a compact error on failure."""

    completed = run_command(args, cwd)
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip() or "command failed"
        raise CommandError(f"{' '.join(args)}: {stderr}")
    return completed.stdout.strip()


def current_branch(cwd: pathlib.Path) -> str | None:
    """Return the current git branch when the working directory is a checkout."""

    completed = run_command(["git", "branch", "--show-current"], cwd)
    if completed.returncode != 0:
        return None
    branch = completed.stdout.strip()
    return branch or None


def gh_pr_view(selector: str | None, cwd: pathlib.Path) -> dict[str, Any]:
    """Fetch the live PR fields used by the merge-readiness policy."""

    fields = [
        "number",
        "url",
        "state",
        "isDraft",
        "mergeable",
        "reviewDecision",
        "statusCheckRollup",
        "headRefName",
        "baseRefName",
        "autoMergeRequest",
    ]
    args = ["gh", "pr", "view", "--json", ",".join(fields)]
    if selector:
        args.append(selector)
    return json.loads(require_command(args, cwd))


def add(
    findings: list[Finding],
    level: str,
    check: str,
    message: str,
    *,
    actual: object | None = None,
    expected: object | None = None,
) -> None:
    """Append a finding with consistent field names."""

    findings.append(Finding(level=level, check=check, message=message, actual=actual, expected=expected))


def status_rollup_findings(pr_data: dict[str, Any], findings: list[Finding]) -> None:
    """Classify the visible status checks attached to the PR."""

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


def pr_readiness(selector: str | None, cwd: pathlib.Path) -> tuple[dict[str, object], list[Finding]]:
    """Evaluate the live PR state needed before merge or auto-merge."""

    pr_data = gh_pr_view(selector, cwd)
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
        add(findings, "FAIL", "review_decision", "PR still requires review before merge.", actual=review_decision, expected="APPROVED")
    else:
        add(findings, "FAIL", "review_decision", "PR has a blocking review decision.", actual=review_decision, expected="APPROVED")

    status_rollup_findings(pr_data, findings)

    if pr_data.get("autoMergeRequest"):
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
    """Print JSON or compact text and return a failing status only on FAIL."""

    counts = {"FAIL": 0, "WARN": 0, "INFO": 0, "PASS": 0, "SKIP": 0}
    for finding in findings:
        counts[finding.level] = counts.get(finding.level, 0) + 1

    payload = {"summary": summary, "counts": counts, "findings": [asdict(finding) for finding in findings]}
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
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
    """Create the command-line parser."""

    parser = argparse.ArgumentParser(description="Check live GitHub PR readiness for merge.")
    parser.add_argument("--cwd", type=pathlib.Path, default=pathlib.Path.cwd(), help="Repo working directory used for git and gh context.")
    parser.add_argument("--pr", help="PR number, URL, or branch. Defaults to the PR attached to the current branch.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    cwd = args.cwd.resolve()
    try:
        selector = args.pr
        if selector is None:
            selector = current_branch(cwd)
        summary, findings = pr_readiness(selector, cwd)
        return emit(summary, findings, as_json=args.json)
    except CommandError as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}, sort_keys=True))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
