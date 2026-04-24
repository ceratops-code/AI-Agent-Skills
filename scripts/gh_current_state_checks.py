#!/usr/bin/env python3
"""Compatibility wrapper for the Ceratops GitHub helper package."""

from __future__ import annotations

import pathlib
import sys


SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ceratops_gh_runtime.gh_current_state_checks import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
