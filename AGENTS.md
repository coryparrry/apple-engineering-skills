# Repository instructions

This repository publishes generic Agent Skills for Apple-platform engineering.

## Source and scope

- Use Xcode MCP `DocumentationSearch` as the primary source for Apple framework and API guidance.
- Record the review date and evidence method in the skill's own `## Review` section; keep the consulted Apple documentation URIs in `references/apple-documentation.md`.
- Use official OpenAI documentation and the repository validators for Codex plugin packaging.
- Do not copy third-party skill text. Comparative repositories may identify omissions, but instructions here must be original.
- Do not introduce private project names, local absolute paths, customer data, or product-specific policy.

## Skill contract

- Follow the Agent Skills specification: lowercase hyphenated directory name matching the `name` in `SKILL.md`.
- Keep shared constraints and routing in `SKILL.md`. Use focused `references/` for substantial procedures and documentation that should load only when relevant.
- Include `license` and string-valued `metadata` fields for `author`, `version`, `last-updated`, `last-reviewed`, and `apple-docs-reviewed`.
- The open standard permits an optional top-level `compatibility` field, but omit it until Codex's validator accepts it; the README and skill body remain authoritative.
- Link every reference from `SKILL.md` and avoid duplicated guidance, standalone review files, or unrelated auxiliary documentation.
- Encode non-obvious production invariants, evidence boundaries, and stopping conditions. Avoid generic tutorials and universal rules based on one incident.
- When adding or removing a shipped skill, update the README count and catalogue, plugin keywords when relevant, and `skills.sh.json` in the same change.

## Review contract

- A date changes only after the corresponding content or documentation has actually been reviewed.
- Updating `apple-docs-reviewed` requires a fresh Xcode MCP documentation pass.
- Keep a compact `## Review` record in the same `SKILL.md`, including dates, scope, Xcode MCP method, and a link to its Apple documentation evidence reference.
- Run `python3 scripts/validate_repository.py` before committing.
