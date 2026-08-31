from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys

import pytest

from tests.repository_lifecycle.support import (
    DEPLOY_OPERATION,
    REPOSITORY_LIFECYCLE_SOURCE,
    SDLC_CONTRACT_TEMPLATE,
    run_deploy_operation,
    run_release_operation,
)
from repository_operation import (
    OperationProfile,
    OperationRequest,
    OperationError,
    execute_prepared_operations,
    prepare_operations,
)
from tests.support.repositories import write_sdlc_contract


def test_sdlc_template_is_a_schema_valid_empty_skeleton(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    contract = write_sdlc_contract(repo, deploy_operations={})
    shutil.copy2(SDLC_CONTRACT_TEMPLATE, contract)

    result = run_deploy_operation(repo, "missing")

    assert result.returncode == 1
    payload = json.loads(result.stderr)
    assert payload["status"] == "error"
    assert payload["message"] == "Deployment operation is not declared: missing"

    optional = run_deploy_operation(repo, "missing", if_declared=True)
    assert optional.returncode == 0, optional.stderr
    assert json.loads(optional.stdout) == {
        "status": "no_op",
        "operation": "missing",
        "steps": [],
        "reason": "operation_not_declared",
    }


def test_absent_sdlc_section_is_a_successful_no_op(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    write_sdlc_contract(repo, release_operations={})

    result = run_deploy_operation(repo, "deploy")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "status": "no_op",
        "operation": "deploy",
        "steps": [],
        "reason": "contract_section_not_declared",
    }


def test_deploy_operation_preserves_argv_without_a_shell(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    probe = repo / "argv-probe.py"
    output = repo / "argv.json"
    injected = repo / "injected.txt"
    literal = f"literal; echo injected > {injected}"
    probe.write_text(
        "import json, pathlib, sys\n"
        "pathlib.Path(sys.argv[1]).write_text("
        "json.dumps(sys.argv[2:]), encoding='utf-8')\n",
        encoding="utf-8",
        newline="\n",
    )
    write_sdlc_contract(
        repo,
        deploy_operations={
            "verify": {
                "handoff": "ceratops-skill-lifecycle/deploy",
                "steps": [
                    {
                        "id": "argv",
                        "run": [
                            sys.executable,
                            "argv-probe.py",
                            str(output),
                            "value with spaces",
                            literal,
                        ],
                    }
                ]
            }
        },
    )

    result = run_deploy_operation(repo, "verify")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "status": "deployed",
        "operation": "verify",
        "commit": None,
        "steps": ["argv"],
        "handoff": "ceratops-skill-lifecycle/deploy",
    }
    assert json.loads(output.read_text(encoding="utf-8")) == [
        "value with spaces",
        literal,
    ]
    assert not injected.exists()

    write_sdlc_contract(
        repo,
        release_operations={
            "publish": {
                "steps": [
                    {
                        "id": "argv",
                        "run": [
                            sys.executable,
                            "argv-probe.py",
                            str(output),
                            "release value",
                            literal,
                        ],
                    }
                ]
            }
        },
    )
    published = run_release_operation(repo, "publish")

    assert published.returncode == 0, published.stderr
    assert json.loads(published.stdout) == {
        "status": "published",
        "operation": "publish",
        "commit": None,
        "steps": ["argv"],
    }
    assert json.loads(output.read_text(encoding="utf-8")) == [
        "release value",
        literal,
    ]
    wrong_contract = run_release_operation(
        repo,
        "verify",
        contract=repo / "sdlc" / "sdlc.yml",
    )
    assert wrong_contract.returncode == 1
    assert json.loads(wrong_contract.stderr)["message"] == (
        "Release operation is not declared: verify"
    )
    assert not injected.exists()


def test_deploy_operation_requires_and_expands_exact_declared_parameters(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    output = repo / "parameter.txt"
    parameterless_output = repo / "parameterless.txt"
    probe = repo / "parameter-probe.py"
    probe.write_text(
        "import pathlib, sys\n"
        "pathlib.Path(sys.argv[1]).write_text(sys.argv[2], encoding='utf-8')\n",
        encoding="utf-8",
        newline="\n",
    )
    write_sdlc_contract(
        repo,
        deploy_operations={
            "after_promote": {
                "parameters": ["base_revision"],
                "steps": [
                    {
                        "id": "record",
                        "run": [
                            sys.executable,
                            "parameter-probe.py",
                            str(output),
                            "{base_revision}",
                        ],
                    }
                ],
            },
            "parameterless": {
                "steps": [
                    {
                        "id": "record",
                        "run": [
                            sys.executable,
                            "parameter-probe.py",
                            str(parameterless_output),
                            "literal",
                        ],
                    }
                ]
            },
        },
    )

    missing = run_deploy_operation(repo, "after_promote")
    assert missing.returncode == 1
    assert "missing base_revision" in json.loads(missing.stderr)["message"]
    extra = run_deploy_operation(
        repo,
        "after_promote",
        parameters=("base_revision=abc", "unexpected=value"),
    )
    assert extra.returncode == 1
    assert "unexpected unexpected" in json.loads(extra.stderr)["message"]

    conditional = run_deploy_operation(
        repo,
        "after_promote",
        parameters_if_declared=("base_revision=conditional",),
    )
    assert conditional.returncode == 0, conditional.stderr
    assert output.read_text(encoding="utf-8") == "conditional"

    duplicated = run_deploy_operation(
        repo,
        "after_promote",
        parameters=("base_revision=explicit",),
        parameters_if_declared=("base_revision=conditional",),
    )
    assert duplicated.returncode == 1
    assert "supplied more than once" in json.loads(duplicated.stderr)["message"]

    strict_parameterless = run_deploy_operation(
        repo,
        "parameterless",
        parameters=("base_revision=explicit",),
    )
    assert strict_parameterless.returncode == 1
    assert "unexpected base_revision" in json.loads(strict_parameterless.stderr)[
        "message"
    ]
    conditional_parameterless = run_deploy_operation(
        repo,
        "parameterless",
        parameters_if_declared=("base_revision=conditional",),
    )
    assert (
        conditional_parameterless.returncode == 0
    ), conditional_parameterless.stderr
    assert parameterless_output.read_text(encoding="utf-8") == "literal"

    result = run_deploy_operation(
        repo,
        "after_promote",
        parameters=("base_revision=0123456789abcdef",),
    )
    assert result.returncode == 0, result.stderr
    assert output.read_text(encoding="utf-8") == "0123456789abcdef"


def test_deploy_runs_repository_command_once_from_repository_directory(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    installed_skill = tmp_path / "runtime" / "ceratops-repo-lifecycle"
    installed_skill.mkdir(parents=True)
    (repo / "scripts").mkdir(parents=True)
    log = tmp_path / "deploy-invocations.jsonl"
    (repo / "scripts" / "deploy-repository.py").write_text(
        "import json, os, pathlib, sys\n"
        "with pathlib.Path(os.environ['INSTALL_LOG']).open('a', encoding='utf-8') as stream:\n"
        "    stream.write(json.dumps({'cwd': str(pathlib.Path.cwd()), 'argv': sys.argv[1:]}) + '\\n')\n",
        encoding="utf-8",
        newline="\n",
    )
    write_sdlc_contract(
        repo,
        deploy_operations={
            "deploy": {
                "steps": [
                    {
                        "id": "deploy-repository",
                        "run": [sys.executable, "scripts/deploy-repository.py"],
                    }
                ]
            }
        },
    )

    result = subprocess.run(
        [
            sys.executable,
            str(DEPLOY_OPERATION),
            "--repo-root",
            str(repo),
            "--operation",
            "deploy",
        ],
        cwd=installed_skill,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "INSTALL_LOG": str(log)},
    )

    assert result.returncode == 0, result.stderr
    invocations = [
        json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()
    ]
    assert invocations == [{"cwd": str(repo.resolve()), "argv": []}]


def test_deploy_operation_rejects_invalid_schema(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    contract = write_sdlc_contract(
        repo,
        deploy_operations={
            "invalid": {"steps": [{"id": "invalid", "run": "python -V"}]}
        },
    )

    result = run_deploy_operation(repo, "invalid", contract=contract)

    assert result.returncode == 1
    payload = json.loads(result.stderr)
    assert payload["status"] == "error"
    assert payload["message"].startswith("Invalid deployment contract:")


def test_deploy_operation_enforces_repository_path_boundaries(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    outside = tmp_path / "outside"
    marker = repo / "must-not-run.txt"
    repo.mkdir()
    outside.mkdir()
    write_sdlc_contract(
        repo,
        deploy_operations={
            "escape": {
                "steps": [
                    {
                        "id": "would-mutate",
                        "run": [
                            sys.executable,
                            "-c",
                            (
                                "import pathlib; "
                                "pathlib.Path('must-not-run.txt').write_text('ran')"
                            ),
                        ],
                    },
                    {
                        "id": "escape",
                        "cwd": "../outside",
                        "run": [sys.executable, "-c", "raise SystemExit(0)"],
                    }
                ]
            }
        },
    )

    escaped_cwd = run_deploy_operation(repo, "escape")

    assert escaped_cwd.returncode == 1
    assert json.loads(escaped_cwd.stderr)["message"] == (
        "Deployment step cwd must be a directory inside the repository."
    )
    assert not marker.exists()

    outside_contract = outside / "sdlc.yml"
    outside_contract.write_text(
        json.dumps({"version": 1, "operations": {}}),
        encoding="utf-8",
        newline="\n",
    )
    escaped_contract = run_deploy_operation(
        repo,
        "escape",
        contract=outside_contract,
    )
    assert escaped_contract.returncode == 1
    assert json.loads(escaped_contract.stderr)["message"] == (
        "Deployment contract must be a file inside the repository."
    )


def test_deploy_operation_reports_a_bounded_failure_tail(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    failure = repo / "fail.py"
    failure.write_text(
        "import sys\n"
        "for index in range(12):\n"
        "    print(f'line-{index}', file=sys.stderr)\n"
        "raise SystemExit(7)\n",
        encoding="utf-8",
        newline="\n",
    )
    write_sdlc_contract(
        repo,
        deploy_operations={
            "fail": {
                "steps": [
                    {
                        "id": "expected-failure",
                        "run": [sys.executable, "fail.py"],
                    }
                ]
            }
        },
    )

    result = run_deploy_operation(repo, "fail")

    assert result.returncode == 1
    payload = json.loads(result.stderr)
    assert payload["status"] == "operation_failed"
    assert payload["message"] == "Deployment step failed: expected-failure"
    assert payload["operation"] == "fail"
    assert payload["commit"] is None
    assert payload["steps"] == []
    assert payload["failed_step"] == "expected-failure"
    assert payload["diagnostic"] == {
        "exit_code": 7,
        "stdout_tail": [],
        "stderr_tail": [f"line-{index}" for index in range(4, 12)],
    }


def _deployment_profile() -> OperationProfile:
    return OperationProfile(
        label="Deployment",
        section="deploy",
        default_contract=pathlib.Path("sdlc/sdlc.yml"),
        schema=(
            REPOSITORY_LIFECYCLE_SOURCE
            / "references"
            / "schemas"
            / "sdlc.yml.schema.json"
        ),
        default_success_status="deployed",
        operation_statuses={},
    )


def test_prepare_operations_validates_the_whole_sequence_before_execution(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    marker = repo / "must-not-run.txt"
    write_sdlc_contract(
        repo,
        deploy_operations={
            "first": {
                "steps": [
                    {
                        "id": "mutate",
                        "run": [
                            sys.executable,
                            "-c",
                            "import pathlib; pathlib.Path('must-not-run.txt').write_text('ran')",
                        ],
                    }
                ]
            },
            "invalid-later": {
                "steps": [
                    {
                        "id": "escape",
                        "cwd": "../outside",
                        "run": [sys.executable, "-V"],
                    }
                ]
            },
        },
    )
    (tmp_path / "outside").mkdir()

    with pytest.raises(
        OperationError,
        match="step cwd must be a directory inside the repository",
    ):
        prepare_operations(
            repo,
            [OperationRequest("first"), OperationRequest("invalid-later")],
            _deployment_profile(),
        )

    assert not marker.exists()


def test_execute_prepared_operations_stops_after_failure_with_a_ledger(
    tmp_path: pathlib.Path,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    write_sdlc_contract(
        repo,
        deploy_operations={
            "first": {
                "steps": [
                    {
                        "id": "first",
                        "run": [
                            sys.executable,
                            "-c",
                            "import pathlib; pathlib.Path('first.txt').write_text('ran')",
                        ],
                    }
                ]
            },
            "fails": {
                "steps": [
                    {
                        "id": "fails",
                        "run": [sys.executable, "-c", "raise SystemExit(9)"],
                    }
                ]
            },
            "later": {
                "steps": [
                    {
                        "id": "later",
                        "run": [
                            sys.executable,
                            "-c",
                            "import pathlib; pathlib.Path('later.txt').write_text('ran')",
                        ],
                    }
                ]
            },
        },
    )
    prepared = prepare_operations(
        repo,
        [OperationRequest("first"), OperationRequest("fails"), OperationRequest("later")],
        _deployment_profile(),
    )

    result = execute_prepared_operations(prepared)

    assert result["status"] == "operation_failed"
    assert result["completed_operations"] == ["first"]
    assert result["pending_operations"] == ["fails", "later"]
    assert (repo / "first.txt").is_file()
    assert not (repo / "later.txt").exists()
