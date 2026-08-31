"""Prepare and execute schema-validated repository operations without a shell.

Release publication and local deployment select separate sections of one
repository-owned ``sdlc/sdlc.yml`` while sharing exact argv handling, strict
parameters, repository-bounded working directories, compact results, and
bounded structured failure evidence. The executor does not infer lifecycle
timing or whether an operation is a check or a side effect.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, cast

from ceratops_repo_compatibility_engine.sdlc_contract_validation import (
    SdlcContractError,
    load_contract,
)

PARAMETER_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PLACEHOLDER_RE = re.compile(r"^\{(?P<name>[a-z][a-z0-9_]*)\}$")
FAILURE_TAIL_LINES = 8
FAILURE_TAIL_CHARS = 4096


@dataclass(frozen=True)
class OperationProfile:
    """Describe one contract section without weakening shared execution rules."""

    label: str
    section: str
    default_contract: pathlib.Path
    schema: pathlib.Path
    default_success_status: str
    operation_statuses: Mapping[str, str]


@dataclass(frozen=True)
class OperationRequest:
    """Select one operation and its exact parameter policy for preparation."""

    operation: str
    parameters: Mapping[str, str] | None = None
    parameters_if_declared: Mapping[str, str] | None = None
    if_declared: bool = False


@dataclass(frozen=True)
class PreparedStep:
    """One repository-bounded command ready for shell-free execution."""

    step_id: str
    argv: tuple[str, ...]
    cwd: pathlib.Path


@dataclass(frozen=True)
class PreparedOperation:
    """One fully validated operation whose commands have not executed."""

    repo_root: pathlib.Path
    operation: str
    label: str
    success_status: str
    steps: tuple[PreparedStep, ...]
    handoff: str | None
    no_op_reason: str | None = None


class OperationError(RuntimeError):
    """Raised when a contract or operation violates its repository boundary."""


def _inside(path: pathlib.Path, parent: pathlib.Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _read_contract(
    repo_root: pathlib.Path,
    contract_path: pathlib.Path,
    profile: OperationProfile,
) -> Mapping[str, Any]:
    resolved = (
        contract_path if contract_path.is_absolute() else repo_root / contract_path
    ).resolve(strict=True)
    if not resolved.is_file() or not _inside(resolved, repo_root):
        raise OperationError(
            f"{profile.label} contract must be a file inside the repository."
        )
    try:
        return load_contract(resolved, schema_path=profile.schema)
    except SdlcContractError as exc:
        raise OperationError(
            f"Invalid {profile.label.lower()} contract: {exc}"
        ) from exc


def _contract_section(
    contract: Mapping[str, Any], profile: OperationProfile
) -> Mapping[str, Any] | None:
    selected = contract.get(profile.section)
    if selected is None:
        return None
    if not isinstance(selected, Mapping):
        raise OperationError(f"{profile.label} contract section is invalid.")
    return selected


def _operation_steps(
    section: Mapping[str, Any],
    operation: str,
    profile: OperationProfile,
) -> tuple[Mapping[str, Any], Sequence[Mapping[str, Any]]]:
    operations = section.get("operations")
    if not isinstance(operations, Mapping) or operation not in operations:
        raise OperationError(f"{profile.label} operation is not declared: {operation}")
    selected = operations[operation]
    if not isinstance(selected, Mapping):
        raise OperationError(f"{profile.label} operation is invalid: {operation}")
    steps = selected.get("steps", [])
    if not isinstance(steps, Sequence) or isinstance(steps, (str, bytes)):
        raise OperationError(
            f"{profile.label} operation has no valid steps: {operation}"
        )
    return selected, steps


def parse_parameters(values: Sequence[str], profile: OperationProfile) -> dict[str, str]:
    """Parse unique nonempty ``name=value`` operation parameters."""

    result: dict[str, str] = {}
    for value in values:
        name, separator, parameter = value.partition("=")
        if (
            not separator
            or PARAMETER_NAME_RE.fullmatch(name) is None
            or not parameter
        ):
            raise OperationError(
                f"{profile.label} parameters must use name=value."
            )
        if name in result:
            raise OperationError(
                f"Duplicate {profile.label.lower()} parameter: {name}"
            )
        result[name] = parameter
    return result


def _expanded_argv(
    argv: Sequence[str],
    parameters: Mapping[str, str],
    profile: OperationProfile,
) -> list[str]:
    """Replace only whole-argument declared placeholders."""

    expanded: list[str] = []
    for value in argv:
        match = PLACEHOLDER_RE.fullmatch(value)
        if match is None:
            expanded.append(value)
            continue
        name = match.group("name")
        if name not in parameters:
            raise OperationError(
                f"Missing {profile.label.lower()} parameter: {name}"
            )
        expanded.append(parameters[name])
    return expanded


def _working_directory(
    repo_root: pathlib.Path,
    step: Mapping[str, Any],
    profile: OperationProfile,
) -> pathlib.Path:
    raw = step.get("cwd", ".")
    if not isinstance(raw, str):
        raise OperationError(f"{profile.label} step cwd must be text.")
    cwd = (repo_root / raw).resolve(strict=True)
    if not cwd.is_dir() or not _inside(cwd, repo_root):
        raise OperationError(
            f"{profile.label} step cwd must be a directory inside the repository."
        )
    return cwd


def _repository_commit(repo_root: pathlib.Path) -> str | None:
    """Return the exact current commit when the operation root is a Git worktree."""

    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else None


def _bounded_tail(value: str | None) -> list[str]:
    """Retain only the final bounded lines of one captured stream."""

    return (value or "")[-FAILURE_TAIL_CHARS:].splitlines()[-FAILURE_TAIL_LINES:]


def _supplied_parameters(
    selected: Mapping[str, Any],
    request: OperationRequest,
    profile: OperationProfile,
) -> dict[str, str]:
    expected = selected.get("parameters", [])
    if (
        not isinstance(expected, Sequence)
        or isinstance(expected, (str, bytes))
        or not all(isinstance(value, str) for value in expected)
    ):
        raise OperationError(
            f"{profile.label} operation has invalid parameters: {request.operation}"
        )
    declared = set(expected)
    supplied = dict(request.parameters or {})
    conditional = dict(request.parameters_if_declared or {})
    duplicated = sorted(set(supplied) & set(conditional))
    if duplicated:
        raise OperationError(
            f"{profile.label} parameter supplied more than once: "
            + ", ".join(duplicated)
        )
    supplied.update(
        (name, value) for name, value in conditional.items() if name in declared
    )
    missing = sorted(declared - set(supplied))
    extra = sorted(set(request.parameters or {}) - declared)
    if missing or extra:
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if extra:
            detail.append("unexpected " + ", ".join(extra))
        raise OperationError(
            f"{profile.label} parameter mismatch: " + "; ".join(detail)
        )
    return supplied


def _no_op(
    repo_root: pathlib.Path,
    request: OperationRequest,
    profile: OperationProfile,
    reason: str,
) -> PreparedOperation:
    return PreparedOperation(
        repo_root=repo_root,
        operation=request.operation,
        label=profile.label,
        success_status=profile.operation_statuses.get(
            request.operation, profile.default_success_status
        ),
        steps=(),
        handoff=None,
        no_op_reason=reason,
    )


def prepare_operations(
    repo_root: pathlib.Path,
    requests: Sequence[OperationRequest],
    profile: OperationProfile,
    contract_path: pathlib.Path | None = None,
) -> list[PreparedOperation]:
    """Validate an ordered operation sequence completely before any command runs."""

    if not requests:
        raise OperationError("At least one operation request is required.")
    root = repo_root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise OperationError("Repository root is not a directory.")
    contract = _read_contract(root, contract_path or profile.default_contract, profile)
    section = _contract_section(contract, profile)
    if section is None:
        return [
            _no_op(root, request, profile, "contract_section_not_declared")
            for request in requests
        ]
    operations = section.get("operations")
    prepared_operations: list[PreparedOperation] = []
    for request in requests:
        if (
            request.if_declared
            and isinstance(operations, Mapping)
            and request.operation not in operations
        ):
            prepared_operations.append(
                _no_op(root, request, profile, "operation_not_declared")
            )
            continue
        selected, steps = _operation_steps(section, request.operation, profile)
        supplied = _supplied_parameters(selected, request, profile)
        prepared_steps: list[PreparedStep] = []
        for step in steps:
            step_id = step.get("id")
            argv = step.get("run")
            if (
                not isinstance(step_id, str)
                or not isinstance(argv, Sequence)
                or isinstance(argv, (str, bytes))
                or not all(isinstance(value, str) and value for value in argv)
            ):
                raise OperationError(
                    f"{profile.label} operation has an invalid step: "
                    f"{request.operation}"
                )
            prepared_steps.append(
                PreparedStep(
                    step_id=step_id,
                    argv=tuple(
                        _expanded_argv(cast(Sequence[str], argv), supplied, profile)
                    ),
                    cwd=_working_directory(root, step, profile),
                )
            )
        handoff = selected.get("handoff")
        prepared_operations.append(
            PreparedOperation(
                repo_root=root,
                operation=request.operation,
                label=profile.label,
                success_status=profile.operation_statuses.get(
                    request.operation, profile.default_success_status
                ),
                steps=tuple(prepared_steps),
                handoff=handoff if isinstance(handoff, str) else None,
            )
        )
    return prepared_operations


def execute_prepared_operation(prepared: PreparedOperation) -> dict[str, object]:
    """Execute one validated operation and return compact structured evidence."""

    if prepared.no_op_reason is not None:
        return {
            "status": "no_op",
            "operation": prepared.operation,
            "steps": [],
            "reason": prepared.no_op_reason,
        }
    commit = _repository_commit(prepared.repo_root)
    completed: list[str] = []
    for step in prepared.steps:
        try:
            result = subprocess.run(
                list(step.argv),
                cwd=step.cwd,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            return {
                "status": "operation_failed",
                "message": f"{prepared.label} step could not start: {step.step_id}",
                "operation": prepared.operation,
                "commit": commit,
                "steps": completed,
                "failed_step": step.step_id,
                "diagnostic": {
                    "exit_code": None,
                    "stdout_tail": [],
                    "stderr_tail": _bounded_tail(str(exc)),
                },
            }
        if result.returncode != 0:
            return {
                "status": "operation_failed",
                "message": f"{prepared.label} step failed: {step.step_id}",
                "operation": prepared.operation,
                "commit": commit,
                "steps": completed,
                "failed_step": step.step_id,
                "diagnostic": {
                    "exit_code": result.returncode,
                    "stdout_tail": _bounded_tail(result.stdout),
                    "stderr_tail": _bounded_tail(result.stderr),
                },
            }
        completed.append(step.step_id)

    operation_result: dict[str, object] = {
        "status": prepared.success_status,
        "operation": prepared.operation,
        "commit": commit,
        "steps": completed,
    }
    if prepared.handoff is not None:
        operation_result["handoff"] = prepared.handoff
    return operation_result


def execute_prepared_operations(
    prepared: Sequence[PreparedOperation],
) -> dict[str, object]:
    """Execute an ordered prepared sequence and stop with a completed/pending ledger."""

    completed: list[str] = []
    results: list[dict[str, object]] = []
    for index, operation in enumerate(prepared):
        result = execute_prepared_operation(operation)
        results.append(result)
        if result.get("status") == "operation_failed":
            return {
                "status": "operation_failed",
                "completed_operations": completed,
                "pending_operations": [
                    item.operation for item in prepared[index:]
                ],
                "results": results,
            }
        completed.append(operation.operation)
    return {
        "status": "completed",
        "completed_operations": completed,
        "pending_operations": [],
        "results": results,
    }


def run_operation(
    repo_root: pathlib.Path,
    operation: str,
    profile: OperationProfile,
    contract_path: pathlib.Path | None = None,
    parameters: Mapping[str, str] | None = None,
    parameters_if_declared: Mapping[str, str] | None = None,
    *,
    if_declared: bool = False,
) -> dict[str, object]:
    """Prepare and run one declared operation through the shared executor."""

    prepared = prepare_operations(
        repo_root,
        [
            OperationRequest(
                operation=operation,
                parameters=parameters,
                parameters_if_declared=parameters_if_declared,
                if_declared=if_declared,
            )
        ],
        profile,
        contract_path,
    )
    return execute_prepared_operation(prepared[0])


def build_parser(profile: OperationProfile) -> argparse.ArgumentParser:
    """Create the parser for one contract-section-specific executable wrapper."""

    parser = argparse.ArgumentParser(
        description=(
            f"Execute one {profile.section} operation from "
            f"{profile.default_contract.as_posix()}."
        )
    )
    parser.add_argument("--repo-root", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument(
        "--contract", type=pathlib.Path, default=profile.default_contract
    )
    parser.add_argument("--operation", required=True)
    parser.add_argument("--parameter", action="append", default=[])
    parser.add_argument("--parameter-if-declared", action="append", default=[])
    parser.add_argument(
        "--if-declared",
        action="store_true",
        help="Return an explicit no-op when the selected operation is absent.",
    )
    return parser


def operation_main(
    profile: OperationProfile,
    argv: list[str] | None = None,
) -> int:
    """Execute one profile and emit only its compact machine result."""

    args = build_parser(profile).parse_args(argv)
    try:
        result = run_operation(
            args.repo_root,
            args.operation,
            profile,
            args.contract,
            parse_parameters(args.parameter, profile),
            parse_parameters(args.parameter_if_declared, profile),
            if_declared=args.if_declared,
        )
    except (OperationError, OSError, ValueError) as exc:
        print(
            json.dumps(
                {"status": "error", "message": str(exc)},
                separators=(",", ":"),
            ),
            file=sys.stderr,
        )
        return 1
    stream = sys.stderr if result.get("status") == "operation_failed" else sys.stdout
    print(json.dumps(result, separators=(",", ":")), file=stream)
    return 1 if result.get("status") == "operation_failed" else 0
