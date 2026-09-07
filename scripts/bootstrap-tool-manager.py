#!/usr/bin/env python3
"""Install the first manager with the shared engine, or prepare its fixed runtime.

Network side effects are limited to pinned official uv/Python downloads and
locked wheel dependencies. Temporary downloads live under the installation
root and are removed on exit. This never edits Codex settings or restarts apps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from tool_manager_support import SOURCE  # isort: skip
from ceratops_tool_manager.contracts import DeploymentError, read_json
from ceratops_tool_manager.engine import Engine
from ceratops_tool_manager.storage import Layout


def ensure_launchers(layout: Layout) -> None:
    """Complete interrupted first-bootstrap launcher provisioning without overwrite."""
    layout.directory("bin")
    launcher = layout.path("bin", "ceratops-tool-manager.py")
    if not launcher.exists():
        shutil.copyfile(SOURCE / "launcher.py", launcher)
    command = layout.path("bin", "ceratops-tool-manager.cmd")
    if not command.exists():
        command.write_text('@echo off\r\n"C:\\AI-Agents-Tools\\runtime\\python\\python.exe" -I -B "C:\\AI-Agents-Tools\\bin\\ceratops-tool-manager.py" %*\r\n', encoding="utf-8", newline="")


def prepare_runtime() -> None:
    """Only the explicit bootstrap provisions uv and the managed interpreter."""
    if os.name != "nt":
        raise DeploymentError("bootstrap supports Windows x64")
    layout = Layout()
    layout.directory("runtime")
    lock = read_json(SOURCE / "bootstrap-lock.json")
    expected = {"python": "python", "uv": "uv", "python_version": lock["python_version"], "uv_version": lock["uv_version"]}
    record = layout.path("runtime", "runtime.json")
    if record.exists():
        if read_json(record) != expected or not layout.path("runtime", "python", "python.exe").is_file() or not layout.path("runtime", "uv", "uv.exe").is_file():
            raise DeploymentError("existing bootstrap runtime differs or is incomplete")
        ensure_launchers(layout)
        return
    with layout.lock("bootstrap"):
        layout.directory("staging")
        with tempfile.TemporaryDirectory(prefix="bootstrap-", dir=layout.path("staging")) as work:
            temporary = Path(work)
            archive = temporary / "uv.whl"
            request = urllib.request.Request(lock["uv_url"], headers={"User-Agent": "ceratops-tool-manager-bootstrap/1"})
            with urllib.request.urlopen(request, timeout=60) as response, archive.open("wb") as output:
                shutil.copyfileobj(response, output)
            if hashlib.sha256(archive.read_bytes()).hexdigest() != lock["uv_sha256"]:
                raise DeploymentError("uv download digest mismatch")
            layout.directory("runtime", "uv")
            uv = layout.path("runtime", "uv", "uv.exe")
            with zipfile.ZipFile(archive) as wheel:
                names = [n for n in wheel.namelist() if n.endswith("/uv.exe")]
                if len(names) != 1:
                    raise DeploymentError("uv wheel executable is ambiguous")
                expected_uv = wheel.read(names[0])
                if uv.exists() and uv.read_bytes() != expected_uv:
                    raise DeploymentError("existing uv executable differs from the pinned artifact")
                if not uv.exists():
                    uv.write_bytes(expected_uv)
            env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("UV_", "PIP_", "PYTHON"))}
            env.update({"UV_PYTHON_INSTALL_DIR": str(temporary / "python"), "UV_PYTHON_BIN_DIR": str(temporary / "bin"),
                        "UV_CACHE_DIR": str(layout.directory("cache")), "UV_NO_CONFIG": "1", "UV_PYTHON_INSTALL_BIN": "0",
                        "TEMP": work, "TMP": work})
            result = subprocess.run([str(uv), "python", "install", lock["python_version"], "--no-config"], env=env, capture_output=True, text=True, timeout=240, check=False)
            if result.returncode:
                raise DeploymentError(result.stderr[-2000:])
            found = subprocess.run([str(uv), "python", "find", "--managed-python", "--no-project", "--no-config", lock["python_version"]], env=env, capture_output=True, text=True, timeout=30, check=False)
            interpreter = Path(found.stdout.strip()).resolve()
            if found.returncode or not interpreter.is_file() or not interpreter.is_relative_to(temporary / "python"):
                raise DeploymentError(f"managed Python selection is invalid: {found.stderr[-1000:]}")
            destination = layout.path("runtime", "python")
            if destination.exists():
                raise DeploymentError("unrecorded Python runtime exists; preserve it for inspection")
            shutil.move(str(interpreter.parent), str(destination))
            layout.atomic_json(record, expected)
        # The stable launcher only selects a complete environment. It contains
        # no installer and never changes while a manager process is serving.
        ensure_launchers(layout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-runtime", action="store_true")
    args = parser.parse_args()
    try:
        prepare_runtime()
        if not args.prepare_runtime:
            if Engine().selected("ceratops-tool-manager") is not None:
                raise DeploymentError("manager is already installed; use its install or update command")
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("package-tool-release.py")), "--source", str(SOURCE)], check=False)
            if result.returncode:
                return result.returncode
            import tomllib

            version = tomllib.loads((SOURCE / "pyproject.toml").read_text())["project"]["version"]
            print(json.dumps(Engine().install("ceratops-tool-manager", version), sort_keys=True))
        else:
            print("OK")
        return 0
    except (DeploymentError, OSError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
