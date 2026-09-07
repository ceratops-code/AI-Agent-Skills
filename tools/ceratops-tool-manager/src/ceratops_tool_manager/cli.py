"""CLI/debugging adapter. Public deployment commands mirror the MCP tools."""

from __future__ import annotations

import argparse
import json
import sys

from . import TOOL_ID
from .contracts import DeploymentError
from .engine import Engine


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=TOOL_ID)
    commands = parser.add_subparsers(dest="operation", required=True)
    for operation in ("install", "update"):
        command = commands.add_parser(operation)
        command.add_argument("tool_id")
        command.add_argument("version")
    versions = commands.add_parser("versions")
    versions.add_argument("tool_id", nargs="?", default=TOOL_ID)
    args = parser.parse_args(argv)
    try:
        engine = Engine()
        result = getattr(engine, args.operation)(args.tool_id, args.version) if args.operation != "versions" else engine.versions(args.tool_id)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (DeploymentError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
