from __future__ import annotations

import argparse
import json
import pathlib
import runpy
import sys
from typing import Any

import pytest

from tests.repository_lifecycle.support import (
    DEPLOY_OPERATION,
    RELEASE_OPERATION,
    SHIP_REPOSITORY,
    load_pr_workflow_module,
)
from tests.support.repositories import (
    run_git,
    write_sdlc_contract,
)


def _completed_batch(*results: dict[str, Any]) -> dict[str, Any]:
    operations = [str(result["operation"]) for result in results]
    return {
        "status": "completed",
        "completed_operations": operations,
        "pending_operations": [],
        "results": list(results),
    }


def _prepared_batch(*operations: str) -> dict[str, Any]:
    return {"status": "prepared", "operations": list(operations)}


def _failed_batch(
    failure: dict[str, Any],
    *,
    completed: tuple[dict[str, Any], ...] = (),
    pending: tuple[str, ...] = (),
) -> dict[str, Any]:
    failed_operation = str(failure["operation"])
    return {
        **failure,
        "status": "operation_failed",
        "completed_operations": [
            str(result["operation"]) for result in completed
        ],
        "pending_operations": [failed_operation, *pending],
        "results": [*completed, failure],
    }


@pytest.mark.parametrize(
    "metadata",
    [
        [],
        ["--title", "Complete Dev Tools catalog"],
        ["--body", "Collection policy.\n\nDeploy configuration.\n"],
        ["--title", "Caller title", "--body", "Exact description"],
        ["--body", ""],
    ],
)
def test_repository_ship_metadata_reaches_shared_pr_producer(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, metadata: list[str],
) -> None:
    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    ship = load_pr_workflow_module(monkeypatch, "ship")
    args = loaded["build_parser"]().parse_args(
        ["--repo-root", str(tmp_path), "--head-branch", "release/local", *metadata]
    )
    command = loaded["_ship_command"](args, tmp_path, None, "a" * 40)
    parsed = ship.build_parser().parse_args(command[4:])
    events: list[str] = []
    monkeypatch.setattr(ship.merge, "restore_unfinished_checkpoints", lambda root: None)
    monkeypatch.setattr(ship, "_repository_name", lambda *args: "example/repository")
    monkeypatch.setattr(ship, "_resolve_commit", lambda *args: "a" * 40)
    monkeypatch.setattr(ship, "_load_pending_work_scope", lambda *args: (None, None))
    monkeypatch.setattr(
        ship, "_load_or_create_checkpoint",
        lambda *args: (tmp_path / "checkpoint.json", {"phase": "prepared"}),
    )
    monkeypatch.setattr(ship, "_enforce_actions_availability", lambda *args: events.append("availability"))

    class ProducerReached(Exception):
        pass

    def ensure(arguments: argparse.Namespace) -> None:
        assert events == ["availability"]
        assert arguments.title == args.title
        assert arguments.body == args.body
        assert arguments.head_branch == "release/local"
        assert arguments.base_branch == "main"
        assert arguments.remote_name == "origin"
        events.append("producer")
        raise ProducerReached

    monkeypatch.setattr(ship.ensure_pr, "ensure_pr", ensure)
    with pytest.raises(ProducerReached):
        ship.ship(parsed)
    assert events == ["availability", "producer"]


