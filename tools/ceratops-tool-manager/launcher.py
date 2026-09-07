"""Stable bootstrap ABI: select a complete manager environment on each launch.

The interpreter and this tiny launcher are bootstrap infrastructure. Tool
updates only replace active JSON, leaving every running process's files alone.
This launcher is installed once, and validates the selected receipt before
passing through the original CLI/transport arguments.
"""

import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path("C:/AI-Agents-Tools")

    def checked(path: Path) -> Path:
        if not path.is_relative_to(root):
            raise ValueError("launcher path escaped installation root")
        for item in (path, *path.parents):
            info = item.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError("launcher rejects links and reparse points")
        return path

    selected = json.loads(checked(root / "active" / "ceratops-tool-manager.json").read_text())
    if set(selected) != {"schema", "tool_id", "version", "manifest_sha256", "instance", "module"} or selected["schema"] != 1 or selected["tool_id"] != "ceratops-tool-manager" or selected["module"] != "ceratops_tool_manager":
        raise ValueError("invalid manager selection")
    if not isinstance(selected["instance"], str) or not re.fullmatch("[0-9a-f]{32}", selected["instance"]):
        raise ValueError("invalid installation identity")
    directory = root / "installations" / "ceratops-tool-manager" / selected["instance"]
    if json.loads(checked(directory / "receipt.json").read_text()) != selected:
        raise ValueError("manager receipt mismatch")
    python = checked(directory / "environment" / "Scripts" / "python.exe")
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith(("PYTHON", "PIP_", "UV_"))}
    return subprocess.call([str(python), "-I", "-B", "-m", "ceratops_tool_manager", *sys.argv[1:]], env=env)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        print(f"Tool manager launch failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
