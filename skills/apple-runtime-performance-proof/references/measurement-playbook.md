# Measurement playbook

## Match the tool to the question

- **CPU/hangs:** Time Profiler and responsiveness tools; add thread/system traces for waits or child work. Correlate signposts to explain repetition.
- **Memory:** distinguish leaks, retained growth, peaks, and pressure. Use Allocations, Leaks, Memory Graph, or VM tools, then repeat the release lifecycle.
- **Launch:** distinguish cold, warm, resume, and harness launch; measure visible readiness under stable data and diagnostics.
- **Responsiveness:** mark semantic start/completion; correlate main thread, rendering, and providers; inspect distributions.
- **Energy:** use platform-supported hardware/tooling, record power/thermal/charging state, and correlate CPU, wakes, networking, GPU, disk, and background work. For Power Profiler, verify the device/OS is supported, target the app rather than All Processes when app-specific metrics are required, do not use an overall-system-power value recorded while charging, and never compare power-impact values across different device models.

## Signpost contract

Name intervals for stable operations such as `Refresh` or `Capture`; put per-operation values in IDs or metadata.

For overlap, retain a distinct ID and interval state, end the matching name once, and emit separate admission/cancellation/discard/terminal events when relevant.

Use static names and privacy-safe, low-cardinality metadata. Verify intervals in Instruments before relying on them.

## Comparable before and after runs

Hold hardware, OS, build configuration, compiler/SDK settings, architecture, diagnostics, data, cache, network, permissions, scenario, window, profiler, repetitions, and aggregation constant. The before/after artifacts necessarily differ by source revision; bind and record both identities.

Keep raw samples and compare representative repetitions, not a favorable run. Verify output, cancellation, and cleanup with the metric.

## MetricKit interpretation

Use MetricKit for field distributions and diagnostics. Route by platform, SDK, and deployment target: retain and consume modern `MetricManager` report streams where available, otherwise use the legacy `MXMetricManager` subscriber API. Do not refer to interval/state entries on a platform or target that exposes only the legacy reports.

Before attribution, inspect environment/version, handle periods spanning versions, distinguish TestFlight/production, compare adequate rollout windows, and preserve device/state context and dSYMs.

Metric reports are aggregated and delivered on a system schedule, at most daily. Diagnostic reports are discrete event-based deliveries on supported systems and have a separate lifecycle. Both support field hypotheses and incident evidence, not exact local replay or causation by themselves.

## XCTest performance metrics

Choose the metric that matches the claim and read its semantics before interpreting the number. `XCTClockMetric` measures elapsed clock time, including idle time and unrelated scheduling within the measurement boundary. `XCTMemoryMetric` reports the before/after physical-memory difference, not peak memory or a leak diagnosis.

Keep setup outside the measured block unless setup is part of the claim. Use stable iterations, inputs, launch/cache state, and baseline configuration; preserve per-iteration results and investigate variance rather than accepting one favorable aggregate. XCTest measurements prove only the exercised test boundary, so use Instruments or runtime counters for peaks, attribution, lifecycle retention, and provider work.

## Minimum proof by claim type

| Claim | Minimum persuasive evidence |
|---|---|
| “This function is a CPU hotspot” | Symbolicated samples in the exact process during the scenario |
| “This change reduced the CPU storm” | Comparable before/after process timelines, operation counts, and child correlation |
| “The leak is fixed” | Repeated lifecycle with bounded live allocations and released ownership path |
| “Launch improved” | Repeated same-class launches to the same readiness point on bound artifacts |
| “Field performance improved” | Version-segmented MetricKit/Organizer trend plus rollout and environment context |
| “The app caused provider load” | Request/protocol identity, verified workload-bound spawn/parentage, or equivalent causal tracing; timestamp/signpost correlation alone supports only “provider work overlapped the app operation” |