@pytest.mark.parametrize("scope_present", [False, True])
def test_repository_ship_absent_default_contract_is_no_op_and_finalizes(
    tmp_path: pathlib.Path,
    scope_present: bool,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "version": 2,
                "target_branch": "release/local",
                "target_commit": "a" * 40,
                "sources": [
                    {
                        "branch": "selected",
                        "commit": "a" * 40,
                        "state": "retained",
                    }
                ],
            }
        ),
        encoding="utf-8",
        newline="\n",
    )
    shipped = {
        "status": "shipped",
        "repository": "example/repository",
        "commit": "a" * 40,
        "pr": 24,
        "url": "https://example.invalid/pull/24",
        "merge_commit": "c" * 40,
        "synchronized_head": "b" * 40,
    }
    prepared = {
        "status": "ready",
        "source_branches": [] if not scope_present else ["selected"],
        "pending_work_scope": str(scope) if scope_present else "",
        **({"target_commit": "a" * 40} if scope_present else {}),
    }
    responses: list[tuple[int, dict[str, Any]]] = [
        (0, prepared),
        (0, shipped),
    ]
    if scope_present:
        responses.extend(
            [
                (0, prepared),
                (0, {"status": "finalized"}),
            ]
        )
    commands: list[list[str]] = []

    def run_json(
        command: list[str], *, cwd: pathlib.Path | None = None
    ) -> tuple[int, dict[str, Any]]:
        if cwd is not None:
            assert cwd == repo
        commands.append(command)
        return responses[len(commands) - 1]

    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    review_request = tmp_path / "review-replies.json"
    parsed = loaded["build_parser"]().parse_args(
        [
            "--head-branch",
            "release/local",
            "--review-replies-request",
            str(review_request),
        ]
    )
    assert not hasattr(parsed, "pending_work_scope")
    assert not hasattr(parsed, "no_pending_work_check")
    assert parsed.repo is None
    assert parsed.review_replies_request == review_request
    inferred_repository_command = loaded["_ship_command"](
        parsed,
        repo,
        None,
        None,
    )
    assert "--repo" not in inferred_repository_command
    assert inferred_repository_command[
        inferred_repository_command.index("--repo-root") + 1
    ] == str(repo)
    ship_repository = loaded["ship_repository"]
    ship_repository.__globals__["_run_json"] = run_json
    ship_repository.__globals__["_branch_worktree"] = (
        lambda repo_root, branch: None
    )
    result = ship_repository(
        argparse.Namespace(
            repo_root=repo,
            repo="example/repository",
            head_branch="release/local",
            base_branch="main",
            remote_name="origin",
            commit=None if scope_present else "a" * 40,
            title=None,
            body=None,
            merge_method="merge",
            delete_branch=False,
            reusable_head=True,
            sdlc_contract=pathlib.Path("sdlc/sdlc.yml"),
            release_preflight_operation=["preflight"],
            release_operation=["publish"],
            deploy_operation=["deploy"],
            ci_wait_seconds=1,
            review_wait_seconds=1,
            review_replies_request=review_request,
            interval_seconds=1,
        )
    )

    assert result["release_publication"] == {
        "status": "completed",
        "completed_operations": ["publish"],
        "pending_operations": [],
        "results": [
            {
                "status": "no_op",
                "configured": False,
                "operation": "publish",
                "steps": [],
                "reason": "contract_not_configured",
            }
        ],
    }
    assert result["deployment"] == {
        "status": "completed",
        "completed_operations": ["deploy"],
        "pending_operations": [],
        "results": [
            {
                "status": "no_op",
                "configured": False,
                "operation": "deploy",
                "steps": [],
                "reason": "contract_not_configured",
            }
        ],
    }
    assert result["finalization"] == (
        {"status": "finalized"} if scope_present else None
    )
    assert "prepare" in commands[0]
    if scope_present:
        assert "--target-commit" not in commands[0]
    else:
        assert commands[0][-2:] == ["--target-commit", "a" * 40]
    assert commands[1][commands[1].index("--commit") + 1] == "a" * 40
    assert commands[1][commands[1].index("--review-replies-request") + 1] == str(
        review_request
    )
    if scope_present:
        assert len(commands) == 4
        assert "--pending-work-check" in commands[1]
        assert str(scope.resolve()) in commands[1]
        assert "check" in commands[2]
        assert "finalize" in commands[3]
    else:
        assert len(commands) == 2
        assert "--no-pending-work-check" in commands[1]
    deploy_runner = str(SHIP_REPOSITORY.parent / "run-deploy-operation.py")
    assert all(deploy_runner not in command for command in commands)

    blocker = {
        "status": "blocked",
        "message": "Codex review gate found one active thread.",
        "phase": "gates",
        "blocker": {
            "kind": "review_threads",
            "head_oid": "a" * 40,
            "threads": [{"thread_id": "PRRT_1", "body": "Fix this."}],
        },
    }
    blocked_responses: list[tuple[int, dict[str, Any]]] = [
        (
            0,
            {
                "status": "ready",
                "source_branches": [],
                "pending_work_scope": "",
            },
        ),
        (1, blocker),
    ]

    def blocked_run_json(
        command: list[str], *, cwd: pathlib.Path | None = None
    ) -> tuple[int, dict[str, Any]]:
        return blocked_responses.pop(0)

    ship_repository.__globals__["_run_json"] = blocked_run_json
    with pytest.raises(loaded["RepositoryShipError"]) as captured:
        ship_repository(
            argparse.Namespace(
                repo_root=repo,
                repo="example/repository",
                head_branch="release/local",
                base_branch="main",
                remote_name="origin",
                commit="a" * 40,
                title=None,
                body=None,
                merge_method="merge",
                delete_branch=False,
                reusable_head=True,
                sdlc_contract=pathlib.Path("sdlc/sdlc.yml"),
                release_preflight_operation=["preflight"],
                release_operation=["publish"],
                deploy_operation=["deploy"],
                ci_wait_seconds=1,
                review_wait_seconds=1,
                review_replies_request=None,
                interval_seconds=1,
            )
        )
    assert captured.value.payload == blocker


