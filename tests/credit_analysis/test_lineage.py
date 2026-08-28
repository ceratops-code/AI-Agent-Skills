from __future__ import annotations

import json
import pathlib

from tests.credit_analysis.models import (
    FakeCreditModelRunner,
    load_credit_analysis_workflow_module,
)
from tests.credit_analysis.paths import (
    CREDIT_ANALYSIS_CONTRACT,
)
from tests.credit_analysis.sessions import (
    _attach_prior_analysis_state,
    credit_analysis_request,
    finding_record,
    indexed_credit_analysis_session,
    surface_result_record,
    write_json_file,
)
from tests.credit_analysis.workflow import run_credit_analysis_workflow


def test_credit_analysis_lineage_allows_later_meta_analysis_without_recursion(
    tmp_path: pathlib.Path,
    monkeypatch,
) -> None:
    workflow = load_credit_analysis_workflow_module()
    a_root = tmp_path / "a"
    b_root = tmp_path / "b"
    a_root.mkdir()
    b_root.mkdir()
    request_a, _, _ = credit_analysis_request(
        a_root,
        extra_completed_turns=1,
        extra_calls_per_turn=2,
    )
    runner_a = FakeCreditModelRunner(temporary_controls=False)
    plan_a = workflow.command_plan_orchestration(
        request_a,
        available_models=runner_a.available_models,
    )
    complete_a = workflow.command_execute_orchestration(
        pathlib.Path(plan_a["state_path"]),
        runner=runner_a,
        available_models=runner_a.available_models,
    )
    assert complete_a["complete"] is True

    codex_home = tmp_path / "codex-home"
    luna_thread_id = "019a0000-0000-7000-8000-000000000001"
    sol_thread_id = "019a0000-0000-7000-8000-000000000002"
    indexed_credit_analysis_session(
        codex_home,
        thread_id=luna_thread_id,
        thread_name="retained Luna child",
        updated_at="2026-08-01T00:00:01Z",
        project_name="retained-luna",
    )
    indexed_credit_analysis_session(
        codex_home,
        thread_id=sol_thread_id,
        thread_name="retained Sol child",
        updated_at="2026-08-01T00:00:02Z",
        project_name="retained-sol",
    )
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    prior_state_path = pathlib.Path(plan_a["state_path"])
    state_a = json.loads(prior_state_path.read_text(encoding="utf-8"))
    luna_task_id = next(
        task_id for task_id in state_a["task_order"] if task_id.startswith("luna.")
    )
    sol_task_id = next(
        task_id
        for task_id in state_a["task_order"]
        if task_id.startswith("sol.adjudication.")
        and state_a["execution"][task_id]["status"] == "complete"
    )
    for task_id, thread_id in (
        (luna_task_id, luna_thread_id),
        (sol_task_id, sol_thread_id),
    ):
        attempt = state_a["execution"][task_id]["attempts"][0]
        attempt["ephemeral"] = False
        attempt["event_summary"]["child_session_ids"] = [thread_id]
    write_json_file(prior_state_path, state_a)

    request_b, session_b, _ = credit_analysis_request(
        b_root,
        extra_completed_turns=1,
        extra_calls_per_turn=2,
    )
    _attach_prior_analysis_state(session_b, prior_state_path)
    raw_rows = [
        json.loads(line)
        for line in session_b.read_text(encoding="utf-8").splitlines()
    ]
    raw_state_paths = workflow.command_plan_orchestration.__globals__[
        "_holistic_raw_state_paths_by_call"
    ](raw_rows)
    assert raw_state_paths["read-1"] == [prior_state_path]
    assert raw_state_paths["read-2"] == [prior_state_path]
    runner_b = FakeCreditModelRunner(temporary_controls=False)
    plan_b = workflow.command_plan_orchestration(
        request_b,
        available_models=runner_b.available_models,
    )
    evidence_b = json.loads(
        pathlib.Path(plan_b["evidence_path"]).read_text(encoding="utf-8")
    )
    assert evidence_b["analysis_lineage"]["included_prior_analysis_ids"] == [
        plan_a["analysis_id"]
    ]
    assert evidence_b["analysis_lineage"]["source_selection_uses_prompt_markers"] is False
    assert evidence_b["analysis_lineage"]["included_session_reads"] == 3
    assert {
        item["session_id"]
        for item in evidence_b["analysis_lineage"]["included_descendant_sessions"]
    } == {luna_thread_id, sol_thread_id}
    assert evidence_b["analysis_lineage"]["unresolved_descendant_sessions"] == []
    assert "analysis_generated_activity" not in evidence_b
    assert "luna_event_stream" not in json.dumps(evidence_b)
    descendant_runs = [
        run for run in evidence_b["runs"] if str(run["turn_id"]).startswith("thread.")
    ]
    assert len(descendant_runs) == 6
    assert {run["source_analysis_id"] for run in descendant_runs} == {
        plan_a["analysis_id"]
    }
    manifest_b = json.loads(
        pathlib.Path(plan_b["manifest_path"]).read_text(encoding="utf-8")
    )
    compact_b = json.loads(
        pathlib.Path(manifest_b["compact_evidence"]["path"]).read_text(
            encoding="utf-8"
        )
    )
    analysis_records = [
        record
        for record in compact_b["records"]
        if record["workstream"] == "analysis-overhead"
    ]
    assert len(analysis_records) >= 2
    assert all(
        record["candidate_id"] in manifest_b["candidate_ids"]
        for record in analysis_records
    )

    complete_b = workflow.command_execute_orchestration(
        pathlib.Path(plan_b["state_path"]),
        runner=runner_b,
        available_models=runner_b.available_models,
    )
    final_b = json.loads(
        pathlib.Path(complete_b["final_result_path"]).read_text(encoding="utf-8")
    )
    assert final_b["lineage"]["included_prior_analysis_ids"] == [
        plan_a["analysis_id"]
    ]
    assert all(
        child["analysis_id"] == plan_b["analysis_id"]
        for child in final_b["lineage"]["created_child_tasks"]
    )
    assert final_b["lineage"]["excluded_own_descendant_task_ids"] == [
        child["task_id"] for child in final_b["lineage"]["created_child_tasks"]
    ]
    analysis_totals = final_b["workstream_classification_totals"][
        "analysis-overhead"
    ]
    assert sum(analysis_totals.values()) == len(analysis_records)

    unavailable_thread_id = "019a0000-0000-7000-8000-000000000003"
    state_a["execution"][luna_task_id]["attempts"][0]["event_summary"][
        "child_session_ids"
    ].append(unavailable_thread_id)
    write_json_file(prior_state_path, state_a)
    c_root = tmp_path / "c"
    c_root.mkdir()
    request_c, session_c, _ = credit_analysis_request(
        c_root,
        extra_completed_turns=1,
        extra_calls_per_turn=2,
    )
    _attach_prior_analysis_state(session_c, prior_state_path)
    plan_c = workflow.command_plan_orchestration(
        request_c,
        available_models=runner_b.available_models,
    )
    evidence_c = json.loads(
        pathlib.Path(plan_c["evidence_path"]).read_text(encoding="utf-8")
    )
    unresolved = evidence_c["analysis_lineage"]["unresolved_descendant_sessions"]
    assert any(
        item["session_id"] == unavailable_thread_id
        and item["reason"] == "session-unavailable"
        for item in unresolved
    )
    assert "analysis_generated_activity" not in evidence_c


