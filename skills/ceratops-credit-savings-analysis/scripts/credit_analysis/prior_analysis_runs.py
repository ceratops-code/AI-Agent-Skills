"""Deterministic projections and descendant-source lineage handling.

This module owns bounded semantic projections, discovery of explicitly
referenced orchestration state, and normalization of retained child sessions as
ordinary source runs. Controller state resolves identity, provenance, and
attribution only; retained prompts, results, and event excerpts are never copied
into shared model inputs.
"""
# ruff: noqa: F401,F403,F405,I001

from __future__ import annotations

from .single_thread_analysis import *


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


def _holistic_prior_analysis_sources(
    evidence: Mapping[str, Any],
    *,
    current_analysis_id: str,
    raw_state_paths_by_call: Mapping[str, Sequence[pathlib.Path]],
) -> tuple[list[dict[str, Any]], set[str]]:
    """Resolve earlier controller descendants without copying their artifacts."""

    sources: list[dict[str, Any]] = []
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
            descendants: list[dict[str, Any]] = []
            seen_sessions: set[str] = set()
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
                    for attempt in task_state.get("attempts", []):
                        if not isinstance(attempt, Mapping):
                            continue
                        summary = attempt.get("event_summary")
                        child_ids = (
                            summary.get("child_session_ids", [])
                            if isinstance(summary, Mapping)
                            else []
                        )
                        if not isinstance(child_ids, list):
                            continue
                        for session_id in child_ids:
                            if (
                                not isinstance(session_id, str)
                                or not session_id
                                or session_id in seen_sessions
                            ):
                                continue
                            seen_sessions.add(session_id)
                            descendants.append(
                                {
                                    "session_id": session_id,
                                    "task_id": task_id,
                                    "attempt_number": attempt.get("attempt_number"),
                                    "model": attempt.get("model"),
                                    "phase": attempt.get("phase") or task_state.get("phase"),
                                    "execution_cwd": attempt.get("execution_cwd"),
                                    "ephemeral": bool(attempt.get("ephemeral")),
                                }
                            )
            for child in prior.get("child_lineage", []):
                if not isinstance(child, Mapping):
                    continue
                child_ids = child.get("child_session_ids", [])
                if not isinstance(child_ids, list):
                    continue
                for session_id in child_ids:
                    if (
                        not isinstance(session_id, str)
                        or not session_id
                        or session_id in seen_sessions
                    ):
                        continue
                    seen_sessions.add(session_id)
                    descendants.append(
                        {
                            "session_id": session_id,
                            "task_id": child.get("task_id"),
                            "attempt_number": child.get("attempt_number"),
                            "model": None,
                            "phase": None,
                            "execution_cwd": child.get("execution_cwd"),
                            "ephemeral": bool(child.get("ephemeral")),
                        }
                    )
            sources.append(
                {
                    "analysis_id": analysis_id,
                    "source_call_id": call_id,
                    "state_sha256": _file_hash(state_path),
                    "descendants": descendants,
                }
            )
    return sources, analysis_call_ids


