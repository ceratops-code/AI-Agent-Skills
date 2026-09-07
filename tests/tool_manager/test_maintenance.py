"""Validate source packaging and bootstrap contracts without network access."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from tests.tool_manager.test_engine import contracts, make_release, storage

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bootstrap_completes_launchers_after_runtime_record(tmp_path, monkeypatch):
    module = load("bootstrap-tool-manager")
    monkeypatch.setattr(storage, "INSTALL_ROOT", tmp_path)
    lock = json.loads((module.SOURCE / "bootstrap-lock.json").read_text())
    for relative in ("runtime/python/python.exe", "runtime/uv/uv.exe"):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"stub")
    (tmp_path / "runtime/runtime.json").write_text(json.dumps({"python": "python", "uv": "uv", "python_version": lock["python_version"], "uv_version": lock["uv_version"]}))
    monkeypatch.setattr(module.urllib.request, "urlopen", lambda *a, **kw: pytest.fail("must not download existing runtime"))
    module.prepare_runtime()
    assert (tmp_path / "bin/ceratops-tool-manager.py").is_file()
    assert (tmp_path / "bin/ceratops-tool-manager.cmd").is_file()
    (tmp_path / "runtime/runtime.json").write_text("{}")
    with pytest.raises(contracts.DeploymentError, match="incomplete"):
        module.prepare_runtime()


def test_packaging_refuses_changed_version_and_publishes_atomically(tmp_path, monkeypatch):
    module = load("package-tool-release")
    runtime_root = tmp_path / "installed"
    runtime_root.mkdir()
    monkeypatch.setattr(storage, "INSTALL_ROOT", runtime_root)
    bundle = make_release(runtime_root, "1.0.0")
    project = tmp_path / "source"
    project.mkdir()
    (project / "tool.json").write_text(json.dumps({"schema": 1, "tool_id": "fixture", "distribution": "fixture", "module": "fixture"}))
    (project / "pyproject.toml").write_text('[project]\nname="fixture"\nversion="1.0.0"\n')
    (project / "pylock.toml").write_text('lock-version="1.0"\npackages=[]\n')
    for relative in ("runtime/python/python.exe", "runtime/uv/uv.exe"):
        path = runtime_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"stub")
    (runtime_root / "runtime/runtime.json").write_text('{"python_version":"3.13.12"}')

    def build(command, **kwargs):
        destination = Path(command[command.index("--out-dir") + 1])
        source = next(bundle.glob("*.whl"))
        (destination / source.name).write_bytes(source.read_bytes())
        return ""

    monkeypatch.setattr(module, "run", build)
    with pytest.raises(contracts.DeploymentError, match="another artifact"):
        module.package(project)
    registry_path = runtime_root / "registry.json"
    registry_path.write_text('{"schema":1,"tools":{}}')
    result = module.package(project)
    assert json.loads(registry_path.read_text())["tools"]["fixture"]["1.0.0"] == result["manifest_sha256"]
    assert not list((runtime_root / "staging").iterdir())
    assert module.package(project) == result
