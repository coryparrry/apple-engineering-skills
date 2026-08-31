# Apple Engineering Skills

![Apple Engineering Skills](https://img.shields.io/badge/Apple-Engineering_Skills-111827?style=for-the-badge&logo=apple&logoColor=white)
![13 Agent Skills](https://img.shields.io/badge/Agent_Skills-13-2563eb?style=for-the-badge)
![MIT License](https://img.shields.io/badge/License-MIT-16a34a?style=for-the-badge)
[![skills.sh](https://skills.sh/b/coryparrry/apple-engineering-skills)](https://skills.sh/coryparrry/apple-engineering-skills)

> Thirteen production-oriented Agent Skills for building, diagnosing, validating, and shipping Apple-platform software.

These are narrow engineering playbooks for the hard boundaries that generic framework tutorials miss: state ownership, privacy, permissions, lifecycle, runtime evidence, release provenance, and authoritative data.

Every Apple API claim is reviewed through Xcode MCP `DocumentationSearch`. Each skill keeps its main routing in `SKILL.md` and loads detailed procedures only when they apply.

## 🚀 Install

### Codex plugin

1. Open **Plugins** in Codex.
2. Select **Add marketplace**.
3. Add `https://github.com/coryparrry/apple-engineering-skills`.
4. Install **Apple Engineering Skills**.
5. Start a new task so Codex discovers the installed skills.

CLI alternative:

```bash
codex plugin marketplace add coryparrry/apple-engineering-skills
codex plugin add apple-engineering-skills@coryparrry-apple-engineering-skills
```

For local plugin development, add this repository's absolute path as the marketplace source instead.

### skills.sh

Install all thirteen skills for Codex:

```bash
npx skills add coryparrry/apple-engineering-skills --global --agent codex --skill '*'
```

Install one skill:

```bash
npx skills add coryparrry/apple-engineering-skills --global --agent codex --skill swift-concurrency-runtime
```

Replace the final slug with any skill from the catalogue below. The same repository can be installed for other supported agents through the [`skills` CLI](https://skills.sh/docs/cli).

## ✨ Skills

| Category | Need | Skill | What it does |
|---|---|---|---|
| Intelligence & Media | Ship an on-device generative feature. | [`apple-foundation-models-production`](skills/apple-foundation-models-production/) | Bounds Foundation Models availability, tools, guided output, attachments, privacy, and fallbacks. |
| Intelligence & Media | Decode, analyze, and encode images safely. | [`apple-vision-image-pipeline`](skills/apple-vision-image-pipeline/) | Defines byte, pixel, memory, orientation, color, OCR, and output-validation contracts. |
| App Reliability | Protect durable application data. | [`apple-persistence-integrity`](skills/apple-persistence-integrity/) | Covers SwiftData ownership, bounded reads, migrations, recovery, and cross-store integrity. |
| App Reliability | Add useful diagnostics without collecting content. | [`apple-privacy-telemetry`](skills/apple-privacy-telemetry/) | Designs bounded OSLog, MetricKit, and OTLP telemetry with closed privacy policy. |
| App Reliability | Prove a performance change at runtime. | [`apple-runtime-performance-proof`](skills/apple-runtime-performance-proof/) | Binds source, artifact, process, scenario, traces, and before/after evidence. |
| App Reliability | Make asynchronous work predictable. | [`swift-concurrency-runtime`](skills/swift-concurrency-runtime/) | Defines ownership, admission, cancellation, reentrancy, deadlines, streams, and shutdown. |
| macOS Systems | Build or diagnose an Accessibility client. | [`macos-accessibility-tcc`](skills/macos-accessibility-tcc/) | Handles TCC, AX ownership, secure fields, observer teardown, and target relaunch. |
| macOS Systems | Bridge SwiftUI and AppKit lifecycle correctly. | [`macos-app-lifecycle-bridge`](skills/macos-app-lifecycle-bridge/) | Assigns owners for windows, panels, menus, status items, event monitors, and teardown. |
| macOS Systems | Protect local IPC and MCP integrity. | [`macos-local-ipc-integrity`](skills/macos-local-ipc-integrity/) | Covers framing, authorization, replay, backpressure, durable commit, and privacy. |
| macOS Systems | Make screen capture consent and lifecycle reliable. | [`macos-screen-capture-lifecycle`](skills/macos-screen-capture-lifecycle/) | Handles ScreenCaptureKit permissions, ownership, teardown, restart, and runtime proof. |
| Distribution | Prove what source actually shipped and ran. | [`apple-release-provenance`](skills/apple-release-provenance/) | Reconciles source, archive, export, publication, download, install, signing, and runtime. |
| Distribution | Maintain a trustworthy Swift package contract. | [`swift-package-contracts`](skills/swift-package-contracts/) | Reviews public API, compatibility, consumer proof, binary delivery, and versioned releases. |
| Game Services | Keep valuable game state authoritative. | [`apple-authoritative-game-systems`](skills/apple-authoritative-game-systems/) | Designs deterministic server state, Game Center identity, App Attest, StoreKit, and offline reconciliation. |

## 🧰 Repository Surfaces

| Surface | Purpose |
|---|---|
| [`skills/`](skills/) | Portable Agent Skills and their focused references. |
| [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | Codex plugin metadata and skill discovery. |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | Codex marketplace entry for this repository-root plugin. |
| [`skills.sh.json`](skills.sh.json) | Category and ordering metadata for the skills.sh repository page. |
| [`scripts/validate_repository.py`](scripts/validate_repository.py) | Offline publication, packaging, routing, and review-freshness checks. |

The repository is the plugin root. There is no nested plugin copy and no mirrored skill tree.

## 🧪 Validation

```bash
python3 scripts/validate_repository.py
python3 -m unittest scripts/test_validate_repository.py
python3 -m json.tool skills.sh.json >/dev/null
npx skills add . --list
```

The validator uses Python's standard library. It checks the repository's supported Agent Skills contract, plugin and marketplace manifests, routed references, publication-sensitive text, Xcode review evidence, and review freshness.

A passing validator does not replace technical review or runtime proof. Apple framework claims remain bound to the dated Xcode documentation evidence in each skill.

## 🛡️ Security and Privacy

The bundle contains instructions and references, not a network service, account system, analytics client, or datastore. Skills do not grant authority to upload private data, mutate production systems, reset permissions, or publish artifacts.

Review the [privacy policy](PRIVACY.md) and [terms](TERMS.md) before using the skills with sensitive projects. Report repository issues through GitHub.

## 📄 License

MIT. See [LICENSE](LICENSE).
