# Package boundaries

Use when editing the manifest, module graph, resources, or binary distribution.

## Manifest and modules

Review consumer impact from tools version, Swift language modes/settings, product/module names, target kinds, linkage, explicitly declared platform floors, dependency requirements, conditional targets, and resources. Inspect the evaluated manifest, then build each supported conditional graph. If `platforms` is omitted, SwiftPM supplies defaults; record them as toolchain behavior rather than silently advertising them as tested support.

- Expose the smallest coherent module graph consumers need.
- Keep replaceable concrete adapters internal and stable contracts low-dependency.
- Avoid cycles through tests, generators, or umbrella modules.
- Give SPI an audience and stability policy; do not promise underscored re-exports.
- Review generated interfaces and documentation as a consumer.

For each dependency, record its target, escaped public types, version/platform constraints, and transitive licenses, resources, privacy declarations, or binaries. Resolve a clean external fixture because workspaces can supply undeclared siblings or cached state.

Treat a reusable library's `Package.resolved` as development evidence for that checkout, not a downstream pin. A consuming top-level package resolves the library's declared requirement ranges into its own graph, so verify representative lower/upper selections and record the consumer-selected graph.

## Resources and binaries

Resources are target-scoped. Process files needing platform handling/localization; copy files whose layout or bytes must remain unchanged. In Swift code for a target that declares resources, use SwiftPM's synthesized `Bundle.module`, not `Bundle.main`; keep lookup behind that target's API rather than assuming a consumer can access its bundle token. Test name case, localization, and loading from a consuming app.

For XCFramework or remote binaries, verify checksum and source provenance, promised slices/floors, interfaces/headers, linkage, dependencies, resources, signatures, and clean-consumer launch. If binary compatibility is promised, use library evolution as appropriate and run a previously built client against the replacement; source compatibility is insufficient.
