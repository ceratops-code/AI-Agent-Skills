#!/usr/bin/env python3
"""Run explicit Windows acceptance against the installed manager and harmless tool.

This maintenance command exercises real wheel installs and a persistent stdio
connection. It retains the harmless fixture's exact releases for repeatable
checks; source copies are removed on exit. Self-update is explicit and ends at
the requested version, after also testing ordinary previous-version selection.
No model calls, Codex registration, desktop restarts, or user data are involved.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from tool_manager_support import REPOSITORY  # isort: skip
from ceratops_tool_manager.contracts import DeploymentError, token
from ceratops_tool_manager.storage import Layout

sys.path.insert(0, str(REPOSITORY))
from tests.tool_manager.mcp_client import WireClient  # noqa: E402


def data(response):
    result = response.get("result", {})
    if response.get("error") or result.get("isError"):
        raise DeploymentError(json.dumps(response))
    return result.get("structuredContent") or json.loads(result["content"][0]["text"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--self-update-version", required=True)
    args = parser.parse_args()
    token(args.self_update_version, "version")
    scratch = args.scratch.resolve(strict=True)
    evidence = scratch / "tool-deployment-check.json"
    root = Layout().root
    command = [str(root / "runtime/python/python.exe"), "-I", "-B", str(root / "bin/ceratops-tool-manager.py")]
    result = {"status": "pending", "checks": []}
    try:
        spec = importlib.util.spec_from_file_location("package_tool_release", Path(__file__).with_name("package-tool-release.py"))
        packager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(packager)
        with tempfile.TemporaryDirectory(prefix="fixture-sources-", dir=scratch) as work:
            for version in ("2.0.0", "3.0.0"):
                source = Path(work) / version
                shutil.copytree(REPOSITORY / "tools/fixtures/harmless-tool", source, ignore=shutil.ignore_patterns("__pycache__", "*.egg-info", "build", "dist"))
                project = source / "pyproject.toml"
                project.write_text(project.read_text().replace('version = "1.0.0"', f'version = "{version}"'))
                if version == "3.0.0":
                    (source / "src/ceratops_deployment_fixture/__main__.py").write_text('raise SystemExit("Intentional readiness failure for deployment acceptance.")\n')
                packager.package(source)
        fixture = "ceratops-deployment-fixture"
        with WireClient([*command, "--mcp"]) as client:
            tools = client.request("tools/list")["result"]["tools"]
            assert {tool["name"] for tool in tools} == {"install", "update", "versions"}
            current = data(client.request("tools/call", {"name": "versions", "arguments": {}}))
            previous = current["installed_version"]
            assert previous != args.self_update_version, "self-update acceptance requires a different selected version"
            for operation, version in (("install", "1.0.0"), ("update", "2.0.0"), ("install", "1.0.0")):
                outcome = data(client.request("tools/call", {"name": operation, "arguments": {"tool_id": fixture, "version": version}}))
                assert outcome["installed_version"] == version
            before = (root / "active" / (fixture + ".json")).read_bytes()
            failure = client.request("tools/call", {"name": "update", "arguments": {"tool_id": fixture, "version": "3.0.0"}})
            assert failure.get("error") or failure["result"].get("isError")
            assert (root / "active" / (fixture + ".json")).read_bytes() == before
            outcome = data(client.request("tools/call", {"name": "update", "arguments": {"tool_id": "ceratops-tool-manager", "version": args.self_update_version}}))
            assert outcome["installed_version"] == args.self_update_version
            assert outcome["running_version"] == previous and outcome["reconnection_required"]
            # The same old connection remains usable after self-update.
            selected = data(client.request("tools/call", {"name": "versions", "arguments": {}}))
            assert selected["installed_version"] == args.self_update_version
            assert selected["running_version"] == previous
            data(client.request("tools/call", {"name": "install", "arguments": {"tool_id": "ceratops-tool-manager", "version": previous}}))
            data(client.request("tools/call", {"name": "update", "arguments": {"tool_id": "ceratops-tool-manager", "version": args.self_update_version}}))
            result["checks"].extend(["real dependency readiness", "fixture update", "previous-version installation", "failed candidate preserves selection", "self-update completes current request", "old process still serves"])
        with WireClient([*command, "--mcp"]) as client:
            current = data(client.request("tools/call", {"name": "versions", "arguments": {}}))
            assert current["installed_version"] == current["running_version"] == args.self_update_version
            assert not current["reconnection_required"]
            tools = client.request("tools/list")["result"]["tools"]
            assert all(tool["inputSchema"]["additionalProperties"] is False for tool in tools)
            unknown = client.request("tools/call", {"name": "versions", "arguments": {"root": "C:/outside"}})
            assert unknown.get("error") or unknown["result"].get("isError")
            escaped = client.request("tools/call", {"name": "install", "arguments": {"tool_id": "../outside", "version": "1.0.0"}})
            assert escaped.get("error") or escaped["result"].get("isError")
            result["manager"] = current
        cli = subprocess.run([*command, "versions"], capture_output=True, text=True, check=True, timeout=30)
        assert json.loads(cli.stdout) == result["manager"]
        result["checks"].extend(["next connection runs selected version", "unknown inputs rejected", "CLI/MCP parity"])
        result["status"] = "passed"
        print("OK")
        return 0
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
        print(result["error"], file=sys.stderr)
        return 2
    finally:
        evidence.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
