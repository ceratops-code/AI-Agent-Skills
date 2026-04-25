"""Module entrypoint for the Ceratops GitHub helper package."""

from __future__ import annotations

from .gh_current_state_checks import main


if __name__ == "__main__":
    raise SystemExit(main())
