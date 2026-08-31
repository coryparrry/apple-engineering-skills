# Public contracts

Use when modifying exported API, Codable data, availability, or concurrency semantics.

| Dimension | Example failure | Minimum evidence |
|---|---|---|
| source | overload ambiguity | compile old client source |
| binary | changed symbol/ABI | old binary client + new library |
| wire | changed encoded meaning | cross-version fixtures |
| behavior | error/order change | contract test and release note |
| concurrency | new actor boundary | strict client build/runtime test |
| availability | API exceeds platform floor | minimum-target build/runtime |

Review removals, renames, protocol requirements, associated types, exhaustive enums, constraints, defaults, errors, cancellation, and actor annotations. Additions can change overload resolution or inference.

## Codable

Synthesis couples stored properties to encoding. For durable data, use explicit keys and test old-to-new, new-to-old, current, and malformed payloads.

- Preserve historical bytes/text; recreating an old model with new code proves nothing.
- Give absent fields semantic defaults; decode old/new renamed keys but encode one key.
- Define unknown-enum behavior; preserve units, timestamps, locale, and precision.
- Version before interpreting changed meaning; never persist localized errors as protocol data.

## Concurrency and availability

`Sendable`, actors, `async`, `@Sendable` closures, callback execution, cancellation, and one-result completion affect clients. For public `@unchecked Sendable`, record protected state, synchronization, all mutation paths, and why checking cannot express the proof. Test actor changes across supported toolchains, language modes, and concurrency-setting combinations, especially default actor isolation and upcoming-feature state.

Manifest platforms constrain the graph; declaration availability constrains calls. Keep newer types out of older signatures, compile at the advertised floor, and run fallbacks on the oldest relevant runtime. Raising the floor is a consumer break.
