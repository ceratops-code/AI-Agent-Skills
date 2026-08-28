"""Freeze and reopen one task-local credit-analysis contract snapshot.

Fresh planning copies the exact validated installed contract into controller
ownership. Resumes hash-check and load only that retained copy, so deploying a
new skill cannot mutate an existing analysis. Snapshot paths must remain inside
the caller's verified task root and must never be links.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
from collections.abc import Mapping
from typing import Any


class ContractSnapshotError(ValueError):
    """Report an invalid or changed task-local contract snapshot."""


def _is_link(path: pathlib.Path) -> bool:
    junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(junction and junction())


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _inside_task_root(path: pathlib.Path, task_root: pathlib.Path, label: str) -> None:
    try:
        path.relative_to(task_root)
    except ValueError as exc:
        raise ContractSnapshotError(f"{label} escapes task root") from exc


def freeze_contract_snapshot(
    source: pathlib.Path,
    destination: pathlib.Path,
    *,
    task_root: pathlib.Path,
) -> dict[str, str]:
    """Copy exact contract bytes once and return their immutable state record."""

    root = task_root.expanduser().resolve(strict=True)
    if _is_link(root) or not root.is_dir():
        raise ContractSnapshotError("contract snapshot task root is invalid")
    source_path = source.expanduser().resolve(strict=True)
    if _is_link(source_path) or not source_path.is_file():
        raise ContractSnapshotError("installed contract source is invalid")
    destination_path = destination.expanduser()
    if not destination_path.is_absolute():
        raise ContractSnapshotError("contract snapshot path must be absolute")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    parent = destination_path.parent.resolve(strict=True)
    _inside_task_root(parent, root, "contract snapshot path")
    target = parent / destination_path.name
    if target.exists() or _is_link(target):
        raise ContractSnapshotError("refusing to overwrite contract snapshot")
    payload = source_path.read_bytes()
    try:
        with target.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise ContractSnapshotError(f"could not write contract snapshot: {exc}") from exc
    if target.read_bytes() != payload:
        raise ContractSnapshotError("contract snapshot verification failed")
    return {"path": str(target), "sha256": _sha256(payload)}


def load_contract_snapshot(
    record: Mapping[str, Any],
    *,
    task_root: pathlib.Path,
) -> dict[str, Any]:
    """Validate one retained snapshot record and decode its frozen contract."""

    if set(record) != {"path", "sha256"}:
        raise ContractSnapshotError("contract snapshot record is invalid")
    raw_path = record.get("path")
    expected_hash = record.get("sha256")
    if not isinstance(raw_path, str) or not raw_path:
        raise ContractSnapshotError("contract snapshot path is invalid")
    if (
        not isinstance(expected_hash, str)
        or len(expected_hash) != 64
        or any(character not in "0123456789abcdef" for character in expected_hash)
    ):
        raise ContractSnapshotError("contract snapshot hash is invalid")
    root = task_root.expanduser().resolve(strict=True)
    path = pathlib.Path(raw_path).expanduser()
    if _is_link(path):
        raise ContractSnapshotError("contract snapshot must not be linked")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ContractSnapshotError("contract snapshot is missing") from exc
    _inside_task_root(resolved, root, "contract snapshot")
    if not resolved.is_file() or _is_link(resolved):
        raise ContractSnapshotError("contract snapshot is invalid")
    payload = resolved.read_bytes()
    if _sha256(payload) != expected_hash:
        raise ContractSnapshotError("contract snapshot changed")
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ContractSnapshotError("contract snapshot is invalid JSON") from exc
    if not isinstance(value, dict):
        raise ContractSnapshotError("contract snapshot must be an object")
    return value


__all__ = (
    "ContractSnapshotError",
    "freeze_contract_snapshot",
    "load_contract_snapshot",
)
