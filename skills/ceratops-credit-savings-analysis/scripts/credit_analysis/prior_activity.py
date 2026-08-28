"""Deterministic projections and lineage loading for prior analysis evidence.

This module owns bounded semantic projections, discovery of explicitly
referenced orchestration state, and read-only loading of retained prior-analysis
artifacts. Complete artifacts stay at their controller-owned paths; later
analyses receive only hash-validated bounded projections and never gain mutation
authority or native Luna rollout state.
"""
# ruff: noqa: F401,F403,F405,I001

from __future__ import annotations

from .core import *


def _review_record_index(evidence: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
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


def _holistic_projection(
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


def _holistic_state_paths(value: Any) -> list[pathlib.Path]:
    """Find exact controller state paths only in structured tool output."""

    found: list[pathlib.Path] = []

    def visit(item: Any) -> None:
        if isinstance(item, Mapping):
            state_path = item.get("state_path")
            if isinstance(state_path, str) and state_path:
                resolved_text = state_path
                if resolved_text.startswith("<user-home>"):
                    resolved_text = str(pathlib.Path.home()) + resolved_text[
                        len("<user-home>") :
                    ]
                found.append(pathlib.Path(resolved_text))
            for nested in item.values():
                visit(nested)
            return
        if isinstance(item, list):
            for nested in item:
                visit(nested)
            return
        if not isinstance(item, str) or len(item) > 2_000_000:
            return
        stripped = item.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                visit(json.loads(stripped))
            except json.JSONDecodeError:
                pass
        for match in re.finditer(
            r'"state_path"\s*:\s*("(?:[^"\\]|\\.)*")', item
        ):
            try:
                candidate = json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, str) and candidate:
                resolved_text = candidate
                if resolved_text.startswith("<user-home>"):
                    resolved_text = str(pathlib.Path.home()) + resolved_text[
                        len("<user-home>") :
                    ]
                found.append(pathlib.Path(resolved_text))

    visit(value)
    return list(dict.fromkeys(found))


def _holistic_raw_state_paths_by_call(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, list[pathlib.Path]]:
    """Index transient structured state paths before evidence redaction.

    Raw local paths are used only to load explicitly referenced controller state
    and are never copied into retained evidence. Correlation IDs keep each path
    bound to the model call whose tool result supplied it.
    """

    indexed: dict[str, list[pathlib.Path]] = {}
    for row in rows:
        if row.get("type") != "response_item":
            continue
        payload = row.get("payload")
        if not isinstance(payload, Mapping):
            continue
        item_type = payload.get("type")
        call_id = payload.get("call_id") or payload.get("id")
        if (
            not isinstance(item_type, str)
            or not item_type.endswith("_output")
            or not isinstance(call_id, str)
            or not call_id
        ):
            continue
        paths = _holistic_state_paths(
            {
                key: item
                for key, item in payload.items()
                if key not in {"call_id", "id", "type"}
            }
        )
        if paths:
            indexed[call_id] = list(
                dict.fromkeys([*indexed.get(call_id, []), *paths])
            )
    return indexed


def _retained_text_projection(
    artifact: Any,
    *,
    limit: int,
    surface_ids: Sequence[str],
) -> dict[str, Any]:
    """Load retained text only when its controller-recorded hash still matches."""

    if not isinstance(artifact, Mapping):
        return {"mode": "unavailable", "reason": "artifact-metadata-missing"}
    path_value = artifact.get("path")
    expected_hash = artifact.get("sha256")
    if (
        not isinstance(path_value, str)
        or not path_value
        or not isinstance(expected_hash, str)
        or re.fullmatch(r"[0-9a-f]{64}", expected_hash) is None
    ):
        return {"mode": "unavailable", "reason": "artifact-metadata-invalid"}
    try:
        path = pathlib.Path(path_value).expanduser().resolve(strict=True)
    except OSError:
        return {"mode": "unavailable", "reason": "artifact-missing"}
    if path.is_symlink() or not path.is_file():
        return {"mode": "unavailable", "reason": "artifact-not-regular"}
    if _file_hash(path) != expected_hash:
        return {"mode": "unavailable", "reason": "artifact-hash-mismatch"}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return {"mode": "unavailable", "reason": "artifact-unreadable"}
    return {
        "mode": "verified",
        "artifact_sha256": expected_hash,
        "projection_limit_chars": limit,
        "projection": _holistic_projection(
            text,
            limit=limit,
            surface_ids=surface_ids,
        ),
    }


def _holistic_prior_analysis_activity(
    evidence: Mapping[str, Any],
    *,
    current_analysis_id: str,
    surface_ids: Sequence[str],
    text_limit: int,
    raw_state_paths_by_call: Mapping[str, Sequence[pathlib.Path]],
) -> tuple[list[dict[str, Any]], set[str]]:
    """Load referenced earlier controller telemetry without prompt-text markers."""

    activities: list[dict[str, Any]] = []
    analysis_call_ids: set[str] = set()
    seen_analyses: set[str] = set()
    review_index = _review_record_index(evidence)
    for call in _all_calls(evidence):
        call_id = str(call["call_id"])
        review_records = [
            review_index[record_id]
            for record_id in call.get("model_review_record_ids", [])
            if record_id in review_index
        ]
        review_payloads = [record.get("content") for record in review_records]
        state_paths = _holistic_state_paths(
            [call.get("tool_results", []), *review_payloads]
        )
        for record in review_records:
            record_call_id = record.get("call_id")
            if isinstance(record_call_id, str):
                state_paths.extend(raw_state_paths_by_call.get(record_call_id, ()))
        for unresolved in dict.fromkeys(state_paths):
            try:
                state_path = unresolved.expanduser().resolve(strict=True)
            except OSError:
                continue
            if state_path.is_symlink() or not state_path.is_file():
                continue
            try:
                prior = _read_json(state_path, "referenced prior analysis state")
            except CreditAnalysisError:
                continue
            if prior.get("schema") != HOLISTIC_STATE_SCHEMA:
                continue
            analysis_id = prior.get("analysis_id")
            if not isinstance(analysis_id, str) or analysis_id == current_analysis_id:
                continue
            analysis_call_ids.add(call_id)
            if analysis_id in seen_analyses:
                continue
            seen_analyses.add(analysis_id)
            tasks: list[dict[str, Any]] = []
            execution = prior.get("execution")
            order = prior.get("task_order")
            if isinstance(execution, Mapping) and isinstance(order, list):
                for task_id in order:
                    task_state = execution.get(task_id)
                    if (
                        not isinstance(task_id, str)
                        or not isinstance(task_state, Mapping)
                    ):
                        continue
                    attempts: list[dict[str, Any]] = []
                    for attempt in task_state.get("attempts", []):
                        if not isinstance(attempt, Mapping):
                            continue
                        artifacts = attempt.get("artifacts")
                        prompt_projection = None
                        result_projection = None
                        luna_event_stream = None
                        if isinstance(artifacts, Mapping):
                            prompt_artifact = artifacts.get("prompt")
                            if isinstance(prompt_artifact, Mapping):
                                prompt_path = pathlib.Path(
                                    str(prompt_artifact.get("path", ""))
                                )
                                if (
                                    prompt_path.is_file()
                                    and not prompt_path.is_symlink()
                                ):
                                    prompt_projection = _holistic_projection(
                                        prompt_path.read_text(encoding="utf-8"),
                                        limit=text_limit,
                                        surface_ids=surface_ids,
                                    )
                            output_artifact = artifacts.get("raw_output")
                            if isinstance(output_artifact, Mapping):
                                output_path = pathlib.Path(
                                    str(output_artifact.get("path", ""))
                                )
                                if (
                                    output_path.is_file()
                                    and not output_path.is_symlink()
                                ):
                                    result_projection = _holistic_projection(
                                        output_path.read_text(encoding="utf-8"),
                                        limit=text_limit,
                                        surface_ids=surface_ids,
                                    )
                            if task_id.startswith("luna."):
                                luna_event_stream = _retained_text_projection(
                                    artifacts.get("events"),
                                    limit=text_limit,
                                    surface_ids=surface_ids,
                                )
                        attempts.append(
                            {
                                "attempt_number": attempt.get("attempt_number"),
                                "model": attempt.get("model"),
                                "reasoning_effort": attempt.get("reasoning_effort"),
                                "duration_ms": attempt.get("duration_ms"),
                                "exit_code": attempt.get("exit_code"),
                                "timed_out": attempt.get("timed_out"),
                                "terminated": attempt.get("terminated"),
                                "error": attempt.get("error"),
                                "event_summary": attempt.get("event_summary"),
                                "prompt": prompt_projection,
                                "result": result_projection,
                                "luna_event_stream": luna_event_stream,
                            }
                        )
                    tasks.append(
                        {
                            "task_id": task_id,
                            "status": task_state.get("status"),
                            "result_identity": task_state.get("result"),
                            "attempts": attempts,
                        }
                    )
            activities.append(
                {
                    "analysis_id": analysis_id,
                    "source_call_id": call_id,
                    "state_sha256": _file_hash(state_path),
                    "phase": prior.get("phase"),
                    "model_calls": prior.get("model_calls"),
                    "model_attempts": prior.get("model_attempts"),
                    "tasks": tasks,
                    "evidence_ref": f"analysis://{analysis_id}",
                }
            )
    return activities, analysis_call_ids


__all__ = (
    "OUTCOME_KEYS",
    "SURFACE_EVIDENCE_KEYWORDS",
    "_holistic_prior_analysis_activity",
    "_holistic_projection",
    "_holistic_raw_state_paths_by_call",
    "_holistic_state_paths",
    "_relevant_segments",
    "_review_record_index",
    "_shared_relevant_segments",
    "_structured_outcome",
)
