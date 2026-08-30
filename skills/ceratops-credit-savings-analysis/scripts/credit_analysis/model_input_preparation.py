"""Prepare bounded retained evidence for model input."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

from .single_thread_analysis import CreditAnalysisError, _bounded_value


def _review_record_index(evidence: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Index retained model-review records without changing their content."""

    model_review = evidence.get("model_review")
    if not isinstance(model_review, Mapping):
        raise CreditAnalysisError("model-review evidence is invalid")
    records = model_review.get("records")
    if not isinstance(records, list):
        raise CreditAnalysisError("model-review records are invalid")
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise CreditAnalysisError("model-review record is invalid")
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or record_id in indexed:
            raise CreditAnalysisError("model-review record ID is invalid")
        indexed[record_id] = record
    return indexed


SURFACE_EVIDENCE_KEYWORDS = {
    "helper-contracts": (
        "helper",
        "script",
        "contract",
        "cleanup",
        "rollback",
        "dependency",
        "output",
    ),
    "context-evidence": (
        "read",
        "search",
        "context",
        "evidence",
        "token",
        "cached",
        "path",
    ),
    "rework-validation": (
        "failed",
        "error",
        "retry",
        "again",
        "temporary",
        "workaround",
        "patch",
        "revert",
        "correct",
    ),
    "tool-flow": (
        "tool",
        "command",
        "wait",
        "timeout",
        "terminated",
        "result",
        "exit",
    ),
    "instruction-reasoning": (
        "instruction",
        "rule",
        "prompt",
        "clarif",
        "approve",
        "plan",
        "skill",
    ),
}
OUTCOME_KEYS = frozenset(
    {
        "code",
        "error",
        "errors",
        "exit_code",
        "returncode",
        "status",
        "stderr",
        "success",
        "terminated",
        "termination",
        "timed_out",
        "timeout",
    }
)


def _structured_outcome(value: Any, *, depth: int = 0) -> Any:
    """Project explicit process/result telemetry without semantic judgment."""

    if depth > 5:
        return None
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            normalized = str(key).casefold()
            if normalized in OUTCOME_KEYS:
                result[str(key)] = _bounded_value(item, text_limit=600)
                continue
            nested = _structured_outcome(item, depth=depth + 1)
            if nested not in (None, {}, []):
                result[str(key)] = nested
        return result or None
    if isinstance(value, list):
        items = [
            projected
            for item in value
            if (projected := _structured_outcome(item, depth=depth + 1))
            is not None
        ]
        return items or None
    return None


def _relevant_segments(text: str, surface_id: str) -> list[dict[str, Any]]:
    """Retain bounded deterministic windows around surface-relevant terms."""

    lowered = text.casefold()
    segments: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for keyword in SURFACE_EVIDENCE_KEYWORDS[surface_id]:
        start = 0
        while len(segments) < 4:
            position = lowered.find(keyword, start)
            if position < 0:
                break
            left = max(0, position - 350)
            right = min(len(text), position + len(keyword) + 650)
            bounds = (left, right)
            if not any(
                left < old_right and right > old_left
                for old_left, old_right in seen
            ):
                seen.add(bounds)
                segments.append(
                    {"start": left, "end": right, "text": text[left:right]}
                )
            start = position + len(keyword)
        if len(segments) >= 4:
            break
    return segments


def _shared_relevant_segments(
    text: str,
    surface_ids: Sequence[str],
    *,
    text_limit: int,
) -> list[dict[str, Any]]:
    """Keep one deterministic non-overlapping segment per applicable surface."""

    result: list[dict[str, Any]] = []
    bounds: list[tuple[int, int]] = []
    for surface_id in surface_ids:
        for segment in _relevant_segments(text, surface_id):
            start = int(segment["start"])
            end = int(segment["end"])
            if any(
                start < prior_end and end > prior_start
                for prior_start, prior_end in bounds
            ):
                continue
            bounds.append((start, end))
            result.append(
                {
                    "surface_id": surface_id,
                    "start": start,
                    "end": end,
                    "text": str(segment["text"])[:text_limit],
                }
            )
            break
    return result


def _prepare_bounded_evidence(
    value: Any,
    *,
    limit: int,
    surface_ids: Sequence[str],
) -> Any:
    """Keep useful bounded evidence while the complete value remains retained."""

    serialized = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    if len(serialized) <= limit:
        return {"mode": "complete", "value": value}
    segments = _shared_relevant_segments(
        serialized,
        surface_ids,
        text_limit=max(160, min(420, limit // 2)),
    )[:2]
    return {
        "mode": "retained-projection",
        "chars": len(serialized),
        "sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "structured_outcome": _structured_outcome(value),
        "head": serialized[: min(300, limit // 3)],
        "relevant_segments": segments,
        "tail": serialized[-min(300, limit // 3) :],
    }


__all__ = (
    "OUTCOME_KEYS",
    "SURFACE_EVIDENCE_KEYWORDS",
    "_prepare_bounded_evidence",
    "_relevant_segments",
    "_review_record_index",
    "_shared_relevant_segments",
    "_structured_outcome",
)
