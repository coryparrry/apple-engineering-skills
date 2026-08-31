# Telemetry contract

Adapt event names to the app while preserving these boundaries:

`typed domain event -> policy -> approved versioned envelope -> local/remote sinks`

`MetricKit report -> selection/sanitization -> approved metric envelope -> local/remote sinks`

Conceptual Swift shape:

```swift
// Component, Outcome, DurationBucket, and ApprovedEventKind are public,
// bounded Sendable/Encodable enums owned by this module.
public enum TelemetryEvent: Sendable {
    case operationFinished(component: Component, outcome: Outcome, duration: DurationBucket)
}

public struct TelemetryPolicy: Sendable {
    public struct ApprovedEnvelope: Sendable, Encodable {
        public let schemaVersion: UInt
        public let event: ApprovedEventKind
        public let component: Component
        public let outcome: Outcome?
        public let duration: DurationBucket?

        // Internal to the dedicated TelemetryPolicyModule.
        init(
            schemaVersion: UInt,
            event: ApprovedEventKind,
            component: Component,
            outcome: Outcome?,
            duration: DurationBucket?
        ) {
            self.schemaVersion = schemaVersion
            self.event = event
            self.component = component
            self.outcome = outcome
            self.duration = duration
        }
    }

    public init() {}

    public func approve(_ event: TelemetryEvent) -> ApprovedEnvelope? {
        switch event {
        case let .operationFinished(component, outcome, duration):
            // Apply range/domain checks here before construction.
            return ApprovedEnvelope(
                schemaVersion: 1,
                event: .operationFinished,
                component: component,
                outcome: outcome,
                duration: duration
            )
        }
    }
}

public protocol TelemetrySink: Sendable {
    func record(_ envelope: TelemetryPolicy.ApprovedEnvelope) async
}
```

Place `TelemetryPolicy`, its event vocabulary, and `ApprovedEnvelope` in a dedicated policy module. The envelope is public so sinks in other modules can receive and encode it, but its initializer remains module-internal; application and exporter modules therefore cannot construct one directly. Do not give the envelope public `Decodable` conformance, because `init(from:)` would reopen external construction. Swift has no friend access that lets an enclosing type call a nested type's `private` initializer, so do not present that pattern as enforceable. Keep unrelated constructors out of the policy module and verify negative external compile fixtures for both direct initialization and decoding. MetricKit uses a separate report policy because it originates outside the domain-event pipeline. Sinks never receive raw events, raw reports, or application objects. Map known errors to bounded enums without a description fallback.

## Allowlist rules

- Allow fields by semantic meaning, not just by key name or primitive type.
- Bound enum domains and numeric ranges. Bucket high-cardinality measurements.
- Normalize app build/version data; exclude local branch or developer suffixes.
- Minimize timestamp precision; treat optional strings as suspicious.
- Version the schema and review new fields before enabling them.

## Integration rules

### OSLog

Use a stable bundle-derived subsystem, static bounded categories, explicit interpolation privacy, and only approved fields. `.public` needs field-level justification. Never format a raw event/dictionary.

Route `OSSignposter` through the same policy. Keep interval/event names and categories static and bounded, allow only approved interpolations/metadata, and treat signpost IDs as correlation state rather than user identity. Sanitize MetricKit custom signpost logs and diagnostic `signpostData` before any sink.

### MetricKit ingress

Use `MetricManager.metricReports` and `diagnosticReports` when available; otherwise use the legacy `MXMetricManager` subscriber API required by the supported toolchain/deployment target. Keep observation alive as the chosen API requires. Select/sanitize needed measurements into a distinct approved metric envelope, treat diagnostics as sensitive, and never forward a raw report.

### OTLP-style export

Translate only from the envelope. Allowlist resource attributes, names, and values; disable unreviewed auto-instrumentation/baggage; cap queues, batches, retries, and disk lifetime. Drop safely when disabled, over policy, full, or unknown. Never dump failed request bodies or headers.

## Debug diagnostics

Use a separate, preferably release-excluded debug type/sink rather than widening production. Any exceptional raw capture needs explicit authorization, visible state, local-only expiring storage, and deliberate export; never fold it into telemetry.
