#!/usr/bin/env python3
"""Sync shared Ceratops skill fragments into every skill."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections.abc import Mapping, Sequence


ROOT = pathlib.Path(__file__).resolve().parents[1]
FRAGMENT_MANIFEST = ROOT / "templates" / "skill-fragments.json"
SKILLS = ROOT / "skills"
START = "<!-- CERATOPS_COMMON_CORE_START -->"
END = "<!-- CERATOPS_COMMON_CORE_END -->"
SOURCE_PREFIX = "<!-- SOURCE: "
SOURCE_SUFFIX = " -->"


def load_manifest() -> dict[str, object]:
    return json.loads(FRAGMENT_MANIFEST.read_text(encoding="utf-8"))


def validate_manifest(manifest: Mapping[str, object], skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    fragments = manifest.get("fragments")
    assignments = manifest.get("skills")
    if not isinstance(fragments, Mapping):
        return ["fragment manifest is missing a valid fragments object"]
    if not isinstance(assignments, Mapping):
        return ["fragment manifest is missing a valid skills object"]

    if "core-minimal" not in fragments:
        errors.append("fragment manifest must define core-minimal")

    for fragment_name, rel_path in fragments.items():
        if not isinstance(rel_path, str):
            errors.append(f"fragment {fragment_name!r} must map to a string path")
            continue
        if not (ROOT / rel_path).is_file():
            errors.append(f"missing fragment file for {fragment_name}: {rel_path}")

    for skill_name, fragment_names in assignments.items():
        if skill_name not in skill_names:
            errors.append(f"unknown skill assignment: {skill_name}")
        if not isinstance(fragment_names, Sequence) or isinstance(fragment_names, str):
            errors.append(f"{skill_name}: fragment assignment must be a list")
            continue
        if "core-minimal" not in fragment_names:
            errors.append(f"{skill_name}: fragment assignment must include core-minimal")
        for fragment_name in fragment_names:
            if fragment_name not in fragments:
                errors.append(f"{skill_name}: unknown fragment assignment {fragment_name}")
        if "core-gh-findings" in fragment_names and "core-gh-current-state" not in fragment_names:
            errors.append(f"{skill_name}: core-gh-findings requires core-gh-current-state")

    for skill_name in skill_names:
        if skill_name not in assignments:
            errors.append(f"{skill_name}: missing fragment assignment")

    return errors


def fragment_text(rel_path: str) -> str:
    path = ROOT / rel_path
    return path.read_text(encoding="utf-8").strip("\n")


def normalized_template(skill_name: str, manifest: Mapping[str, object]) -> str:
    fragments = manifest["fragments"]
    assignments = manifest["skills"]
    fragment_names = assignments[skill_name]
    rendered: list[str] = []
    for name in fragment_names:
        rel_path = fragments[name]
        rendered.append(f"{SOURCE_PREFIX}{rel_path}{SOURCE_SUFFIX}")
        rendered.append(fragment_text(rel_path))
    body = "\n\n".join(rendered)
    return f"{START}\n{body}\n{END}"


def read_text_and_newline(path: pathlib.Path) -> tuple[str, str]:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    return text, newline


def sync_file(path: pathlib.Path, expected: str, check_only: bool) -> bool:
    text, newline = read_text_and_newline(path)
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
    path.write_text(updated.replace("\n", newline), encoding="utf-8", newline="")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if any skill is out of sync")
    args = parser.parse_args()

    manifest = load_manifest()
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    skill_names = {skill_md.parent.name for skill_md in skill_files}
    manifest_errors = validate_manifest(manifest, skill_names)
    if manifest_errors:
        for error in manifest_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    changed: list[pathlib.Path] = []
    for skill_md in skill_files:
        try:
            skill_name = skill_md.parent.name
            expected = normalized_template(skill_name, manifest)
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
        print("Shared skill fragments are in sync.")
        return 0

    for path in changed:
        print(f"UPDATED: {path.relative_to(ROOT)}")
    if not changed:
        print("No skill fragment updates needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
