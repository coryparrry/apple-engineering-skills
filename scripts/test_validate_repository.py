#!/usr/bin/env python3
"""Focused regression tests for the repository validator."""

from __future__ import annotations

import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import validate_repository as validator


TODAY = dt.date(2026, 8, 30)


class ValidatorTests(unittest.TestCase):
    def make_repository_manifests(self, root: Path) -> tuple[Path, dict[str, object]]:
        plugin = root
        (plugin / ".codex-plugin").mkdir(parents=True)
        (plugin / "skills").mkdir()
        (root / ".agents" / "plugins").mkdir(parents=True)
        (root / "PRIVACY.md").write_text("privacy\n")
        (root / "TERMS.md").write_text("terms\n")
        manifest: dict[str, object] = {
            "name": "apple-engineering-skills",
            "version": "0.1.0",
            "description": "Fixture plugin",
            "author": {"name": "Fixture", "url": "https://example.com/author"},
            "homepage": "https://example.com/plugin",
            "repository": "https://example.com/repository",
            "license": "MIT",
            "keywords": ["swift"],
            "skills": "./skills/",
            "interface": {
                "displayName": "Fixture",
                "shortDescription": "Fixture plugin",
                "longDescription": "Fixture plugin for validator tests.",
                "developerName": "Fixture",
                "category": "Developer Tools",
                "capabilities": ["Interactive"],
                "websiteURL": "https://example.com/plugin",
                "privacyPolicyURL": "https://example.com/privacy",
                "termsOfServiceURL": "https://example.com/terms",
                "defaultPrompt": ["Validate this fixture."],
            },
        }
        marketplace = {
            "name": "fixture-marketplace",
            "interface": {"displayName": "Fixture"},
            "plugins": [
                {
                    "name": "apple-engineering-skills",
                    "source": {
                        "source": "local",
                        "path": "./",
                    },
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Developer Tools",
                }
            ],
        }
        (root / ".agents" / "plugins" / "marketplace.json").write_text(
            json.dumps(marketplace)
        )
        return plugin, manifest

    def make_skill(
        self,
        root: Path,
        name: str = "valid-skill",
        *,
        extra_frontmatter: str = "",
        apple_link: str = "references/apple-documentation.md",
    ) -> Path:
        skill = root / name
        references = skill / "references"
        references.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"""---
name: {name}
description: A focused validation fixture.
license: MIT
{extra_frontmatter}metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Valid skill

Read [Apple evidence]({apple_link}).

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

Reviewed with Xcode MCP `DocumentationSearch`; see [Apple evidence]({apple_link}).
""",
            encoding="utf-8",
        )
        (references / "apple-documentation.md").write_text(
            """# Apple documentation review

Reviewed with Xcode MCP `DocumentationSearch` on 2026-08-30.
Fresh query: `Example API availability`.

- `/documentation/Example/ExampleAPI`
""",
            encoding="utf-8",
        )
        return skill

    def validate(self, skill: Path) -> list[str]:
        errors: list[str] = []
        validator.validate_skill(skill, TODAY, 90, errors)
        return errors

    def test_rejects_non_string_frontmatter_scalars(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            path = skill / "SKILL.md"
            path.write_text(path.read_text().replace('author: "coryparrry"', "author: true"))
            with self.assertRaisesRegex(ValueError, "must be a string scalar"):
                validator.parse_frontmatter(path)

    def test_rejects_names_longer_than_64_characters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory), "a" * 65)
            self.assertTrue(any("directory name" in error for error in self.validate(skill)))

    def test_rejects_repo_unsupported_compatibility_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory), extra_frontmatter="compatibility: Codex\n")
            errors = self.validate(skill)
            self.assertTrue(any("compatibility is omitted" in error for error in errors))

    def test_allows_agent_skills_allowed_tools_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(
                Path(directory),
                extra_frontmatter='allowed-tools: "Bash(git:*) Read"\n',
            )
            self.assertEqual(self.validate(skill), [])

    def test_strict_semver_rejects_empty_and_leading_zero_identifiers(self) -> None:
        self.assertIsNone(validator.SEMVER_RE.fullmatch("1.0.0-.."))
        self.assertIsNone(validator.SEMVER_RE.fullmatch("1.0.0-01"))
        self.assertIsNotNone(validator.SEMVER_RE.fullmatch("1.0.0-alpha.1+build.01"))

    def test_rejects_unknown_plugin_and_interface_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin, manifest = self.make_repository_manifests(root)
            manifest["unexpected"] = True
            interface = manifest["interface"]
            assert isinstance(interface, dict)
            interface["unexpected"] = True
            (plugin / ".codex-plugin" / "plugin.json").write_text(json.dumps(manifest))
            with (
                mock.patch.object(validator, "ROOT", root),
                mock.patch.object(validator, "PLUGIN", plugin),
            ):
                errors: list[str] = []
                validator.validate_json(errors)
            self.assertTrue(any("unsupported fields" in error for error in errors))
            self.assertTrue(any("interface contains unsupported" in error for error in errors))

    def test_allows_standard_skill_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            (skill / "scripts").mkdir()
            (skill / "scripts" / "check.py").write_text("print('ok')\n")
            (skill / "assets").mkdir()
            (skill / "assets" / "fixture.bin").write_bytes(b"fixture")
            (skill / "agents").mkdir()
            (skill / "agents" / "openai.yaml").write_text(
                'interface:\n  display_name: "Valid Skill"\n'
                '  short_description: "Validate a fixture"\n'
            )
            self.assertEqual(self.validate(skill), [])

    def test_rejects_incomplete_agent_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            (skill / "agents").mkdir()
            (skill / "agents" / "openai.yaml").write_text("interface: {}\n")
            errors = self.validate(skill)
            self.assertTrue(any("invalid agents/openai.yaml" in error for error in errors))

    def test_reference_routing_requires_an_exact_markdown_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(
                Path(directory),
                apple_link="references/apple-documentation.md.backup",
            )
            errors = self.validate(skill)
            self.assertTrue(any("does not route" in error for error in errors))
            self.assertTrue(any("inline review must link" in error for error in errors))

    def test_rejects_an_extra_missing_local_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            path = skill / "SKILL.md"
            path.write_text(path.read_text() + "\nRead [missing](references/missing.md).\n")
            errors = self.validate(skill)
            self.assertTrue(any("missing target" in error for error in errors))

    def test_rejects_an_escaping_local_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            path = skill / "SKILL.md"
            path.write_text(path.read_text() + "\nRead [outside](../outside.md).\n")
            errors = self.validate(skill)
            self.assertTrue(any("escapes skill directory" in error for error in errors))

    def test_checks_publication_content_outside_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local_path = "/" + "Users" + "/example/Private/file.txt"
            (root / "README.md").write_text(f"Local file: {local_path}\n")
            with mock.patch.object(validator, "ROOT", root):
                errors: list[str] = []
                validator.validate_publication_content(errors)
            self.assertTrue(any("local Unix user path" in error for error in errors))

    def test_checks_untracked_private_marker_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".publication-private-markers").write_text("internal-codename\n")
            (root / "README.md").write_text("About Internal-Codename\n")
            with mock.patch.object(validator, "ROOT", root):
                errors: list[str] = []
                validator.validate_publication_content(errors)
            self.assertTrue(any("configured private marker" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
