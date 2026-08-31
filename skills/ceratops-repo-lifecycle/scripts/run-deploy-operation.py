#!/usr/bin/env python3
"""Execute one named local deployment from the repository SDLC contract."""

from __future__ import annotations

import pathlib
from collections.abc import Mapping

from repository_operation import OperationProfile, operation_main
from repository_operation import run_operation as _run_operation

SCRIPT_ROOT = pathlib.Path(__file__).resolve().parent
DEFAULT_CONTRACT = pathlib.Path("sdlc/sdlc.yml")
PROFILE = OperationProfile(
    label="Deployment",
    section="deploy",
    default_contract=DEFAULT_CONTRACT,
    schema=SCRIPT_ROOT.parent / "references" / "schemas" / "sdlc.yml.schema.json",
    default_success_status="deployed",
    operation_statuses={},
)


def run_operation(
    repo_root: pathlib.Path,
    operation: str,
    contract_path: pathlib.Path = DEFAULT_CONTRACT,
    parameters: Mapping[str, str] | None = None,
    parameters_if_declared: Mapping[str, str] | None = None,
    *,
    if_declared: bool = False,
) -> dict[str, object]:
    """Run one local deployment from the unified contract's deploy section."""

    return _run_operation(
        repo_root,
        operation,
        PROFILE,
        contract_path,
        parameters,
        parameters_if_declared,
        if_declared=if_declared,
    )


def main(argv: list[str] | None = None) -> int:
    """Execute one deployment operation and emit one compact result."""

    return operation_main(PROFILE, argv)


if __name__ == "__main__":
    raise SystemExit(main())
