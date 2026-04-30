#!/usr/bin/env python3
"""Validate Ceratops skill folders and generated shared sections."""

from __future__ import annotations

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
SECTION_MANIFEST = ROOT / "templates" / "skill-sections.json"
BASELINE_REFERENCE = pathlib.Path("references/best-practice-baseline.md")
SECTIONS_START = "<!-- CERATOPS_SHARED_SECTIONS_START -->"
SECTIONS_END = "<!-- CERATOPS_SHARED_SECTIONS_END -->"

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SKILL_REF_RE = re.compile(r"\$([a-z0-9][a-z0-9-]*)")
README_SKILL_ROW_RE = re.compile(r"^\|\s*`(?P<name>ceratops-[a-z0-9-]+)`\s*\|", re.MULTILINE)
ALLOWED_EXTERNAL_SKILL_REFS = {"skill-creator"}
INTERFACE_FIELD_RE = re.compile(
    r"^\s*(display_name|short_description|icon_small|icon_large|default_prompt):\s*(.+?)\s*$",
    re.MULTILINE,
)
CERATOPS_ICON_REL = "./assets/ceratops-logo-500.png"
CERATOPS_ICON_SOURCE = ROOT / "assets" / "ceratops-logo-500.png"
SHORT_DESC_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "before",
    "by",
    "for",
    "from",
    "in",
    "into",
    "it",
    "of",
    "on",
    "or",
    "the",
    "through",
    "to",
    "up",
    "use",
    "when",
    "with",
}
STALE_ACTIVE_PATTERNS: list[tuple[re.Pattern[str], str, set[pathlib.Path]]] = [
    (
        re.compile(r"templates/fragments/"),
        "stale fragments path",
        {pathlib.Path("CHANGELOG.md"), pathlib.Path("scripts/validate-skills.py")},
    ),
    (
        re.compile(r"templates/skill-fragments\.json"),
        "stale section-manifest name",
        {pathlib.Path("CHANGELOG.md"), pathlib.Path("scripts/validate-skills.py")},
    ),
    (
        re.compile(r"scripts/sync-skill-core\.py"),
        "stale sync-script name",
        {pathlib.Path("CHANGELOG.md"), pathlib.Path("scripts/validate-skills.py")},
    ),
    (re.compile(r"CERATOPS_COMMON_CORE"), "stale common-core marker", {pathlib.Path("scripts/validate-skills.py")}),
    (
        re.compile(r"\bgh_live\b"),
        "stale gh_live helper name",
        {pathlib.Path("CHANGELOG.md"), pathlib.Path("scripts/validate-skills.py")},
    ),
    (
        re.compile(r"\bgh-live\b"),
        "stale gh-live helper name",
        {pathlib.Path("CHANGELOG.md"), pathlib.Path("scripts/validate-skills.py")},
    ),
    (
        re.compile(r"\bceratops_gh_runtime\b"),
        "stale GH helper module name",
        {
            pathlib.Path("CHANGELOG.md"),
            pathlib.Path("scripts/install-skills.ps1"),
            pathlib.Path("scripts/validate-skills.py"),
        },
    ),
    (
        re.compile(r"\bceratops-gh-runtime\b"),
        "stale GH helper package name",
        {
            pathlib.Path("CHANGELOG.md"),
            pathlib.Path("scripts/install-skills.ps1"),
            pathlib.Path("scripts/validate-skills.py"),
        },
    ),
]
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


def load_section_manifest() -> dict[str, object]:
    return json.loads(SECTION_MANIFEST.read_text(encoding="utf-8"))


def parse_openai_interface(path: pathlib.Path) -> dict[str, str]:
    data: dict[str, str] = {}
    text = path.read_text(encoding="utf-8")
    for key, raw_value in INTERFACE_FIELD_RE.findall(text):
        value = raw_value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
    return data


def normalized_tokens(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9]+", text)]


def meaningful_short_description_tokens(text: str) -> set[str]:
    return {
        token
        for token in normalized_tokens(text)
        if token not in SHORT_DESC_STOPWORDS and (len(token) > 2 or token in {"gh", "pr", "ci"})
    }


def display_name_sane(skill_name: str, display_name: str) -> bool:
    name_tokens = {token for token in normalized_tokens(skill_name) if token != "ceratops"}
    if not name_tokens:
        return False
    display_tokens = set(normalized_tokens(display_name))
    overlap = len(name_tokens & display_tokens)
    return display_name.startswith("Ceratops ") and overlap / len(name_tokens) >= 0.5


