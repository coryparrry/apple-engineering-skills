# Verification and release

Use when validating changes or preparing a tag.

| Evidence | Proves | Does not prove |
|---|---|---|
| manifest inspection | declared graph | conditional builds |
| package tests | local behavior | consumer/host integration |
| external fixture | resolution/import/calls | entitlement/runtime installation |
| schema fixtures | tested wire history | future inputs |
| app-hosted tests | bundle/lifecycle/permissions | other host combinations |
| old binary client | tested replacement | source/toolchain compatibility |

Common checks include `swift package dump-package`, `swift package describe`, `swift build`, and `swift test`. API-breaking diagnostics against an exact baseline are one signal, not a substitute for schema, behavior, concurrency, or host tests.

An external fixture lives outside the package under review, depends on the public product, imports documented modules, and exercises representative generics, protocols, async calls, and availability. Resolve the exact reviewed Git tag/commit or packaged artifact in at least one clean fixture; a local path can speed development but cannot prove dependency resolution or published contents. Clear or isolate caches when they could mask undeclared dependencies. If an in-package test is also used for access checking, avoid `@testable` and set `testTarget(packageAccess: false)` where that manifest API is available, because its default is `true`.

`Package.resolved` records the graph selected by a top-level/leaf package. A reusable library's resolution file does not pin versions when a downstream consumer resolves that library. Validate manifest requirement ranges and at least one downstream clean resolution independently; record the selected graph at the consumer boundary.

## Version and provenance

Apply the declared policy: major for incompatible contracts, minor for backward-compatible capability, patch for backward-compatible correction. Define pre-1.0 compatibility. Record source/baseline commits, clean state, manifest/dependency evidence, impact, test matrix, checksums/provenance, omissions, and migrations. Tag only the reviewed artifact's source.

## Stop conditions

Do not recommend release if the baseline/impact is unknown; durable schema changes lack old fixtures or an explicit break; public `@unchecked Sendable` lacks proof; only `@testable` or package-access-enabled in-package tests cover advertised API; host behavior has only package evidence; binaries lack provenance or promised contents; advertised graphs were not built; or version contradicts impact. Report the gap and narrowest closing check.