def test_credit_analysis_workflow_standalone_zero_findings_is_isolated(
    tmp_path: pathlib.Path,
) -> None:
    request, _, task_root = credit_analysis_request(
        tmp_path,
        action="context-evidence",
    )
    pricing = tmp_path / "pricing.json"
    write_json_file(
        pricing,
        {
            "schema": "ceratops-model-call-pricing-profile.v1",
            "input_per_million_tokens": 1.0,
            "cached_input_per_million_tokens": 0.5,
            "output_per_million_tokens": 2.0,
            "mode_multiplier": 1.0,
        },
    )
    request_value = json.loads(request.read_text(encoding="utf-8"))
    request_value["pricing_profile"] = str(pricing)
    write_json_file(request, request_value)
    prepared = run_credit_analysis_workflow("prepare", "--request", str(request))
    assert prepared.returncode == 0, prepared.stderr
    status = json.loads(prepared.stdout)
    assert status["pending_surface"] == "context-evidence"
    evidence = json.loads(pathlib.Path(status["evidence_path"]).read_text(encoding="utf-8"))
    context = json.loads(pathlib.Path(status["context_path"]).read_text(encoding="utf-8"))
    result = surface_result_record(
        status,
        context,
        evidence["evidence_fingerprint"],
    )
    result_path = pathlib.Path(status["required_result_path"])
    incomplete = {**result, "dismissed_candidates": []}
    write_json_file(result_path, incomplete)
    rejected = run_credit_analysis_workflow(
        "advance",
        "--state",
        status["state_path"],
        "--result",
        str(result_path),
    )
    assert rejected.returncode == 2
    assert "zero-finding" in rejected.stderr or "not accounted" in rejected.stderr

    write_json_file(result_path, result)
    write_json_file(task_root / "findings" / "001-context-evidence.json", result)
    advanced = run_credit_analysis_workflow(
        "advance",
        "--state",
        status["state_path"],
        "--result",
        str(result_path),
    )
    assert advanced.returncode == 0, advanced.stderr
    ready = json.loads(advanced.stdout)
    assert ready["pending_surface"] is None
    assert ready["ready_to_finalize"] is True
    state = json.loads(pathlib.Path(status["state_path"]).read_text(encoding="utf-8"))
    assert state["queue"] == ["context-evidence"]
    assert [record["surface_id"] for record in state["completed"]] == [
        "context-evidence"
    ]
    finalized = run_credit_analysis_workflow(
        "finalize",
        "--state",
        status["state_path"],
        "--result",
        ready["required_result_path"],
    )
    assert finalized.returncode == 0, finalized.stderr
    final_state = json.loads(pathlib.Path(status["state_path"]).read_text(encoding="utf-8"))
    final_result = json.loads(
        pathlib.Path(final_state["final_result"]["path"]).read_text(encoding="utf-8")
    )
    assert final_result["mode"] == "standalone"
    assert "not a whole-thread credit reconciliation" in final_result[
        "scope_limitation"
    ]
    assert final_result["confirmed_findings"] == []
    assert final_result["pricing"]["provided"] is True
    assert final_result["priced_cost"] == {
        "total": 7.8e-05,
        "selected_surface_observed_avoidable": 0.0,
    }
    assert not (task_root / "context").exists()
    assert not (task_root / "pending").exists()

    contract = json.loads(CREDIT_ANALYSIS_CONTRACT.read_text(encoding="utf-8"))
    public_actions = [item["id"] for item in contract["public_actions"]]
    assert "synthesis" not in public_actions
    assert "batch-summary" not in public_actions
    assert contract["internal_phases"] == [
        {"id": "synthesis", "public": False},
        {"id": "batch-summary", "public": False},
    ]
    rejected_root = tmp_path / "analysis-synthesis"
    rejected_root.mkdir()
    rejected_request = tmp_path / "request-synthesis.json"
    write_json_file(
        rejected_request,
        {
            **json.loads(request.read_text(encoding="utf-8")),
            "action": "synthesis",
            "mode": "standalone",
            "task_temp_root": str(rejected_root),
            "evidence_output": str(rejected_root / "evidence.json"),
        },
    )
    rejected_synthesis = run_credit_analysis_workflow(
        "prepare", "--request", str(rejected_request)
    )
    assert rejected_synthesis.returncode == 2
    assert "action is not public" in rejected_synthesis.stderr

    volume_base = tmp_path / "volume"
    volume_base.mkdir()
    volume_request, _, _ = credit_analysis_request(
        volume_base,
        action="tool-flow",
    )
    volume_prepared = run_credit_analysis_workflow(
        "prepare", "--request", str(volume_request)
    )
    assert volume_prepared.returncode == 0, volume_prepared.stderr
    volume_status = json.loads(volume_prepared.stdout)
    volume_evidence = json.loads(
        pathlib.Path(volume_status["evidence_path"]).read_text(encoding="utf-8")
    )
    volume_context = json.loads(
        pathlib.Path(volume_status["context_path"]).read_text(encoding="utf-8")
    )
    volume_finding = finding_record(
        "oversized-output",
        [volume_evidence["call_inventory"][0]],
        producer_type="tool-choice",
        owner="synthetic command",
        waste_kind="context-volume",
        complexity="Minimal",
    )
    volume_result = surface_result_record(
        volume_status,
        volume_context,
        volume_evidence["evidence_fingerprint"],
        findings=[volume_finding],
    )
    write_json_file(
        pathlib.Path(volume_status["required_result_path"]), volume_result
    )
    volume_advanced = run_credit_analysis_workflow(
        "advance",
        "--state",
        volume_status["state_path"],
        "--result",
        volume_status["required_result_path"],
    )
    assert volume_advanced.returncode == 0, volume_advanced.stderr
    volume_ready = json.loads(volume_advanced.stdout)
    volume_finalized = run_credit_analysis_workflow(
        "finalize",
        "--state",
        volume_status["state_path"],
        "--result",
        volume_ready["required_result_path"],
    )
    assert volume_finalized.returncode == 0, volume_finalized.stderr
    volume_state = json.loads(
        pathlib.Path(volume_status["state_path"]).read_text(encoding="utf-8")
    )
    volume_machine_result = json.loads(
        pathlib.Path(volume_state["final_result"]["path"]).read_text(
            encoding="utf-8"
        )
    )
    assert volume_machine_result["totals"]["surface_observed_avoidable_calls"] == 0
    assert volume_machine_result["confirmed_findings"][0][
        "deduplicated_avoidable_call_count"
    ] == 0