def short_description_relevant(short_description: str, skill_description: str) -> bool:
    short_tokens = meaningful_short_description_tokens(short_description)
    if not short_tokens:
        return False
    description_tokens = meaningful_short_description_tokens(skill_description)
    overlap = len(short_tokens & description_tokens)
    required_overlap = min(2, len(short_tokens))
    return overlap >= required_overlap


def rendered_sections_block(skill_name: str, manifest: dict[str, object]) -> str:
    sections = manifest["sections"]
    assignments = manifest["skills"]
    section_names = assignments[skill_name]
    rendered: list[str] = []
    for section_name in section_names:
        rel_path = sections[section_name]
        raw_lines = (ROOT / rel_path).read_text(encoding="utf-8").splitlines()
        body = "\n".join(line for line in raw_lines if not re.fullmatch(r"\s*<!--\s*INTERNAL:.*?-->\s*", line)).strip("\n")
        rendered.append(f"<!-- SECTION SOURCE: {rel_path} -->")
        rendered.append(body)
    joined = "\n\n".join(rendered)
    return f"{SECTIONS_START}\n{joined}\n{SECTIONS_END}"


def readme_skill_rows(readme_text: str) -> set[str]:
    return {match.group("name") for match in README_SKILL_ROW_RE.finditer(readme_text)}


