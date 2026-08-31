#!/usr/bin/env python3
"""Validate the Codex plugin, Agent Skills, and review-freshness contract."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT
SKILLS = PLUGIN / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?P<target>[^)]+)\)")
PLAIN_YAML_NON_STRING_RE = re.compile(
    r"(?ix)(?:null|~|true|false|yes|no|on|off|[-+]?(?:\d[\d_]*)(?:\.\d[\d_]*)?(?:e[-+]?\d+)?|\d{4}-\d{2}-\d{2})"
)
ALLOWED_TOP_LEVEL = {"name", "description", "license", "metadata", "allowed-tools"}
PLUGIN_TOP_LEVEL_FIELDS = {
    "id",
    "name",
    "version",
    "description",
    "skills",
    "apps",
    "mcpServers",
    "interface",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
}
PLUGIN_INTERFACE_FIELDS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "websiteURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
    "brandColor",
    "composerIcon",
    "logo",
    "logoDark",
    "screenshots",
    "defaultPrompt",
    "default_prompt",
}
AGENT_TOP_LEVEL_FIELDS = {"interface", "policy", "dependencies"}
AGENT_INTERFACE_FIELDS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".swift", ".txt"}
REQUIRED_METADATA = (
    "author",
    "version",
    "last-updated",
    "last-reviewed",
    "apple-docs-reviewed",
)
PUBLICATION_PATTERNS = (
    (
        "local Unix user path",
        re.compile(r"(?i)(?:^|[\s`\"'(])/(?:users|home)/[^/\s`\"')]+/"),
    ),
    (
        "local Windows user path",
        re.compile(r"(?i)\b[A-Z]:\\users\\[^\\\s]+\\"),
    ),
    (
        "private key material",
        re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    ),
    (
        "GitHub credential",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "OpenAI credential",
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ),
)
PUBLICATION_SKIP_PARTS = {".git", ".venv", "__pycache__"}
PRIVATE_MARKER_FILENAME = ".publication-private-markers"


def parse_string_scalar(raw: str, context: str) -> str:
    value = raw.strip()
    if not value:
        raise ValueError(f"{context} must be a nonempty string scalar")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"{context} has invalid double-quoted YAML") from error
        if not isinstance(parsed, str):
            raise ValueError(f"{context} must be a string")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ValueError(f"{context} has invalid single-quoted YAML")
        return value[1:-1].replace("''", "'")
    if value[0] in "[{&*!|>@`" or value.endswith(":") or PLAIN_YAML_NON_STRING_RE.fullmatch(value):
        raise ValueError(f"{context} must be a string scalar, got {value!r}")
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error

    top: dict[str, str] = {}
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t")):
            key, separator, raw_value = line.partition(":")
            if not separator:
                raise ValueError(f"invalid frontmatter line {line!r}")
            key = key.strip()
            if key in top:
                raise ValueError(f"duplicate frontmatter field {key}")
            in_metadata = key == "metadata" and not raw_value.strip()
            if in_metadata:
                top[key] = ""
                continue
            top[key] = parse_string_scalar(raw_value, key)
            continue
        if "\t" in line or not in_metadata or not line.startswith("  ") or line.startswith("    "):
            raise ValueError(f"unsupported frontmatter indentation in {line!r}")
        key, separator, raw_value = line.strip().partition(":")
        if not separator:
            raise ValueError(f"invalid metadata line {line!r}")
        if key in metadata:
            raise ValueError(f"duplicate metadata field {key}")
        metadata[key] = parse_string_scalar(raw_value, f"metadata.{key}")

    return top, metadata, "\n".join(lines[closing + 1 :])


def parse_date(value: str, field: str, skill: str, errors: list[str]) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        errors.append(f"{skill}: metadata.{field} must be an ISO date, got {value!r}")
        return None


def is_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def markdown_targets(text: str) -> set[str]:
    targets: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group("target").strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        else:
            target = target.split(maxsplit=1)[0]
        targets.add(target.split("#", 1)[0])
    return targets


def validate_publication_content(errors: list[str]) -> None:
    root = ROOT.resolve()
    marker_path = ROOT / PRIVATE_MARKER_FILENAME
    private_markers: tuple[str, ...] = ()
    if marker_path.is_file():
        try:
            private_markers = tuple(
                line.strip().casefold()
                for line in marker_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            )
        except UnicodeDecodeError:
            errors.append(f"{PRIVATE_MARKER_FILENAME}: private marker file is not UTF-8")

    for candidate in sorted(ROOT.rglob("*")):
        relative = candidate.relative_to(ROOT)
        if any(part in PUBLICATION_SKIP_PARTS for part in relative.parts):
            continue
        if candidate.name == PRIVATE_MARKER_FILENAME or candidate.name.startswith("worklog"):
            continue
        if not candidate.is_file() or (
            candidate.suffix.lower() not in TEXT_SUFFIXES and candidate.name != "LICENSE"
        ):
            continue
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root):
            errors.append(f"{relative}: publishable file escapes the repository")
            continue
        try:
            contents = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{relative}: publishable text file is not UTF-8")
            continue
        for label, pattern in PUBLICATION_PATTERNS:
            if pattern.search(contents):
                errors.append(f"{relative}: publishable text contains {label}")
        folded = contents.casefold()
        if any(marker in folded for marker in private_markers):
            errors.append(f"{relative}: publishable text contains a configured private marker")


def validate_local_markdown_links(skill_dir: Path, markdown_files: list[Path], errors: list[str]) -> None:
    skill_root = skill_dir.resolve()
    for source in markdown_files:
        try:
            contents = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"{skill_dir.name}: Markdown file is not UTF-8: {error}")
            continue
        for target in markdown_targets(contents):
            if not target or target.startswith("//") or urlparse(target).scheme:
                continue
            candidate = Path(target)
            if candidate.is_absolute():
                errors.append(
                    f"{skill_dir.name}: local Markdown link must be relative: "
                    f"{source.relative_to(skill_dir)} -> {target}"
                )
                continue
            resolved = (source.parent / candidate).resolve()
            if not resolved.is_relative_to(skill_root):
                errors.append(
                    f"{skill_dir.name}: local Markdown link escapes skill directory: "
                    f"{source.relative_to(skill_dir)} -> {target}"
                )
            elif not resolved.exists():
                errors.append(
                    f"{skill_dir.name}: local Markdown link points to a missing target: "
                    f"{source.relative_to(skill_dir)} -> {target}"
                )


def parse_agent_yaml(path: Path) -> dict[str, dict[str, object]]:
    """Parse the shallow mapping subset accepted for agents/openai.yaml."""

    payload: dict[str, dict[str, object]] = {}
    current_section: str | None = None
    nested_key: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            raise ValueError("tabs are not supported in agent metadata")
        indent = len(line) - len(line.lstrip(" "))
        if indent >= 4 and current_section == "dependencies" and nested_key == "tools":
            # Tool dependency entries are validated by the official plugin validator.
            continue
        key, separator, raw_value = line.strip().partition(":")
        if not separator:
            raise ValueError(f"invalid agent metadata line {line!r}")
        if indent == 0:
            if raw_value.strip():
                raise ValueError(f"agent field {key} must be a mapping")
            if key in payload:
                raise ValueError(f"duplicate agent field {key}")
            payload[key] = {}
            current_section = key
            nested_key = None
            continue
        if indent == 2:
            if current_section is None:
                raise ValueError(f"agent field {key} has no parent mapping")
            section = payload[current_section]
            if key in section:
                raise ValueError(f"duplicate agent field {current_section}.{key}")
            if not raw_value.strip():
                section[key] = {}
                nested_key = key
            elif raw_value.strip() in {"true", "false"}:
                section[key] = raw_value.strip() == "true"
                nested_key = None
            else:
                section[key] = parse_string_scalar(raw_value, f"agent.{current_section}.{key}")
                nested_key = None
            continue
        raise ValueError(f"unsupported agent metadata indentation in {line!r}")
    return payload


def validate_agent_manifest(skill_dir: Path, path: Path, errors: list[str]) -> None:
    try:
        payload = parse_agent_yaml(path)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        errors.append(f"{skill_dir.name}: invalid agents/openai.yaml: {error}")
        return
    unknown_top = sorted(set(payload) - AGENT_TOP_LEVEL_FIELDS)
    if unknown_top:
        errors.append(f"{skill_dir.name}: unsupported agent fields: {', '.join(unknown_top)}")
    interface = payload.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{skill_dir.name}: agent interface must be a mapping")
        return
    unknown_interface = sorted(set(interface) - AGENT_INTERFACE_FIELDS)
    if unknown_interface:
        errors.append(
            f"{skill_dir.name}: unsupported agent interface fields: {', '.join(unknown_interface)}"
        )
    for field in ("display_name", "short_description"):
        if not isinstance(interface.get(field), str) or not str(interface[field]).strip():
            errors.append(f"{skill_dir.name}: agent interface.{field} must be a nonempty string")
    for field in ("icon_small", "icon_large"):
        value = interface.get(field)
        if value is None:
            continue
        candidate = (skill_dir / str(value)).resolve()
        if not candidate.is_relative_to(skill_dir.resolve()) or not candidate.is_file():
            errors.append(f"{skill_dir.name}: agent interface.{field} points outside the skill or is missing")
    brand_color = interface.get("brand_color")
    if brand_color is not None and not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(brand_color)):
        errors.append(f"{skill_dir.name}: agent interface.brand_color must use #RRGGBB")
    policy = payload.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            errors.append(f"{skill_dir.name}: agent policy must be a mapping")
        else:
            unknown_policy = sorted(set(policy) - {"allow_implicit_invocation"})
            if unknown_policy:
                errors.append(f"{skill_dir.name}: unsupported agent policy fields: {', '.join(unknown_policy)}")
            value = policy.get("allow_implicit_invocation")
            if value is not None and not isinstance(value, bool):
                errors.append(
                    f"{skill_dir.name}: agent policy.allow_implicit_invocation must be a boolean"
                )
    dependencies = payload.get("dependencies")
    if dependencies is not None and (
        not isinstance(dependencies, dict) or set(dependencies) - {"tools"}
    ):
        errors.append(f"{skill_dir.name}: agent dependencies may contain only tools")


def validate_json(errors: list[str]) -> None:
    manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"plugin manifest: {error}")
        return
    if not isinstance(manifest, dict):
        errors.append("plugin manifest must contain a JSON object")
        return

    unknown_manifest = sorted(set(manifest) - PLUGIN_TOP_LEVEL_FIELDS)
    if unknown_manifest:
        errors.append(f"plugin manifest contains unsupported fields: {', '.join(unknown_manifest)}")

    required_manifest_fields = {
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "skills",
        "interface",
    }
    missing_manifest = sorted(required_manifest_fields - manifest.keys())
    if missing_manifest:
        errors.append(f"plugin manifest missing fields: {', '.join(missing_manifest)}")
    if manifest.get("name") != "apple-engineering-skills":
        errors.append("plugin manifest name must be apple-engineering-skills")
    if manifest.get("skills") != "./skills/":
        errors.append("plugin manifest must discover ./skills/")
    if manifest.get("license") != "MIT":
        errors.append("plugin manifest license must be MIT")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        errors.append("plugin manifest description must be a nonempty string")
    if not SEMVER_RE.fullmatch(manifest.get("version", "") if isinstance(manifest.get("version"), str) else ""):
        errors.append("plugin manifest version must use semantic versioning")
    author = manifest.get("author")
    if not isinstance(author, dict) or not isinstance(author.get("name"), str) or not is_https_url(author.get("url")):
        errors.append("plugin manifest author must contain string name and HTTPS url")
    elif set(author) - {"name", "email", "url"}:
        errors.append("plugin manifest author contains unsupported fields")
    for field in ("homepage", "repository"):
        if not is_https_url(manifest.get(field)):
            errors.append(f"plugin manifest {field} must be an HTTPS URL")
    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not keywords or not all(isinstance(item, str) and item for item in keywords):
        errors.append("plugin manifest keywords must be a nonempty string array")
    skills_path = (PLUGIN / str(manifest.get("skills", ""))).resolve()
    if not skills_path.is_relative_to(PLUGIN.resolve()) or not skills_path.is_dir():
        errors.append("plugin manifest skills path must resolve to a directory inside the plugin")

    interface = manifest.get("interface", {})
    if not isinstance(interface, dict):
        errors.append("plugin manifest interface must be an object")
        interface = {}
    unknown_interface = sorted(set(interface) - PLUGIN_INTERFACE_FIELDS)
    if unknown_interface:
        errors.append(f"plugin interface contains unsupported fields: {', '.join(unknown_interface)}")
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            errors.append(f"plugin interface {field} must be a nonempty string")
    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        if not is_https_url(interface.get(field)):
            errors.append(f"plugin interface {field} must be an HTTPS URL")
    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities or not all(isinstance(item, str) for item in capabilities):
        errors.append("plugin interface capabilities must be a nonempty string array")
    prompts = interface.get("defaultPrompt", interface.get("default_prompt"))
    if not isinstance(prompts, list) or not prompts or not all(isinstance(item, str) and item for item in prompts):
        errors.append("plugin interface defaultPrompt must be a nonempty string array")
    brand_color = interface.get("brandColor")
    if brand_color is not None and (
        not isinstance(brand_color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", brand_color)
    ):
        errors.append("plugin interface brandColor must use #RRGGBB")
    for field in ("composerIcon", "logo", "logoDark"):
        value = interface.get(field)
        if value is None:
            continue
        candidate = (PLUGIN / str(value)).resolve()
        if not candidate.is_relative_to(PLUGIN.resolve()) or not candidate.is_file():
            errors.append(f"plugin interface {field} points outside the plugin or is missing")
    screenshots = interface.get("screenshots")
    if screenshots is not None:
        if not isinstance(screenshots, list):
            errors.append("plugin interface screenshots must be an array")
        else:
            for item in screenshots:
                candidate = (PLUGIN / str(item)).resolve()
                if (
                    not isinstance(item, str)
                    or not candidate.is_relative_to(PLUGIN.resolve())
                    or not candidate.is_file()
                ):
                    errors.append("plugin interface screenshots contains a missing or escaping path")
    if not interface.get("privacyPolicyURL") or not (ROOT / "PRIVACY.md").is_file():
        errors.append("plugin must publish and link a privacy policy")
    if not interface.get("termsOfServiceURL") or not (ROOT / "TERMS.md").is_file():
        errors.append("plugin must publish and link terms")

    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"marketplace manifest: {error}")
        return
    if not isinstance(marketplace, dict):
        errors.append("marketplace manifest must contain a JSON object")
        return
    unknown_marketplace = sorted(set(marketplace) - {"name", "interface", "plugins"})
    if unknown_marketplace:
        errors.append(f"marketplace contains unsupported fields: {', '.join(unknown_marketplace)}")

    if not isinstance(marketplace.get("name"), str) or not marketplace["name"]:
        errors.append("marketplace name must be a nonempty string")
    marketplace_interface = marketplace.get("interface")
    if not isinstance(marketplace_interface, dict) or not isinstance(marketplace_interface.get("displayName"), str):
        errors.append("marketplace interface.displayName must be a string")
    elif set(marketplace_interface) - {"displayName"}:
        errors.append("marketplace interface contains unsupported fields")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        errors.append("marketplace plugins must be an array")
        return
    matches = [entry for entry in plugins if isinstance(entry, dict) and entry.get("name") == manifest.get("name")]
    if len(matches) != 1:
        errors.append("marketplace must contain exactly one apple-engineering-skills entry")
        return
    entry = matches[0]
    if set(entry) - {"name", "source", "policy", "category"}:
        errors.append("marketplace plugin entry contains unsupported fields")
    if entry.get("source") != {"source": "local", "path": "./"}:
        errors.append("marketplace plugin source must point to the repository root")
    if entry.get("category") != interface.get("category"):
        errors.append("marketplace and plugin interface categories must match")
    policy = entry.get("policy", {})
    if not isinstance(policy, dict) or set(policy) - {"installation", "authentication", "products"}:
        errors.append("marketplace plugin policy has unsupported shape")
        policy = {}
    if policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
        errors.append("marketplace entry must declare AVAILABLE and ON_INSTALL policy")

def validate_skill(skill_dir: Path, today: dt.date, max_age: int, errors: list[str]) -> None:
    skill_name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    if not 1 <= len(skill_name) <= 64 or not NAME_RE.fullmatch(skill_name):
        errors.append(f"{skill_name}: directory name is not Agent Skills compatible")
    if not skill_path.is_file():
        errors.append(f"{skill_name}: missing SKILL.md")
        return

    try:
        top, metadata, body = parse_frontmatter(skill_path)
    except (OSError, ValueError) as error:
        errors.append(f"{skill_name}: {error}")
        return

    unknown_top = sorted(set(top) - ALLOWED_TOP_LEVEL)
    if unknown_top:
        errors.append(f"{skill_name}: unsupported frontmatter fields: {', '.join(unknown_top)}")
    if "compatibility" in top:
        errors.append(f"{skill_name}: compatibility is omitted until the Codex validator accepts it")
    if top.get("name") != skill_name:
        errors.append(f"{skill_name}: frontmatter name must match its directory")
    description = top.get("description", "")
    if not 1 <= len(description) <= 1024:
        errors.append(f"{skill_name}: description must contain 1-1024 characters")
    if top.get("license") != "MIT":
        errors.append(f"{skill_name}: license must be MIT")
    if "allowed-tools" in top and not top["allowed-tools"].strip():
        errors.append(f"{skill_name}: allowed-tools must be a nonempty space-delimited string")
    if not body.strip():
        errors.append(f"{skill_name}: instruction body is empty")

    for field in REQUIRED_METADATA:
        if not metadata.get(field):
            errors.append(f"{skill_name}: missing string metadata field {field}")
    if metadata.get("author") != "coryparrry":
        errors.append(f"{skill_name}: metadata.author must be coryparrry")
    if metadata.get("version") and not SEMVER_RE.fullmatch(metadata["version"]):
        errors.append(f"{skill_name}: metadata.version must use semantic versioning")

    dates: dict[str, dt.date] = {}
    for field in ("last-updated", "last-reviewed", "apple-docs-reviewed"):
        if field in metadata:
            parsed = parse_date(metadata[field], field, skill_name, errors)
            if parsed:
                dates[field] = parsed
                if parsed > today:
                    errors.append(f"{skill_name}: metadata.{field} is in the future")

    reviewed = dates.get("last-reviewed")
    docs_reviewed = dates.get("apple-docs-reviewed")
    updated = dates.get("last-updated")
    if reviewed and (today - reviewed).days > max_age:
        errors.append(f"{skill_name}: last review is {(today - reviewed).days} days old (maximum {max_age})")
    if docs_reviewed and (today - docs_reviewed).days > max_age:
        errors.append(
            f"{skill_name}: Apple documentation review is {(today - docs_reviewed).days} days old (maximum {max_age})"
        )
    if reviewed and updated and reviewed < updated:
        errors.append(f"{skill_name}: last-reviewed cannot precede last-updated")

    review_match = re.search(r"(?ms)^## Review\s*$\n(?P<section>.*)$", body)
    if not review_match:
        errors.append(f"{skill_name}: review evidence must be inside SKILL.md under ## Review")
        review_text = ""
    else:
        review_text = review_match.group("section")
        review_lower = review_text.lower()
        for label, field in (
            ("last updated", "last-updated"),
            ("last reviewed", "last-reviewed"),
            ("apple documentation reviewed", "apple-docs-reviewed"),
        ):
            if label not in review_lower or metadata.get(field, "") not in review_text:
                errors.append(f"{skill_name}: inline review must include {label} and its metadata date")
        if "Xcode MCP" not in review_text or "DocumentationSearch" not in review_text:
            errors.append(f"{skill_name}: inline review must record Xcode MCP DocumentationSearch")
        if "references/apple-documentation.md" not in markdown_targets(review_text):
            errors.append(f"{skill_name}: inline review must link references/apple-documentation.md")

    references_dir = skill_dir / "references"
    apple_docs = references_dir / "apple-documentation.md"
    if not apple_docs.is_file():
        errors.append(f"{skill_name}: missing references/apple-documentation.md")
    else:
        docs_text = apple_docs.read_text(encoding="utf-8")
        if "/documentation/" not in docs_text:
            errors.append(f"{skill_name}: Apple documentation reference contains no Xcode documentation URI")
        if "Xcode" not in docs_text or "DocumentationSearch" not in docs_text:
            errors.append(f"{skill_name}: Apple documentation reference must record Xcode MCP DocumentationSearch")
        if not re.search(r"(?is)\bquer(?:y|ies)\b.{0,1600}`[^`]+`", docs_text):
            errors.append(f"{skill_name}: Apple documentation reference must record an exact search query")
        if metadata.get("apple-docs-reviewed", "") not in docs_text:
            errors.append(f"{skill_name}: Apple documentation reference must include its review date")
        if re.search(r"\]\(/documentation/", docs_text):
            errors.append(f"{skill_name}: Apple documentation links must not be root-relative")

    linked_targets = markdown_targets(body)
    allowed_files = {skill_path}
    if references_dir.is_dir():
        for reference in references_dir.rglob("*"):
            if not reference.is_file():
                continue
            allowed_files.add(reference)
            relative_link = reference.relative_to(skill_dir).as_posix()
            if relative_link not in linked_targets:
                errors.append(f"{skill_name}: SKILL.md does not route to {relative_link}")
    for standard_dir in ("scripts", "assets"):
        directory = skill_dir / standard_dir
        if directory.is_dir():
            allowed_files.update(path for path in directory.rglob("*") if path.is_file())
    agent_metadata = skill_dir / "agents" / "openai.yaml"
    if agent_metadata.is_file():
        allowed_files.add(agent_metadata)
        validate_agent_manifest(skill_dir, agent_metadata, errors)
    all_files = sorted(path for path in skill_dir.rglob("*") if path.is_file())
    for path in all_files:
        if path.is_symlink() and not path.resolve().is_relative_to(skill_dir.resolve()):
            errors.append(f"{skill_name}: symlink escapes skill directory: {path.relative_to(skill_dir)}")
    extra_files = sorted(path for path in all_files if path not in allowed_files)
    if extra_files:
        extras = ", ".join(str(path.relative_to(skill_dir)) for path in extra_files)
        errors.append(f"{skill_name}: unsupported skill files: {extras}")

    markdown_files = [path for path in sorted(allowed_files) if path.suffix.lower() == ".md"]
    validate_local_markdown_links(skill_dir, markdown_files, errors)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-review-age-days", type=int, default=90)
    args = parser.parse_args()
    if args.max_review_age_days < 1:
        parser.error("--max-review-age-days must be positive")

    errors: list[str] = []
    validate_publication_content(errors)
    validate_json(errors)
    if not SKILLS.is_dir():
        errors.append("plugin skills directory is missing")
    else:
        skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir() and not path.name.startswith("."))
        if not skill_dirs:
            errors.append("plugin must contain at least one skill")
        today = dt.datetime.now(dt.timezone.utc).date()
        for skill_dir in skill_dirs:
            validate_skill(skill_dir, today, args.max_review_age_days, errors)

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills, plugin manifest, marketplace, and review freshness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
