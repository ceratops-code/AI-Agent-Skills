"""Load exact governance source bytes and shared validation data.

These primitives preserve UTF-8 encoding and physical line endings for candidate
validation and approved application. They never mutate source files; callers
own the evidence and atomic-write lifecycle.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

UTF8_BOM = b"\xef\xbb\xbf"


class RuleCandidateValidationError(ValueError):
    """One compact mechanical candidate failure with actionable location."""


@dataclass(frozen=True)
class TextSource:
    """Exact UTF-8 source bytes and formatting conventions to preserve."""

    path: Path
    raw: bytes
    text: str
    has_bom: bool
    newline: str
    trailing_newline: bool

    def encode(self, text: str) -> bytes:
        encoded = text.encode("utf-8")
        return UTF8_BOM + encoded if self.has_bom else encoded


@dataclass(frozen=True)
class ReplacementSpan:
    """One replacement's bounds in a complete prospective target."""

    index: int
    start: int
    end: int


@dataclass
class ValidationResult:
    """Validated candidate plus exact prospective target documents."""

    candidate: dict[str, Any]
    sources: dict[Path, TextSource]
    prospective_texts: dict[Path, str]
    candidate_sha256: str
    changed: bool


def _closed_fields(
    value: object,
    fields: set[str],
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuleCandidateValidationError(f"{label} must be an object")
    missing = sorted(fields - set(value))
    extra = sorted(set(value) - fields)
    if missing or extra:
        raise RuleCandidateValidationError(
            f"{label} fields invalid; missing={missing} extra={extra}"
        )
    return cast(dict[str, Any], value)


def _absolute_path(value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise RuleCandidateValidationError(f"{label} must be a non-empty path")
    path = Path(value)
    if not path.is_absolute():
        raise RuleCandidateValidationError(f"{label} must be absolute")
    return Path(os.path.abspath(path.expanduser()))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_hash(path: Path) -> str:
    """Return a SHA-256 hash without loading an arbitrary file twice."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _valid_sha256(value: object) -> bool:
    return bool(
        isinstance(value, str)
        and re.fullmatch(r"[0-9a-f]{64}", value)
    )


def newline_styles(text: str) -> set[str]:
    """Return every concrete line-ending form present in text."""

    without_crlf = text.replace("\r\n", "")
    styles: set[str] = set()
    if "\r\n" in text:
        styles.add("\r\n")
    if "\n" in without_crlf:
        styles.add("\n")
    if "\r" in without_crlf:
        styles.add("\r")
    return styles


def read_source(path: Path, label: str) -> TextSource:
    """Read one non-empty UTF-8 source without normalizing bytes."""

    if not path.is_file():
        raise RuleCandidateValidationError(f"{label} does not exist: {path}")
    raw = path.read_bytes()
    has_bom = raw.startswith(UTF8_BOM)
    payload = raw[len(UTF8_BOM) :] if has_bom else raw
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuleCandidateValidationError(
            f"{label} is not UTF-8: {path}"
        ) from exc
    if not text.strip():
        raise RuleCandidateValidationError(f"{label} is empty: {path}")
    styles = newline_styles(text)
    if len(styles) > 1:
        raise RuleCandidateValidationError(
            f"{label} has mixed line endings: {path}"
        )
    newline = next(iter(styles), "\n")
    return TextSource(
        path=path,
        raw=raw,
        text=text,
        has_bom=has_bom,
        newline=newline,
        trailing_newline=text.endswith(newline),
    )