def test_repository_ship_missing_custom_contract_blocks_before_remote_mutation(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    ship_repository = loaded["ship_repository"]
    commands: list[list[str]] = []
    def unexpected_run(command: list[str]) -> tuple[int, dict[str, Any]]:
        commands.append(command)
        return 0, {}

    ship_repository.__globals__["_run_json"] = unexpected_run

    with pytest.raises(
        loaded["RepositoryShipError"],
        match="does not exist before shipping",
    ):
        ship_repository(
            argparse.Namespace(
                repo_root=repo,
                repo="example/repository",
                head_branch="release/local",
                base_branch="main",
                remote_name="origin",
                commit="a" * 40,
                title=None,
                body=None,
                merge_method="merge",
                delete_branch=False,
                reusable_head=False,
                sdlc_contract=pathlib.Path("sdlc/custom.yml"),
                release_preflight_operation=["preflight"],
                release_operation=["publish"],
                deploy_operation=["deploy"],
                ci_wait_seconds=1,
                review_wait_seconds=1,
                interval_seconds=1,
            )
        )

    assert commands == []


def test_repository_ship_prevalidates_and_executes_ordered_phase_selections(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    assert run_git(repo, "init").returncode == 0
    write_sdlc_contract(
        repo,
        release_operations={
            operation: {"steps": [{"id": operation, "run": ["python", "-V"]}]}
            for operation in ("check-a", "check-b", "publish-a")
        },
        deploy_operations={
            operation: {"steps": [{"id": operation, "run": ["python", "-V"]}]}
            for operation in ("deploy-a", "deploy-b")
        },
    )
    preflight_results = tuple(
        {"status": "completed", "operation": operation, "steps": [operation]}
        for operation in ("check-a", "check-b")
    )
    publication_results = tuple(
        {"status": "published", "operation": "publish-a", "steps": ["publish-a"]}
        for _ in range(2)
    )
    deployment_results = tuple(
        {"status": "deployed", "operation": operation, "steps": [operation]}
        for operation in ("deploy-a", "deploy-b")
    )
    shipped = {
        "status": "shipped",
        "repository": "example/repository",
        "commit": "a" * 40,
        "pr": 7,
        "url": "https://example.invalid/pull/7",
        "merge_commit": "c" * 40,
        "synchronized_head": "b" * 40,
    }
    responses = [
        (0, _prepared_batch("check-a", "check-b", "publish-a", "publish-a")),
        (0, _prepared_batch("deploy-a", "deploy-b")),
        (0, _completed_batch(*preflight_results)),
        (
            0,
            {
                "status": "ready",
                "source_branches": [],
                "pending_work_scope": "",
            },
        ),
        (0, shipped),
        (0, _completed_batch(*publication_results)),
        (0, _completed_batch(*deployment_results)),
    ]
    commands: list[list[str]] = []

    def run_json(command: list[str], **_: object) -> tuple[int, dict[str, Any]]:
        commands.append(command)
        return responses[len(commands) - 1]

    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    ship_repository = loaded["ship_repository"]
    ship_repository.__globals__["_run_json"] = run_json
    ship_repository.__globals__["_branch_worktree"] = (
        lambda repo_root, branch: None
    )
    result = ship_repository(
        argparse.Namespace(
            repo_root=repo,
            repo="example/repository",
            head_branch="release/local",
            base_branch="main",
            remote_name="origin",
            commit="a" * 40,
            title=None,
            body=None,
            merge_method="merge",
            delete_branch=False,
            reusable_head=True,
            sdlc_contract=pathlib.Path("sdlc/sdlc.yml"),
            release_preflight_operation=["check-a", "check-b"],
            release_operation=["publish-a", "publish-a"],
            deploy_operation=["deploy-a", "deploy-b"],
            ci_wait_seconds=1,
            review_wait_seconds=1,
            review_replies_request=None,
            interval_seconds=1,
        )
    )

    def selected(command: list[str]) -> list[str]:
        return [
            command[index + 1]
            for index, value in enumerate(command)
            if value == "--operation"
        ]

    assert len(commands) == 7
    assert selected(commands[0]) == [
        "check-a",
        "check-b",
        "publish-a",
        "publish-a",
    ]
    assert "--prepare-only" in commands[0]
    assert selected(commands[1]) == ["deploy-a", "deploy-b"]
    assert "--prepare-only" in commands[1]
    assert selected(commands[2]) == ["check-a", "check-b"]
    assert "prepare" in commands[3]
    assert "github_pr_workflow" in commands[4]
    assert selected(commands[5]) == ["publish-a", "publish-a"]
    assert selected(commands[6]) == ["deploy-a", "deploy-b"]
    assert result["release_publication"] == _completed_batch(*publication_results)
    assert result["deployment"] == _completed_batch(*deployment_results)


def test_repository_ship_release_failure_blocks_deployment_and_cleanup(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    assert run_git(repo, "init").returncode == 0
    write_sdlc_contract(
        repo,
        release_operations={
            "preflight": {
                "steps": [{"id": "check", "run": ["python", "check.py"]}]
            },
            "publish": {
                "steps": [{"id": "publish", "run": ["python", "publish.py"]}]
            },
        },
    )
    write_sdlc_contract(
        repo,
        deploy_operations={
            "deploy": {
                "steps": [
                    {"id": "deploy", "run": ["python", "deploy.py"]}
                ]
            }
        },
    )
    prepared = {
        "status": "ready",
        "source_branches": [],
        "pending_work_scope": "",
    }
    shipped = {
        "status": "shipped",
        "repository": "example/repository",
        "commit": "a" * 40,
        "pr": 17,
        "url": "https://example.invalid/pull/17",
        "merge_commit": "c" * 40,
        "synchronized_head": "b" * 40,
    }
    release_error = {
        "status": "operation_failed",
        "message": "Release step failed: publish",
        "operation": "publish",
        "commit": "a" * 40,
        "steps": [],
        "failed_step": "publish",
        "diagnostic": {
            "exit_code": 7,
            "stdout_tail": [],
            "stderr_tail": ["workflow failed"],
        },
    }
    responses: list[tuple[int, dict[str, Any]]] = [
        (
            0,
            _completed_batch(
                {
                    "status": "checked",
                    "operation": "preflight",
                    "steps": ["check"],
                }
            ),
        ),
        (0, prepared),
        (0, shipped),
        (1, _failed_batch(release_error)),
    ]
    commands: list[list[str]] = []

    def run_json(command: list[str]) -> tuple[int, dict[str, Any]]:
        commands.append(command)
        return responses[len(commands) - 1]

    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    ship_repository = loaded["ship_repository"]
    ship_repository.__globals__["_run_json"] = run_json
    ship_repository.__globals__["_prepare_operation_batch"] = (
        lambda *args, **kwargs: None
    )
    args = argparse.Namespace(
        repo_root=repo,
        repo="example/repository",
        head_branch="release/local",
        base_branch="main",
        remote_name="origin",
        commit="a" * 40,
        title=None,
        body=None,
        merge_method="merge",
        delete_branch=False,
        reusable_head=True,
        sdlc_contract=pathlib.Path("sdlc/sdlc.yml"),
        release_preflight_operation=["preflight"],
        release_operation=["publish"],
        deploy_operation=["deploy"],
        ci_wait_seconds=1,
        review_wait_seconds=1,
        review_replies_request=None,
        interval_seconds=1,
    )
    with pytest.raises(loaded["RepositoryShipError"]) as captured:
        ship_repository(args)

    assert captured.value.payload["phase"] == "release_publication"
    assert captured.value.payload["status"] == "operation_failed"
    assert captured.value.payload["diagnostic"] == release_error["diagnostic"]
    assert captured.value.payload["remote_mutation"] is True
    assert captured.value.payload["remaining"] == "release_publication"
    assert list(captured.value.payload["completed"]) == [
        "merge",
        "synchronization",
    ]
    assert captured.value.payload["operation_ledger"] == {
        "completed": [],
        "pending": [
            {"section": "release", "operation": "publish", "position": 1},
            {"section": "deploy", "operation": "deploy", "position": 1},
        ],
    }
    release_resume = captured.value.payload["resume_action"]
    assert pathlib.Path(release_resume["cwd"]) == repo.resolve()
    assert release_resume["argv"][:2] == [
        sys.executable,
        str(SHIP_REPOSITORY.resolve()),
    ]
    assert release_resume["argv"][
        release_resume["argv"].index("--commit") + 1
    ] == "a" * 40
    assert "--review-replies-request" not in release_resume["argv"]
    assert len(commands) == 4
    assert str(RELEASE_OPERATION) in commands[-1]
    assert "publish" in commands[-1]
    assert all(str(DEPLOY_OPERATION) not in command for command in commands)

    published = {"status": "published", "operation": "publish", "steps": []}
    deploy_error = {
        "status": "operation_failed",
        "message": "Deployment step failed: deploy",
        "operation": "deploy",
        "commit": "a" * 40,
        "steps": [],
        "failed_step": "deploy",
        "diagnostic": {
            "exit_code": 8,
            "stdout_tail": [],
            "stderr_tail": ["deployment failed"],
        },
    }
    preflight = {"status": "checked", "operation": "preflight", "steps": []}
    responses = [
        (0, _completed_batch(preflight)),
        (0, prepared),
        (0, shipped),
        (0, _completed_batch(published)),
        (1, _failed_batch(deploy_error)),
    ]
    commands.clear()
    with pytest.raises(loaded["RepositoryShipError"]) as captured:
        ship_repository(args)

    assert captured.value.payload["phase"] == "deployment"
    assert captured.value.payload["status"] == "operation_failed"
    assert captured.value.payload["diagnostic"] == deploy_error["diagnostic"]
    assert captured.value.payload["remaining"] == "deployment"
    assert list(captured.value.payload["completed"]) == [
        "merge",
        "synchronization",
        "release_publication",
    ]
    assert captured.value.payload["operation_ledger"] == {
        "completed": [
            {"section": "release", "operation": "publish", "position": 1}
        ],
        "pending": [
            {"section": "deploy", "operation": "deploy", "position": 1}
        ],
    }
    release_checkpoint = loaded["_operation_checkpoint_path"](
        repo, "a" * 40, "release_publication", "publish", 1
    )
    assert release_checkpoint.is_file()

    deployed = {"status": "deployed", "operation": "deploy", "steps": []}
    responses = [
        (0, _completed_batch(preflight)),
        (0, prepared),
        (0, {**shipped, "status": "already_shipped"}),
        (0, _completed_batch(deployed)),
    ]
    commands.clear()
    resumed = ship_repository(args)

    assert resumed["release_publication"] == _completed_batch(published)
    assert resumed["deployment"] == _completed_batch(deployed)
    assert all("publish" not in command for command in commands)
    assert not release_checkpoint.exists()


@pytest.mark.parametrize("late_phase", ["post_sync", "post_finalize"])
@pytest.mark.parametrize("relative_scope", [False, True])
def test_repository_ship_late_pending_work_reports_remote_mutation(
    tmp_path: pathlib.Path,
    late_phase: str,
    relative_scope: bool,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    assert run_git(repo, "init").returncode == 0
    write_sdlc_contract(repo, deploy_operations={})
    write_sdlc_contract(
        repo,
        release_operations={
            "preflight": {
                "steps": [{"id": "check", "run": ["python", "check.py"]}]
            },
            "publish": {
                "steps": [{"id": "publish", "run": ["python", "publish.py"]}]
            },
        },
    )
    scope = repo / "scope.json" if relative_scope else tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "version": 2,
                "target_branch": "release/local",
                "target_commit": "a" * 40,
                "sources": [
                    {
                        "branch": "selected",
                        "commit": "a" * 40,
                        "state": "retained",
                    }
                ],
            }
        ),
        encoding="utf-8",
        newline="\n",
    )
    shipped = {
        "status": "shipped",
        "repository": "example/repository",
        "commit": "a" * 40,
        "pr": 17,
        "url": "https://example.invalid/pull/17",
        "merge_commit": "c" * 40,
        "synchronized_head": "b" * 40,
    }
    pending = {
        "status": "pending_work",
        "remote_mutation": False,
        "findings": [
            {
                "kind": "dirty_worktree",
                "subject": "selected",
                "detail": "1 status entry",
            }
        ],
    }
    deployed = {
        "status": "deployed",
        "operation": "deploy",
        "steps": ["install"],
    }
    preflight = {
        "status": "checked",
        "operation": "preflight",
        "steps": ["check"],
    }
    published = {
        "status": "published",
        "operation": "publish",
        "steps": ["publish"],
    }
    prepared = {
        "status": "ready",
        "source_branches": ["selected"],
        "pending_work_scope": str(scope.resolve()),
    }
    responses: list[tuple[int, dict[str, Any]]] = (
        [
            (0, _completed_batch(preflight)),
            (0, prepared),
            (0, shipped),
            (2, pending),
        ]
        if late_phase == "post_sync"
        else [
            (0, _completed_batch(preflight)),
            (0, prepared),
            (0, shipped),
            (0, prepared),
            (0, _completed_batch(published)),
            (0, _completed_batch(deployed)),
            (2, pending),
        ]
    )
    commands: list[list[str]] = []

    def run_json(
        command: list[str], *, cwd: pathlib.Path | None = None
    ) -> tuple[int, dict[str, Any]]:
        commands.append(command)
        return responses[len(commands) - 1]

    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    ship_repository = loaded["ship_repository"]
    ship_repository.__globals__["_run_json"] = run_json
    ship_repository.__globals__["_prepare_operation_batch"] = (
        lambda *args, **kwargs: None
    )
    ship_repository.__globals__["_branch_worktree"] = (
        lambda repo_root, branch: None
    )
    args = argparse.Namespace(
        repo_root=repo,
        repo="example/repository",
        head_branch="release/local",
        base_branch="main",
        remote_name="origin",
        commit="a" * 40,
        title=None,
        body=None,
        merge_method="merge",
        delete_branch=False,
        reusable_head=True,
        sdlc_contract=pathlib.Path("sdlc/sdlc.yml"),
        release_preflight_operation=["preflight"],
        release_operation=["publish"],
        deploy_operation=["deploy"],
        ci_wait_seconds=1,
        review_wait_seconds=1,
        interval_seconds=1,
    )
    if late_phase == "post_finalize":
        stale_identity = loaded["_operation_identity"](
            repo,
            phase="deployment",
            section="deploy",
            target_branch="release/local",
            target_commit="d" * 40,
            synchronized_commit="b" * 40,
            contract=args.sdlc_contract,
            operation="deploy",
            position=1,
        )
        loaded["_write_operation_checkpoint"](
            loaded["_operation_checkpoint_path"](
                repo, "a" * 40, "deployment", "deploy", 1
            ),
            stale_identity,
            {"status": "deployed", "operation": "deploy", "steps": ["old"]},
        )

    result = ship_repository(args)

    assert result["status"] == "pending_work"
    assert result["remote_mutation"] is True
    assert result["repository"] == "example/repository"
    assert result["commit"] == "a" * 40
    assert result["remaining"] == (
        "selected_work_recheck"
        if late_phase == "post_sync"
        else "finalization"
    )
    assert list(result["completed"]) == (
        ["merge", "synchronization"]
        if late_phase == "post_sync"
        else [
            "merge",
            "synchronization",
            "release_publication",
            "deployment",
        ]
    )
    assert result["operation_ledger"] == (
        {
            "completed": [],
            "pending": [
                {"section": "release", "operation": "publish", "position": 1},
                {"section": "deploy", "operation": "deploy", "position": 1},
            ],
        }
        if late_phase == "post_sync"
        else {
            "completed": [
                {"section": "release", "operation": "publish", "position": 1},
                {"section": "deploy", "operation": "deploy", "position": 1},
            ],
            "pending": [],
        }
    )
    assert result["resume_action"]["argv"][
        result["resume_action"]["argv"].index("--commit") + 1
    ] == "a" * 40
    release_runner = str(SHIP_REPOSITORY.parent / "run-release-operation.py")
    deploy_runner = str(SHIP_REPOSITORY.parent / "run-deploy-operation.py")
    assert release_runner in commands[0]
    assert "preflight" in commands[0]
    assert "prepare" in commands[1]
    assert "check" in commands[3]
    if late_phase == "post_sync":
        assert len(commands) == 4
        assert "deployment" not in result
    else:
        assert len(commands) == 7
        assert release_runner in commands[4]
        assert "publish" in commands[4]
        assert deploy_runner in commands[5]
        assert "finalize" in commands[6]
        assert result["release_publication"] == _completed_batch(published)
        assert result["deployment"] == _completed_batch(deployed)
        release_checkpoint = loaded["_operation_checkpoint_path"](
            repo, "a" * 40, "release_publication", "publish", 1
        )
        deployment_checkpoint = loaded["_operation_checkpoint_path"](
            repo, "a" * 40, "deployment", "deploy", 1
        )
        assert release_checkpoint.is_file()
        assert deployment_checkpoint.is_file()
        release_temporary = release_checkpoint.with_suffix(
            release_checkpoint.suffix + ".tmp"
        )
        deployment_temporary = deployment_checkpoint.with_suffix(
            deployment_checkpoint.suffix + ".tmp"
        )
        release_temporary.write_text("stale", encoding="utf-8", newline="\n")
        deployment_temporary.write_text("stale", encoding="utf-8", newline="\n")
        unrelated_temporary = scope.with_name("unrelated.tmp")
        unrelated_temporary.write_text("retained", encoding="utf-8", newline="\n")
        responses.extend(
            [
                (0, _completed_batch(preflight)),
                (0, prepared),
                (0, {**shipped, "status": "already_shipped"}),
                (0, prepared),
                (1, {"status": "error", "message": "cleanup failed"}),
            ]
        )

        with pytest.raises(loaded["RepositoryShipError"]) as captured:
            ship_repository(args)

        recovery = captured.value.payload
        assert recovery["phase"] == "finalization"
        assert recovery["remaining"] == "finalization"
        assert recovery["completed"]["release_publication"] == _completed_batch(
            published
        )
        assert recovery["completed"]["deployment"] == _completed_batch(deployed)
        assert recovery["resume_action"] == result["resume_action"]
        assert "--review-replies-request" not in recovery["resume_action"]["argv"]
        assert release_checkpoint.is_file()
        assert deployment_checkpoint.is_file()

        responses.extend(
            [
                (0, _completed_batch(preflight)),
                (0, prepared),
                (0, {**shipped, "status": "already_shipped"}),
                (0, prepared),
                (0, {"status": "finalized"}),
            ]
        )

        resumed = ship_repository(args)

        assert resumed["status"] == "already_shipped"
        assert resumed["release_publication"] == _completed_batch(published)
        assert resumed["deployment"] == _completed_batch(deployed)
        assert len(commands) == 17
        retry_release_commands = [
            command for command in commands[7:] if release_runner in command
        ]
        assert len(retry_release_commands) == 2
        assert all(
            "preflight" in command and "publish" not in command
            for command in retry_release_commands
        )
        assert all(deploy_runner not in command for command in commands[7:])
        assert not release_checkpoint.exists()
        assert not deployment_checkpoint.exists()
        assert not release_temporary.exists()
        assert not deployment_temporary.exists()
        assert unrelated_temporary.is_file()


def test_repository_ship_rejects_malformed_deployment_checkpoint(
    tmp_path: pathlib.Path,
) -> None:
    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    checkpoint = tmp_path / "scope.deployment.json"
    checkpoint.write_text("{}", encoding="utf-8", newline="\n")
    identity = {
        "version": 1,
        "phase": "deployment",
        "section": "deploy",
        "target_branch": "release/local",
        "target_commit": "a" * 40,
        "synchronized_commit": "b" * 40,
        "contract": str(tmp_path / "sdlc.yml"),
        "operation": "deploy",
        "position": 1,
    }

    with pytest.raises(
        loaded["RepositoryShipError"],
        match="invalid structure",
    ):
        loaded["_read_operation_checkpoint"](checkpoint, identity)


def test_repository_ship_checkpoints_each_operation_separately(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    assert run_git(repo, "init").returncode == 0
    loaded = runpy.run_path(str(SHIP_REPOSITORY))

    first = loaded["_operation_checkpoint_path"](
        repo, "a" * 40, "deployment", "skills-deploy", 1
    )
    second = loaded["_operation_checkpoint_path"](
        repo, "a" * 40, "deployment", "imaging-tool-deploy", 2
    )

    assert first != second
    assert first.name.endswith(".deployment.001-skills-deploy.json")
    assert second.name.endswith(".deployment.002-imaging-tool-deploy.json")


def test_repository_ship_rejects_noncanonical_release_branch_before_remote_process(
    tmp_path: pathlib.Path,
) -> None:
    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    repo = tmp_path / "repo"
    repo.mkdir()
    child_calls: list[list[str]] = []

    def run_json(command: list[str]) -> tuple[int, dict[str, Any]]:
        child_calls.append(command)
        return 0, {}

    ship_repository = loaded["ship_repository"]
    ship_repository.__globals__["_run_json"] = run_json

    with pytest.raises(
        loaded["RepositoryShipError"],
        match="Head branch must be release/local",
    ):
        ship_repository(
            argparse.Namespace(
                repo_root=repo,
                head_branch="release/task",
            )
        )

    assert child_calls == []


def test_repository_ship_finalization_runs_outside_selected_worktree(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    repo = tmp_path / "repo"
    repo.mkdir()
    command = ["python", "manage-pending-work.py", "finalize"]
    events: list[tuple[str, object]] = []
    original_directory = pathlib.Path.cwd().resolve()

    def change_directory(path: pathlib.Path) -> None:
        events.append(("chdir", path))

    def run_json(
        child_command: list[str], *, cwd: pathlib.Path
    ) -> tuple[int, dict[str, Any]]:
        events.append(("run", (child_command, cwd)))
        return 0, {"status": "finalized"}

    monkeypatch.setattr(loaded["os"], "chdir", change_directory)
    loaded["_run_finalization"].__globals__["_run_json"] = run_json

    result = loaded["_run_finalization"](command, repo_root=repo)

    assert result == (0, {"status": "finalized"})
    assert events == [
        ("chdir", repo),
        ("run", (command, repo)),
        ("chdir", original_directory),
    ]


def test_repository_ship_blocks_selected_worktree_caller_before_remote_process(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loaded = runpy.run_path(str(SHIP_REPOSITORY))
    repo = tmp_path / "repo"
    selected = tmp_path / "worktrees" / "repo" / "thread"
    selected.mkdir(parents=True)
    repo.mkdir()
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "version": 2,
                "target_branch": "release/local",
                "target_commit": "a" * 40,
                "sources": [
                    {
                        "branch": "selected",
                        "commit": "a" * 40,
                        "state": "retained",
                    }
                ],
            }
        ),
        encoding="utf-8",
        newline="\n",
    )
    child_calls: list[list[str]] = []
    selected_path = {"value": selected}

    def branch_worktree(repo_root: pathlib.Path, branch: str) -> pathlib.Path:
        assert repo_root == repo
        assert branch == "selected"
        return selected_path["value"]

    def run_json(command: list[str]) -> tuple[int, dict[str, Any]]:
        child_calls.append(command)
        return 0, {
            "status": "ready",
            "source_branches": ["selected"],
            "pending_work_scope": str(scope),
        }

    ship_repository = loaded["ship_repository"]
    ship_repository.__globals__["_branch_worktree"] = branch_worktree
    ship_repository.__globals__["_run_json"] = run_json
    monkeypatch.chdir(selected)

    with pytest.raises(
        loaded["RepositoryShipError"],
        match="outside selected worktree",
    ):
        ship_repository(
            argparse.Namespace(
                repo_root=repo,
                repo="example/repository",
                head_branch="release/local",
                base_branch="main",
                remote_name="origin",
                commit="a" * 40,
                title=None,
                body=None,
                merge_method="merge",
                delete_branch=False,
                reusable_head=True,
                sdlc_contract=pathlib.Path("sdlc/sdlc.yml"),
                release_preflight_operation=["preflight"],
                release_operation=["publish"],
                deploy_operation=["deploy"],
                ci_wait_seconds=1,
                review_wait_seconds=1,
                interval_seconds=1,
            )
        )

    assert len(child_calls) == 1
    assert "prepare" in child_calls[0]

    preserved = tmp_path / "custom" / "repo" / "thread"
    preserved.mkdir(parents=True)
    selected_path["value"] = preserved
    monkeypatch.chdir(preserved)
    loaded["_require_cleanup_safe_caller"](
        repo,
        scope,
        [
            {
                "branch": "selected",
                "path": str(preserved.resolve()),
                "reason": "resolved parent chain has no 'worktrees' directory",
            }
        ],
    )
