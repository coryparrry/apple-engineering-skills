# Telemetry privacy verification

Test the policy boundary and each real sink. Prefer decoded exports/captured test transports to mock call counts.

## Required negative cases

- Reject/drop unknown events, fields, enum values, types, and schema versions.
- Prevent arbitrary strings entering through errors, attributes, metadata, baggage, or fallbacks.
- Exclude descriptions, URLs, bodies/headers, paths/titles, recognized text, model payloads, media, tokens, and stable IDs from local and remote sinks.
- Reject a forbidden value under a safe-looking key and its hash; blocklists and hashing are insufficient.
- Ensure encoding/transport/retry failures never print or persist raw inputs.
- Disabled telemetry neither exports nor builds a later-upload queue.
- Prove release configuration cannot invoke debug-only raw diagnostics.

Use unmistakable synthetic canaries and assert absence from envelopes, network requests, buffers, and diagnostics.

## Positive and boundary cases

- Compile a separate feature/exporter fixture against the dedicated policy module. It must be able to instantiate `TelemetryPolicy`, approve an event, and receive/encode `ApprovedEnvelope`, but fail to construct an envelope through the module-internal initializer or a decoder.
- Approved events contain only the expected version/fields; ranges are capped or bucketed.
- Version/build normalization rejects branch/developer content.
- OSLog and OTLP originate from the same approved schema/policy; a sink may apply a stricter projection and further minimization.
- Signpost names, metadata, IDs, custom metric logs, and diagnostic `signpostData` contain only approved bounded values.
- Queue, retry, retention, offline, enablement/consent, and schema-migration limits hold.

## Release evidence

Record enabled sinks/endpoints, feature flags/defaults, third-party SDK configuration, sanitized captured export, manifest/disclosure review, and backend retention/deletion/access controls. Static review cannot prove provider-side behavior; mark it as an external evidence boundary.
