#!/usr/bin/env python3
"""Shared GitHub CLI helpers for scripted Ceratops GitHub skills."""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
from dataclasses import dataclass


ROOT = pathlib.Path.cwd()
API_VERSION = "2026-03-10"
REMOTE_RE = re.compile(
    r"""
    (?:
        github\.com[:/]
        |
        api\.github\.com/repos/
    )
    (?P<owner>[^/\s:]+)
    /
    (?P<repo>[^/\s.]+?)(?:\.git)?$
    """,
    re.VERBOSE,
)


class CommandError(RuntimeError):
    """Raised when a required local command fails."""


@dataclass(frozen=True)
class ApiResult:
    ok: bool
    status: int | None
    data: object | None
    stderr: str


def run_command(args: list[str], cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def require_command(args: list[str], cwd: pathlib.Path | None = None) -> str:
    completed = run_command(args, cwd=cwd)
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip() or "command failed"
        raise CommandError(f"{' '.join(args)}: {stderr}")
    return completed.stdout.strip()


def current_branch(cwd: pathlib.Path | None = None) -> str:
    return require_command(["git", "branch", "--show-current"], cwd=cwd)


def detect_repo(cwd: pathlib.Path | None = None) -> str:
    remote = require_command(["git", "remote", "get-url", "origin"], cwd=cwd)
    match = REMOTE_RE.search(remote)
    if not match:
        raise CommandError(f"could not parse GitHub repo from remote URL: {remote}")
    return f"{match.group('owner')}/{match.group('repo')}"


def gh_api(path: str, *, cwd: pathlib.Path | None = None) -> ApiResult:
    completed = run_command(
        [
            "gh",
            "api",
            "-H",
            "Accept: application/vnd.github+json",
            "-H",
            f"X-GitHub-Api-Version: {API_VERSION}",
            path,
        ],
        cwd=cwd,
    )
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    if completed.returncode == 0:
        data = json.loads(stdout) if stdout else None
        return ApiResult(ok=True, status=200, data=data, stderr=stderr)

    status = None
    match = re.search(r"\b(\d{3})\b", stderr)
    if match:
        status = int(match.group(1))
    return ApiResult(ok=False, status=status, data=None, stderr=stderr or stdout)


def gh_pr_view(selector: str | None, *, cwd: pathlib.Path | None = None) -> dict[str, object]:
    args = [
        "gh",
        "pr",
        "view",
        "--json",
        ",".join(
            [
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
        ),
    ]
    if selector:
        args.append(selector)
    output = require_command(args, cwd=cwd)
    return json.loads(output)