def validate_workflow_target(command: str, skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    normalized = command.strip().replace("\\", "/")
    parts = normalized.split()
    if not parts:
        return ["section manifest maintenance workflow contains an empty command"]

    if normalized.startswith("$"):
        target = normalized[1:]
        if target not in skill_names and target not in ALLOWED_EXTERNAL_SKILL_REFS:
            errors.append(f"section manifest maintenance workflow points to unknown skill {normalized}")
        return errors

    if len(parts) >= 2 and parts[0] in {"python", "py"} and parts[1].startswith("scripts/"):
        script_path = ROOT / parts[1]
        if not script_path.is_file():
            errors.append(f"section manifest maintenance workflow points to missing script {parts[1]}")
        return errors

    if len(parts) >= 3 and parts[0] in {"python", "py"} and parts[1] == "-m":
        module = parts[2]
        module_path = ROOT / "src" / pathlib.Path(module.replace(".", "/"))
        if not (module_path.with_suffix(".py").is_file() or (module_path / "__main__.py").is_file()):
            errors.append(f"section manifest maintenance workflow points to missing module {module}")
        return errors

    errors.append(f"section manifest maintenance workflow uses an unsupported command form: {command}")
    return errors


def check_skill_refs(path: pathlib.Path, text: str, skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    for ref in sorted(set(SKILL_REF_RE.findall(text))):
        if ref in ALLOWED_EXTERNAL_SKILL_REFS:
            continue
        if ref not in skill_names:
            errors.append(f"{path.relative_to(ROOT)}: unknown skill reference ${ref}")
    return errors


def check_stale_active_terms() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        for pattern, label, allowed_paths in STALE_ACTIVE_PATTERNS:
            if rel in allowed_paths:
                continue
            if pattern.search(text):
                errors.append(f"{rel}: {label}")
    return errors


def check_baseline_reference_ownership() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("best-practice-baseline.md"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if rel != BASELINE_REFERENCE:
            errors.append(f"{rel}: duplicate best-practice baseline; use {BASELINE_REFERENCE}")
    return errors


def check_skill(skill_dir: pathlib.Path, readme_rows: set[str], manifest: dict[str, object], skill_names: set[str]) -> list[str]:
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
    if name not in readme_rows:
        errors.append(f"{name}: missing README skill table row")
    if "## Boundaries" not in skill_md.read_text(encoding="utf-8"):
        errors.append(f"{name}: missing Boundaries section")
    core_text = skill_md.read_text(encoding="utf-8")
    start = core_text.find(SECTIONS_START)
    end = core_text.find(SECTIONS_END)
    if start == -1 or end == -1 or end < start:
        errors.append(f"{name}: missing shared sections markers")
    else:
        end += len(SECTIONS_END)
        actual = core_text[start:end]
        expected = rendered_sections_block(name, manifest)
        if actual != expected:
            errors.append(f"{name}: generated shared sections block is out of sync with manifest")

    if not openai_yaml.is_file():
        errors.append(f"{name}: missing agents/openai.yaml")
    else:
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "icon_small:", "icon_large:", "default_prompt:"):
            if required not in yaml_text:
                errors.append(f"{name}: openai.yaml missing {required}")
        if f"${name}" not in yaml_text:
            errors.append(f"{name}: default_prompt should mention ${name}")
        interface = parse_openai_interface(openai_yaml)
        display_name = interface.get("display_name", "")
        short_description = interface.get("short_description", "")
        icon_small = interface.get("icon_small", "")
        icon_large = interface.get("icon_large", "")
        if display_name and not display_name_sane(name, display_name):
            errors.append(f"{name}: display_name no longer matches the skill name closely enough")
        if short_description and not short_description_relevant(short_description, frontmatter.get("description", "")):
            errors.append(f"{name}: short_description no longer matches the skill description closely enough")
        for field_name, icon_value in (("icon_small", icon_small), ("icon_large", icon_large)):
            if icon_value and icon_value != CERATOPS_ICON_REL:
                errors.append(f"{name}: {field_name} should use shared Ceratops icon {CERATOPS_ICON_REL}")
            icon_path = (skill_dir / icon_value).resolve() if icon_value else None
            if icon_path and not icon_path.is_file():
                errors.append(f"{name}: {field_name} points to missing file {icon_value}")
            elif icon_path and CERATOPS_ICON_SOURCE.is_file() and icon_path.read_bytes() != CERATOPS_ICON_SOURCE.read_bytes():
                errors.append(f"{name}: {field_name} does not match repo icon {CERATOPS_ICON_SOURCE.relative_to(ROOT)}")
        errors.extend(check_skill_refs(openai_yaml, yaml_text, skill_names))

    errors.extend(check_skill_refs(skill_md, core_text, skill_names))

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
    if not SECTION_MANIFEST.is_file():
        errors.append("missing templates/skill-sections.json")
    if not CERATOPS_ICON_SOURCE.is_file():
        errors.append(f"missing shared Ceratops icon source: {CERATOPS_ICON_SOURCE.relative_to(ROOT)}")

    manifest = load_section_manifest() if SECTION_MANIFEST.is_file() else {"sections": {}, "skills": {}}
    sections = manifest.get("sections", {})
    workflow_hints = manifest.get("maintenance_workflows", {})
    assignments = manifest.get("skills", {})
    if "minimal" not in sections:
        errors.append("section manifest must define minimal")
    if not isinstance(workflow_hints, dict):
        errors.append("section manifest maintenance_workflows must be an object")
    else:
        required_workflows = {
            "shared_source_changes",
            "skill_local_or_metadata_changes",
            "helper_runtime_changes",
            "new_skill_local_availability",
        }
        for workflow_name in required_workflows:
            commands = workflow_hints.get(workflow_name)
            if not isinstance(commands, list) or not all(isinstance(item, str) for item in commands):
                errors.append(f"section manifest maintenance_workflows.{workflow_name} must be a list of strings")
    for section_name, rel_path in sections.items():
        if not (ROOT / rel_path).is_file():
            errors.append(f"missing section file for {section_name}: {rel_path}")
    for skill_name, section_names in assignments.items():
        if "minimal" not in section_names:
            errors.append(f"{skill_name}: section assignment must include minimal")
        for section_name in section_names:
            if section_name not in sections:
                errors.append(f"{skill_name}: unknown section assignment {section_name}")
        if "gh-findings" in section_names and "gh-current-state" not in section_names:
            errors.append(f"{skill_name}: gh-findings requires gh-current-state")

    readme_text = README.read_text(encoding="utf-8") if README.is_file() else ""
    readme_rows = readme_skill_rows(readme_text)
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    if not skill_dirs:
        errors.append("no skill directories found")

    skill_names = {skill_dir.name for skill_dir in skill_dirs}
    if isinstance(workflow_hints, dict):
        required_workflows = {
            "shared_source_changes",
            "skill_local_or_metadata_changes",
            "helper_runtime_changes",
            "new_skill_local_availability",
        }
        for workflow_name in required_workflows:
            commands = workflow_hints.get(workflow_name)
            if isinstance(commands, list) and all(isinstance(item, str) for item in commands):
                for command in commands:
                    errors.extend(validate_workflow_target(command, skill_names))
    for skill_name in assignments:
        if skill_name not in skill_names:
            errors.append(f"{skill_name}: section assignment points to a missing skill directory")
    for row_name in sorted(readme_rows):
        if row_name not in skill_names:
            errors.append(f"{row_name}: stale README skill table row")

    for skill_dir in skill_dirs:
        if skill_dir.name not in assignments:
            errors.append(f"{skill_dir.name}: missing section assignment in manifest")
            continue
        errors.extend(check_skill(skill_dir, readme_rows, manifest, skill_names))
    errors.extend(check_secrets())
    errors.extend(check_stale_active_terms())
    errors.extend(check_baseline_reference_ownership())

    if errors:
        print(f"errors: {len(errors)}", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"ok: {len(skill_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
