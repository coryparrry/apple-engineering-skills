# Release evidence ledger

Use one row per observable transformation. Preserve raw evidence by immutable path, CI artifact ID, or attached command output; never record credentials or private keys.

## Header

Record the claim/channel, exact source revision and dirty/generated inputs, review time, CI/build identity, Xcode/SDK, configuration, architectures, dependency locks, export options, and reproducibility limits.

## Boundaries

| Stage | Unique identity evidence | Locator/channel corroboration | Signing/capability evidence | Channel/transaction evidence | Parent/process | Status | Evidence |
|---|---|---|---|---|---|---|---|
| Source | commit + dirty-input/tree digest | remote + checkout | intended entitlements | — | source checkout | — | — |
| Archive | archive/executable digests | CI artifact ID + build metadata | signature + effective entitlements | — | source + CI | — | — |
| Export | package/executable digests | bundle ID + version/build + export record | distribution identity + requirement + entitlements/profile | export method | archive + export options | — | — |
| Published | provider immutable artifact/build ID and upload digest when observable | provider/channel locator | provider acceptance, notarization, or appcast state as applicable | provider record | export | — | — |
| Downloaded | package/executable digest | origin + delivered version | delivered/update signature | verified channel/update record | published artifact | — | — |
| Installed | executable digest or code-directory hash when observable | canonical path or device-visible build ID | installed signature, requirement, and effective entitlements | verified delivered receipt/transaction fields when observable | installer/channel | — | — |
| Running | executable digest, code-directory hash, UUID, or diagnostic build ID when observable | process path + app-reported version/build | runtime code identity/capability | verified `AppTransaction` fields when observable | installed/channel build | — | — |

Statuses: `proven`, `expected-transformation`, `unproven`, `contradicted`, `not-applicable`.

## Evidence rules

- Source: revision, dirty state, locks, version/build inputs, generated-source origin.
- Build/export: artifact ID/digest, architecture, bundle metadata, authorities/team, requirement, entitlements/profile, important nested code.
- Delivery/install: provider build/notarization/appcast/receipt evidence; on macOS, fresh canonical-bundle inspection; on restricted platforms, record the unobservable boundary.
- Runtime: strongest attainable build/process binding and explicitly bound observations.

A locator, path, origin, or matching version is corroboration, not unique binary identity. If the claim requires unique delivered or running binary identity and no digest, code-directory hash, verified provider identifier, UUID, or equivalent is observable, mark that boundary `unproven`. Basic signature validity proves sealed-code integrity and satisfaction of the checked requirement; it does not by itself prove fitness for a platform or distribution channel, source revision, notarization, or Gatekeeper acceptance. A notarization ticket proves acceptance of the submitted artifact, not installation of the intended build.
