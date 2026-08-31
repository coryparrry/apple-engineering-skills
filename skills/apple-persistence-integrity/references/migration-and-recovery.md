# Migration and Recovery

Read this before changing schemas, container construction, startup fallback, or data-reset behavior.

## Migration Review

Keep a ledger of every supported released schema, app version, model set, and configuration. Keep released `VersionedSchema` definitions immutable and ensure every supported origin has a tested, ordered path to the destination.

Classify changes as lightweight, explicit rename, custom transformation supported by the exact SDK, or destructive product change. A split/merge may require intermediate schemas, external preprocessing, or export/import; do not assume SwiftData custom stages can express it or conflate them with Core Data staged/manual migration. Test with file-backed stores created by each released schema; recreating a fixture with today's models is not upgrade evidence.

## Failure Triage

Capture the error chain, schema/plan version, configuration, resolved store URL, reachability/permissions/capacity, migration phase, and competing-owner possibility without exposing user content. Retry only after a verified transient condition changes.

Use the least destructive recovery:

1. Correct configuration/lifecycle without touching data.
2. Retry once after a proven transient clears.
3. Enter an explicitly supported read-only or degraded mode.
4. After stopping every store owner, create a coherent store-aware snapshot for quarantine/export that includes required journals/sidecars; never copy one live SQLite file and assume it is complete.
5. Rebuild only a proven derived store.
6. Reset authoritative data only with explicit authorization.

Never silently replace a failed durable store with an in-memory container.

## Evidence

Open and migrate each released fixture, assert identities/relationships/values/deletes, then reopen it to prove durability. Also verify failed multi-step mutation rollback, idempotent duplicate replay, partial cross-store recovery after restart, delete semantics, bounded queries at realistic scale, and unavailable/damaged-store behavior. Preserve real failing fixtures during incident diagnosis.
