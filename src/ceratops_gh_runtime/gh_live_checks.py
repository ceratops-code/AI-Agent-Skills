#!/usr/bin/env python3
"""Compatibility alias for the GH current-state checks."""

from __future__ import annotations

from .gh_current_state_checks import main


if __name__ == "__main__":
    raise SystemExit(main())
