#!/usr/bin/env python3
"""Validate Ceratops skill folders and generated shared fragments."""

from __future__ import annotations

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
FRAGMENT_MANIFEST = ROOT / "templates" / "skill-fragments.json"
CORE_START = "<!-- CERATOPS_COMMON_CORE_START -->"
CORE_END = "<!-- CERATOPS_COMMON_CORE_END -->"

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY"),
    re.compile(r"C:\\Users\\roman", re.IGNORECASE),
]


def parse_frontmatter(path: pathlib.Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML frontmatter marker")

    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("missing closing YAML frontmatter marker") from exc

    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    body = "\n".join(lines[end + 1 :])
    return data, body


def load_fragment_manifest() -> dict[str, object]:
    return json.loads(FRAGMENT_MANIFEST.read_text(encoding="utf-8"))


def expected_common_core(skill_name: str, manifest: dict[str, object]) -> str:
    fragments = manifest["fragments"]
    assignments = manifest["skills"]
    fragment_names = assignments[skill_name]
    rendered: list[str] = []
    for fragment_name in fragment_names:
        rel_path = fragments[fragment_name]
        body = (ROOT / rel_path).read_text(encoding="utf-8").strip("\n")
        rendered.append(f"<!-- SOURCE: {rel_path} -->")
        rendered.append(body)
    joined = "\n\n".join(rendered)
    return f"{CORE_START}\n{joined}\n{CORE_END}"


def check_skill(skill_dir: pathlib.Path, readme_text: str, manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    if not NAME_RE.fullmatch(name):
        errors.append(f"{name}: invalid directory name")
    if not skill_md.is_file():
        errors.append(f"{name}: missing SKILL.md")
        return errors

    try:
        frontmatter, body = parse_frontmatter(skill_md)
    except ValueError as exc:
        errors.append(f"{name}: {exc}")
        return errors

    if set(frontmatter) != {"name", "description"}:
        errors.append(f"{name}: frontmatter must contain only name and description")
    if frontmatter.get("name") != name:
        errors.append(f"{name}: frontmatter name does not match directory")
    if len(frontmatter.get("description", "")) < 40:
        errors.append(f"{name}: description is too short")
    if "TODO" in skill_md.read_text(encoding="utf-8"):
        errors.append(f"{name}: contains TODO placeholder")
    if "publish-github-registry" in skill_md.read_text(encoding="utf-8"):
        errors.append(f"{name}: contains stale publish-github-registry reference")
    if not body.strip():
        errors.append(f"{name}: missing body")
    if name not in readme_text:
        errors.append(f"{name}: missing from README")
    if "## Boundaries" not in skill_md.read_text(encoding="utf-8"):
        errors.append(f"{name}: missing Boundaries section")
    core_text = skill_md.read_text(encoding="utf-8")
    start = core_text.find(CORE_START)
    end = core_text.find(CORE_END)
    if start == -1 or end == -1 or end < start:
        errors.append(f"{name}: missing common core markers")
    else:
        end += len(CORE_END)
        actual = core_text[start:end]
        expected = expected_common_core(name, manifest)
        if actual != expected:
            errors.append(f"{name}: generated shared fragment block is out of sync with manifest")

    if not openai_yaml.is_file():
        errors.append(f"{name}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "default_prompt:"):
            if required not in yaml_text:
                errors.append(f"{name}: openai.yaml missing {required}")
        if f"${name}" not in yaml_text:
            errors.append(f"{name}: default_prompt should mention ${name}")

    return errors


def check_secrets() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: high-confidence secret or private path pattern")
    return errors


def main() -> int:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        errors.append("missing skills/ directory")
    if not README.is_file():
        errors.append("missing README.md")
    if not FRAGMENT_MANIFEST.is_file():
        errors.append("missing templates/skill-fragments.json")

    manifest = load_fragment_manifest() if FRAGMENT_MANIFEST.is_file() else {"fragments": {}, "skills": {}}
    fragments = manifest.get("fragments", {})
    assignments = manifest.get("skills", {})
    if "core-minimal" not in fragments:
        errors.append("fragment manifest must define core-minimal")
    for fragment_name, rel_path in fragments.items():
        if not (ROOT / rel_path).is_file():
            errors.append(f"missing fragment file for {fragment_name}: {rel_path}")
    for skill_name, fragment_names in assignments.items():
        if "core-minimal" not in fragment_names:
            errors.append(f"{skill_name}: fragment assignment must include core-minimal")
        for fragment_name in fragment_names:
            if fragment_name not in fragments:
                errors.append(f"{skill_name}: unknown fragment assignment {fragment_name}")
        if "core-gh-findings" in fragment_names and "core-gh-current-state" not in fragment_names:
            errors.append(f"{skill_name}: core-gh-findings requires core-gh-current-state")

    readme_text = README.read_text(encoding="utf-8") if README.is_file() else ""
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    if not skill_dirs:
        errors.append("no skill directories found")

    skill_names = {skill_dir.name for skill_dir in skill_dirs}
    for skill_name in assignments:
        if skill_name not in skill_names:
            errors.append(f"{skill_name}: fragment assignment points to a missing skill directory")

    for skill_dir in skill_dirs:
        if skill_dir.name not in assignments:
            errors.append(f"{skill_dir.name}: missing fragment assignment in manifest")
            continue
        errors.extend(check_skill(skill_dir, readme_text, manifest))
    errors.extend(check_secrets())

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