def _namespace_descendant_evidence(
    evidence: Mapping[str, Any],
    *,
    session_id: str,
    analysis_id: str,
    source_cwd: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Give one child session collision-free ordinary-run identities."""

    value = json.loads(json.dumps(evidence, ensure_ascii=False, default=str))
    prefix = f"thread.{hashlib.sha256(session_id.encode('utf-8')).hexdigest()[:12]}"
    turn_ids = {
        str(run["turn_id"]): f"{prefix}:{run['turn_id']}"
        for run in value.get("runs", [])
    }
    message_ids = {
        str(message["message_id"]): f"{prefix}:{message['message_id']}"
        for run in value.get("runs", [])
        for message in run.get("user_messages", [])
    }
    call_ids = {
        str(call["call_id"]): f"{prefix}:{call['call_id']}"
        for run in value.get("runs", [])
        for call in run.get("calls", [])
    }
    review_ids = {
        str(record["record_id"]): f"{prefix}:{record['record_id']}"
        for record in value.get("model_review", {}).get("records", [])
    }
    for run in value.get("runs", []):
        original_turn_id = str(run["turn_id"])
        run["turn_id"] = turn_ids[original_turn_id]
        run["source_session_id"] = session_id
        run["source_analysis_id"] = analysis_id
        run["source_cwd"] = source_cwd
        for message in run.get("user_messages", []):
            message["message_id"] = message_ids[str(message["message_id"])]
        for call in run.get("calls", []):
            call["call_id"] = call_ids[str(call["call_id"])]
            call["turn_id"] = turn_ids[str(call["turn_id"])]
            call["user_message_ids"] = [
                message_ids[str(message_id)]
                for message_id in call.get("user_message_ids", [])
            ]
            call["model_review_record_ids"] = [
                review_ids[str(record_id)]
                for record_id in call.get("model_review_record_ids", [])
            ]
    model_review = value.get("model_review", {})
    for record in model_review.get("records", []):
        record["record_id"] = review_ids[str(record["record_id"])]
        if record.get("turn_id") is not None:
            record["turn_id"] = turn_ids[str(record["turn_id"])]
    model_review["global_record_ids"] = [
        review_ids[str(record_id)]
        for record_id in model_review.get("global_record_ids", [])
    ]
    model_review["call_record_ids"] = {
        turn_ids[str(turn_id)]: {
            str(index): [review_ids[str(record_id)] for record_id in record_ids]
            for index, record_ids in calls.items()
        }
        for turn_id, calls in model_review.get("call_record_ids", {}).items()
    }
    value["call_inventory"] = [
        call_ids[str(call_id)] for call_id in value.get("call_inventory", [])
    ]
    coverage = value.get("semantic_coverage", {})
    coverage["run_ids"] = [
        turn_ids[str(turn_id)] for turn_id in coverage.get("run_ids", [])
    ]
    value["thread_source"] = {
        "session_id": session_id,
        "analysis_id": analysis_id,
        "source_cwd": source_cwd,
    }
    return value, turn_ids


def _merge_numeric_totals(values: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate deterministic usage totals across independently read sessions."""

    percentage_keys = {
        "input_of_total_pct",
        "cache_rate_pct",
        "output_of_total_pct",
        "reasoning_of_output_pct",
    }
    result: dict[str, Any] = {}
    for key in values[0]:
        if key in percentage_keys:
            continue
        items = [value.get(key) for value in values]
        if all(item is None for item in items):
            result[key] = None
        elif all(
            item is None or isinstance(item, (int, float)) and not isinstance(item, bool)
            for item in items
        ):
            result[key] = sum(item for item in items if item is not None)
        else:
            result[key] = items[0]
    input_tokens = int(result.get("input_tokens") or 0)
    cached_tokens = int(result.get("cached_input_tokens") or 0)
    output_tokens = int(result.get("output_tokens") or 0)
    reasoning_tokens = int(result.get("reasoning_output_tokens") or 0)
    total_tokens = int(result.get("total_tokens") or input_tokens + output_tokens)
    result.update(
        {
            "input_of_total_pct": round(100 * input_tokens / total_tokens, 2)
            if total_tokens
            else 0.0,
            "cache_rate_pct": round(100 * cached_tokens / input_tokens, 2)
            if input_tokens
            else 0.0,
            "output_of_total_pct": round(100 * output_tokens / total_tokens, 2)
            if total_tokens
            else 0.0,
            "reasoning_of_output_pct": round(100 * reasoning_tokens / output_tokens, 2)
            if output_tokens
            else 0.0,
        }
    )
    return result


def _merge_thread_evidence(
    primary: Mapping[str, Any],
    descendants: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Merge namespaced child sessions into one ordinary frozen run inventory."""

    merged = json.loads(json.dumps(primary, ensure_ascii=False, default=str))
    if not descendants:
        return merged
    all_values = [merged, *descendants]
    merged["runs"] = [run for value in all_values for run in value.get("runs", [])]
    merged["call_inventory"] = [
        call_id for value in all_values for call_id in value.get("call_inventory", [])
    ]
    merged["collection"] = {
        key: sum(int(value.get("collection", {}).get(key) or 0) for value in all_values)
        for key in (
            "session_reads",
            "completed_runs",
            "model_calls",
            "user_messages",
            "model_review_records",
        )
    }
    merged["semantic_coverage"] = {
        "mode": "complete",
        "threshold_percent": 100,
        "run_ids": [str(run["turn_id"]) for run in merged["runs"]],
        "covered_calls": len(merged["call_inventory"]),
        "total_calls": len(merged["call_inventory"]),
        "covered_percent": 100.0,
    }
    merged["totals"] = _merge_numeric_totals(
        [value["totals"] for value in all_values]
    )
    repeated: dict[tuple[str, str], dict[str, Any]] = {}
    for value in all_values:
        for group in value.get("repeated_tool_calls", []):
            key = (str(group.get("name")), str(group.get("fingerprint")))
            if key not in repeated:
                repeated[key] = dict(group)
            else:
                repeated[key]["count"] = int(repeated[key].get("count") or 0) + int(
                    group.get("count") or 0
                )
    merged["repeated_tool_calls"] = list(repeated.values())
    reviews = [value["model_review"] for value in all_values]
    merged_review = merged["model_review"]
    merged_review["records"] = [
        record for review in reviews for record in review.get("records", [])
    ]
    merged_review["global_record_ids"] = [
        record_id
        for review in reviews
        for record_id in review.get("global_record_ids", [])
    ]
    merged_review["call_record_ids"] = {
        str(turn_id): calls
        for review in reviews
        for turn_id, calls in review.get("call_record_ids", {}).items()
    }
    canonical: dict[str, Any] = {}
    for review in reviews:
        for item in review.get("canonical_path_references", []):
            canonical.setdefault(
                json.dumps(item, sort_keys=True, separators=(",", ":")), item
            )
    merged_review["canonical_path_references"] = list(canonical.values())
    merged["source_fingerprint"] = _content_hash(
        [value.get("source_fingerprint") for value in all_values]
    )
    merged["window_fingerprint"] = _content_hash(
        [value.get("window_fingerprint") for value in all_values]
    )
    return merged


__all__ = (
    "OUTCOME_KEYS",
    "SURFACE_EVIDENCE_KEYWORDS",
    "_holistic_prior_analysis_sources",
    "_holistic_projection",
    "_holistic_raw_state_paths_by_call",
    "_holistic_state_paths",
    "_merge_thread_evidence",
    "_namespace_descendant_evidence",
    "_relevant_segments",
    "_review_record_index",
    "_shared_relevant_segments",
    "_structured_outcome",
)
