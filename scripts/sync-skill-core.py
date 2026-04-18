#!/usr/bin/env python3
"""Sync the shared Ceratops skill core block into every skill."""

from __future__ import annotations

import argparse
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "common-core.md"
SKILLS = ROOT / "skills"
START = "<!-- CERATOPS_COMMON_CORE_START -->"
END = "<!-- CERATOPS_COMMON_CORE_END -->"


def normalized_template() -> str:
    text = TEMPLATE.read_text(encoding="utf-8").strip("\n")
    return f"{START}\n{text}\n{END}"


def sync_file(path: pathlib.Path, expected: str, check_only: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"{path}: missing common core markers")

    end += len(END)
    actual = text[start:end]
    if actual == expected:
        return False

    if check_only:
        return True

    updated = text[:start] + expected + text[end:]
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if any skill is out of sync")
    args = parser.parse_args()

    expected = normalized_template()
    changed: list[pathlib.Path] = []

    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        try:
            if sync_file(skill_md, expected, args.check):
                changed.append(skill_md)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    if args.check:
        if changed:
            for path in changed:
                print(f"OUT_OF_SYNC: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("Common core is in sync.")
        return 0

    for path in changed:
        print(f"UPDATED: {path.relative_to(ROOT)}")
    if not changed:
        print("No skill core updates needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
