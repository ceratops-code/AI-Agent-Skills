#!/usr/bin/env python3
"""Validate shared Ceratops skill section assignments.

Source `skills/*/SKILL.md` files are intentionally delta-only. Runtime
installation expands the shared section assignments into generated `SKILL.md`
files under `$CODEX_HOME/skills` through `scripts/build-runtime-skills.py`.
This script remains the shared-source maintenance command: it validates the
section manifest and refuses stale source files that still contain generated
runtime blocks.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections.abc import Mapping, Sequence


ROOT = pathlib.Path(__file__).resolve().parents[1]
SECTION_MANIFEST = ROOT / "templates" / "skill-sections.json"
SKILLS = ROOT / "skills"
START = "<!-- CERATOPS_SHARED_SECTIONS_START -->"
END = "<!-- CERATOPS_SHARED_SECTIONS_END -->"
SOURCE_PREFIX = "<!-- SECTION SOURCE: "
SOURCE_SUFFIX = " -->"
INTERNAL_COMMENT_RE = re.compile(r"^\s*<!--\s*INTERNAL:.*?-->\s*$")


def load_manifest() -> dict[str, object]:
    return json.loads(SECTION_MANIFEST.read_text(encoding="utf-8"))


def validate_manifest(manifest: Mapping[str, object], skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    sections = manifest.get("sections")
    assignments = manifest.get("skills")
    if not isinstance(sections, Mapping):
        return ["section manifest is missing a valid sections object"]
    if not isinstance(assignments, Mapping):
        return ["section manifest is missing a valid skills object"]

    if "minimal" not in sections:
        errors.append("section manifest must define minimal")

    for section_name, rel_path in sections.items():
        if not isinstance(rel_path, str):
            errors.append(f"section {section_name!r} must map to a string path")
            continue
        if not (ROOT / rel_path).is_file():
            errors.append(f"missing section file for {section_name}: {rel_path}")

    for skill_name, section_names in assignments.items():
        if skill_name not in skill_names:
            errors.append(f"unknown skill section assignment: {skill_name}")
        if not isinstance(section_names, Sequence) or isinstance(section_names, str):
            errors.append(f"{skill_name}: section assignment must be a list")
            continue
        if "minimal" not in section_names:
            errors.append(f"{skill_name}: section assignment must include minimal")
        for section_name in section_names:
            if section_name not in sections:
                errors.append(f"{skill_name}: unknown section assignment {section_name}")
        if "gh-findings" in section_names and "gh-current-state" not in section_names:
            errors.append(f"{skill_name}: gh-findings requires gh-current-state")

    for skill_name in skill_names:
        if skill_name not in assignments:
            errors.append(f"{skill_name}: missing section assignment")

    return errors


def section_text(rel_path: str) -> str:
    path = ROOT / rel_path
    text = path.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if not INTERNAL_COMMENT_RE.fullmatch(line)]
    return "\n".join(lines).strip("\n")


def rendered_sections_block(skill_name: str, manifest: Mapping[str, object]) -> str:
    sections = manifest["sections"]
    assignments = manifest["skills"]
    section_names = assignments[skill_name]
    rendered: list[str] = []
    for name in section_names:
        rel_path = sections[name]
        rendered.append(f"{SOURCE_PREFIX}{rel_path}{SOURCE_SUFFIX}")
        rendered.append(section_text(rel_path))
    body = "\n\n".join(rendered)
    return f"{START}\n{body}\n{END}"


def read_text_and_newline(path: pathlib.Path) -> tuple[str, str]:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    return text, newline


def sync_file(path: pathlib.Path, expected: str) -> bool:
    text, newline = read_text_and_newline(path)
    start = text.find(START)
    end = text.find(END)
    if start == -1 and end == -1:
        return False
    raise ValueError(f"{path}: source SKILL.md must be delta-only; remove generated shared section markers")


def main() -> int:
    manifest = load_manifest()
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    skill_names = {skill_md.parent.name for skill_md in skill_files}
    manifest_errors = validate_manifest(manifest, skill_names)
    if manifest_errors:
        print(f"errors: {len(manifest_errors)}", file=sys.stderr)
        for error in manifest_errors:
            print(error, file=sys.stderr)
        return 1

    for skill_md in skill_files:
        try:
            skill_name = skill_md.parent.name
            expected = rendered_sections_block(skill_name, manifest)
            sync_file(skill_md, expected)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1

    print("ok: source skills are delta-only; runtime sections are generated by install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
