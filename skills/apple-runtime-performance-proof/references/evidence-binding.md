# Evidence binding and claim boundaries

## Provenance record

Capture claim-relevant fields. Prefer attached machine-readable output over hand-copied prose.

- **Source:** repository, commit, branch, relevant changes, dependencies, flags.
- **Artifact:** product/executable paths, bundle/version/build/configuration/SDK/architecture, hash or UUID, signing/sandbox, matching dSYM.
- **Runtime:** executable path from the live PID, start/parent/host, same-name instances, helpers, container/permissions, device/OS/thermal/profiler state.
- **Scenario:** preconditions, data, steps, markers, repetitions, cache/network state, correctness guardrails.
- **Measurement:** tool/version, trace, target, window, sampling, symbolication, filters, aggregation, exclusions.

## Identity checks

Inspect bundle metadata, hashes, Mach-O UUIDs, signing, and the live PID's executable path. Never assume the built product is the installed product.

Store provenance beside every trace. A filename like “after” proves no identity.

## Attribution across processes

Map user action to app coordination, helper/provider work, and app commit. Measure each dominant node. For spawned processes, capture start, nonsecret identity, exit, duration, and resource use. For indirect services, combine signposts and system traces; label correlation unless stronger evidence proves causality.

Avoid app-side fixes for unavoidable provider cost. Repeated provider calls can still reveal an app scheduling bug.

## Boundary report

When proof stops, state observed facts, missing identity/process/permission/symbols/scenario, and the maximum safe conclusion.

Compilation proves build compatibility, not responsiveness. Simulator evidence does not prove device energy use, and a different binary UUID breaks source-to-runtime identity.
