"""Pure capacity planning for the holistic credit-analysis controller.

This module owns byte-bounded run partitioning, Luna admission priority,
flexible Luna result allowances, and measured Sol report packing.  It never
reads sessions, launches models, or mutates controller state.  Calls remain
attached to their source run; transport parts are an input-capacity mechanism,
not independent semantic runs.
"""
# ruff: noqa: F401,F403,F405,I001

from __future__ import annotations

from typing import Callable

from .single_thread_analysis import *


def _capacity_json_bytes(value: Any) -> int:
    """Return the exact compact UTF-8 JSON size used by model inputs."""

    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
    )


def _capacity_episode_for_calls(
    episode: Mapping[str, Any], calls: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Retain only the run messages referenced by one ordered call group."""

    message_ids = {
        str(message_id)
        for call in calls
        for message_id in call.get("user_message_ids", [])
    }
    return {
        **episode,
        "candidate_ids": [str(call["candidate_id"]) for call in calls],
        "user_messages": [
            message
            for message in episode.get("user_messages", [])
            if str(message.get("message_id")) in message_ids
        ],
        "calls": [dict(call) for call in calls],
    }


def partition_luna_inputs(
    *,
    analysis_id: str,
    episodes: Sequence[Mapping[str, Any]],
    bundle: Mapping[str, Any],
    budget_bytes: int,
    payload_builder: Callable[..., Mapping[str, Any]],
    record_fitter: Callable[[Mapping[str, Any], int], Mapping[str, Any]],
) -> list[list[dict[str, Any]]]:
    """Divide oversized runs into the minimum fitting ordered input parts.

    A normal run remains one part.  An oversized run is split only between its
    ordered call records.  If one complete compact record is still oversized,
    ``record_fitter`` deterministically reduces that record's evidence detail
    while preserving its run, call, candidate, and evidence identities.
    """

    fragments: list[dict[str, Any]] = []

    def payload_for(fragment: Mapping[str, Any]) -> Mapping[str, Any]:
        return payload_builder(
            analysis_id=analysis_id,
            task_id="luna.discovery.0001",
            ordinal=1,
            episodes=[fragment],
            bundle=bundle,
        )

    for source_episode in episodes:
        # Include the largest possible part counters while measuring.  The final
        # counters can only be the same size or smaller, so metadata added after
        # partitioning cannot turn an admitted part into an overflow.
        maximum_part_index = max(1, len(source_episode.get("calls", [])))
        episode = {
            **source_episode,
            "episode_fragment": maximum_part_index,
            "episode_fragment_count": maximum_part_index,
            "run_window_ordinal": maximum_part_index,
            "run_window_count": maximum_part_index,
        }
        if _capacity_json_bytes(payload_for(episode)) <= budget_bytes:
            fragments.append(episode)
            continue
        current: list[Mapping[str, Any]] = []
        for source_call in episode["calls"]:
            call = dict(source_call)
            proposed = _capacity_episode_for_calls(episode, [*current, call])
            if current and _capacity_json_bytes(payload_for(proposed)) > budget_bytes:
                fragments.append(_capacity_episode_for_calls(episode, current))
                current = [call]
            else:
                current = [*current, call]
            singleton = _capacity_episode_for_calls(episode, current)
            if len(current) == 1 and _capacity_json_bytes(payload_for(singleton)) > budget_bytes:
                fitted = dict(record_fitter(call, budget_bytes))
                singleton = _capacity_episode_for_calls(episode, [fitted])
                if _capacity_json_bytes(payload_for(singleton)) > budget_bytes:
                    raise CreditAnalysisError(
                        "one reduced run part exceeds Luna's proven input envelope"
                    )
                current = [fitted]
        if current:
            fragments.append(_capacity_episode_for_calls(episode, current))

    counts = Counter(str(fragment["turn_id"]) for fragment in fragments)
    seen: Counter[str] = Counter()
    normalized: list[dict[str, Any]] = []
    for fragment in fragments:
        turn_id = str(fragment["turn_id"])
        seen[turn_id] += 1
        normalized.append(
            {
                **fragment,
                "episode_fragment": seen[turn_id],
                "episode_fragment_count": counts[turn_id],
                "run_window_ordinal": seen[turn_id],
                "run_window_count": counts[turn_id],
            }
        )
    packets = [[fragment] for fragment in normalized]
    if not packets:
        raise CreditAnalysisError("holistic Luna plan is empty")
    observed = [
        candidate
        for packet in packets
        for episode in packet
        for candidate in episode["candidate_ids"]
    ]
    expected = list(bundle["candidate_ids"])
    if observed != expected or len(observed) != len(set(observed)):
        raise CreditAnalysisError("holistic Luna run-part plan changed call coverage")
    if any(
        _capacity_json_bytes(payload_for(packet[0])) > budget_bytes
        for packet in packets
    ):
        raise CreditAnalysisError("holistic Luna run-part plan exceeds capacity")
    return packets


def select_luna_tasks(
    tasks: Sequence[Mapping[str, Any]], *, maximum_attempts: int
) -> set[str]:
    """Select fitting run parts by largest-run/immediate-successor priority."""

    fitting = [dict(task) for task in tasks if not task.get("capacity_omitted", False)]
    if len(fitting) <= maximum_attempts:
        return {str(task["task_id"]) for task in fitting}
    tasks_by_run: dict[str, list[dict[str, Any]]] = defaultdict(list)
    run_order: list[str] = []
    for task in fitting:
        turn_id = str(task["turn_id"])
        if turn_id not in tasks_by_run:
            run_order.append(turn_id)
        tasks_by_run[turn_id].append(task)
    for run_tasks in tasks_by_run.values():
        run_tasks.sort(key=lambda task: int(task["run_window_ordinal"]))
    ranked_runs = sorted(
        run_order,
        key=lambda turn_id: (
            -sum(int(task.get("evidence_bytes") or task["input_bytes"]) for task in tasks_by_run[turn_id]),
            run_order.index(turn_id),
        ),
    )
    priority: list[dict[str, Any]] = []
    queued: set[str] = set()
    for anchor in ranked_runs:
        anchor_index = run_order.index(anchor)
        bundle_runs = [anchor]
        if anchor_index + 1 < len(run_order):
            bundle_runs.append(run_order[anchor_index + 1])
        for turn_id in bundle_runs:
            first = tasks_by_run[turn_id][0]
            if str(first["task_id"]) not in queued:
                priority.append(first)
                queued.add(str(first["task_id"]))
        for turn_id in bundle_runs:
            for task in tasks_by_run[turn_id][1:]:
                task_id = str(task["task_id"])
                if task_id not in queued:
                    priority.append(task)
                    queued.add(task_id)
    for task in fitting:
        task_id = str(task["task_id"])
        if task_id not in queued:
            priority.append(task)
            queued.add(task_id)
    return {
        str(task["task_id"])
        for task in priority[:maximum_attempts]
    }


def luna_output_allowance(
    *,
    admitted_tasks: int,
    sol_reviewer_capacity_bytes: int,
    maximum_reviewers: int,
    per_report_framing_bytes: int = 1_000,
) -> int:
    """Compute one safe uniform Luna result allowance for downstream Sol."""

    if admitted_tasks < 1 or maximum_reviewers < 1:
        raise CreditAnalysisError("Luna output allocation requires admitted tasks")
    reviewer_count = min(maximum_reviewers, admitted_tasks)
    reports_per_reviewer = math.ceil(admitted_tasks / reviewer_count)
    usable = (
        sol_reviewer_capacity_bytes
        - reports_per_reviewer * per_report_framing_bytes
    )
    allowance = usable // reports_per_reviewer
    if allowance < 1_000:
        raise CreditAnalysisError(
            "accepted Luna reports cannot fit the proven Sol reviewer envelope"
        )
    return min(64_000, allowance)


def pack_report_groups(
    groups: Sequence[Mapping[str, Any]],
    *,
    bin_count: int,
    capacity_bytes: int,
    allow_omissions: bool,
) -> tuple[list[list[dict[str, Any]]], list[dict[str, Any]]] | None:
    """Best-fit measured Luna report groups across fixed Sol reviewers."""

    bins: list[list[dict[str, Any]]] = [[] for _ in range(bin_count)]
    loads = [0] * bin_count
    omitted: list[dict[str, Any]] = []
    ordered = sorted(
        (dict(group) for group in groups),
        key=lambda group: (
            -int(group["routing_bytes"]),
            int(group["run_ordinal"]),
            int(group["run_window_ordinal"]),
        ),
    )
    for group in ordered:
        size = int(group["routing_bytes"])
        choices = [
            index
            for index in range(bin_count)
            if loads[index] + size <= capacity_bytes
        ]
        if not choices:
            if not allow_omissions:
                return None
            omitted.append(group)
            continue
        selected = min(choices, key=lambda index: (loads[index], index))
        bins[selected].append(group)
        loads[selected] += size
    for group_bin in bins:
        group_bin.sort(
            key=lambda group: (
                int(group["run_ordinal"]),
                int(group["run_window_ordinal"]),
            )
        )
    omitted.sort(
        key=lambda group: (
            int(group["run_ordinal"]),
            int(group["run_window_ordinal"]),
        )
    )
    return bins, omitted


__all__ = (
    "luna_output_allowance",
    "pack_report_groups",
    "partition_luna_inputs",
    "select_luna_tasks",
)
