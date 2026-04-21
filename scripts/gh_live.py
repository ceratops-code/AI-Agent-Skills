#!/usr/bin/env python3
"""Compatibility wrapper for the Ceratops GitHub helper package."""

from __future__ import annotations

import pathlib
import sys


SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ceratops_gh_runtime.gh_live import (  # noqa: E402
    API_VERSION,
    ROOT,
    ApiResult,
    CommandError,
    current_branch,
    detect_repo,
    gh_api,
    gh_pr_view,
    require_command,
    run_command,
)

__all__ = [
    "API_VERSION",
    "ROOT",
    "ApiResult",
    "CommandError",
    "current_branch",
    "detect_repo",
    "gh_api",
    "gh_pr_view",
    "require_command",
    "run_command",
]
