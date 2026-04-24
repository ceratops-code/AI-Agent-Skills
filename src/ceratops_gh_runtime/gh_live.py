#!/usr/bin/env python3
"""Compatibility alias for the GH current-state helpers."""

from __future__ import annotations

from .gh_current_state import (  # noqa: F401
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
