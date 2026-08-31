# Store Boundaries

Read this when SwiftData coexists with SQLite, files, caches, indexes, or a remote authority.

## SwiftData Boundary

- Give production `ModelContainer` construction one composition-root owner; inject the container or a narrow service.
- Keep schema, migration plan, configurations, store URLs, and test/in-memory mode explicit.
- Treat the SwiftUI environment context as main-actor UI state. Use an isolated service or `@ModelActor` for other persistence work.
- Move domain IDs, non-temporary `PersistentIdentifier`s, or immutable `Sendable` snapshots across actor boundaries, not live models or contexts. A newly inserted model's identifier is temporary until a successful save; never persist it or place it in a durable map, and refetch by stable identity in the destination context.
- For a durable business operation, use a clean/dedicated context, disable or deliberately account for autosave, validate first, mutate within one isolation domain, save once at the intended commit point, and roll back only that operation's pending changes. `save`, `transaction`, and `rollback` affect the context's full pending-change set.
- Use predicates, stable sorts, `fetchLimit`, batch-size fetches, `fetchCount`, or identifier-only fetches instead of materializing an unbounded store. Before batching, save/rollback or deliberately configure pending-change behavior and test the descriptor's documented failure cases.

## Classify Every Copy

Choose one authority per durable fact. Classify every other copy as a rebuildable projection, disposable cache, lookup index, conflict-managed mirror, or independent record. Record stable identity, propagation direction, delete semantics, and repair policy.

## Choose a Cross-Store Protocol

- **Projection:** commit the authority, then update a copy that tolerates lag and can be rebuilt.
- **Outbox:** commit the mutation and a pending action in the same store; apply the second write with a stable operation ID.
- **Reconciliation:** compare stable IDs plus a version/digest and repair deterministically.
- **Compensation:** record a new durable reversal when the business operation defines one.

For every step boundary, specify what remains committed after process exit, how relaunch discovers it, why replay is idempotent, and how stale replay is rejected. Do not hold a SwiftData transaction open across another database, IPC call, or network request.

## Custom SQLite Rules

- Give each connection or pool one owner and shutdown path.
- Never query or mutate SwiftData's private SQLite schema.
- Coordinate stores with application IDs and journals, not file-layout assumptions.
- Define whether backup, reset, and import operate on both stores, rebuild a projection, or reconcile afterward.
- Preserve partial-commit evidence when automated repair fails.

## Store-file and Core Data boundaries

- Treat a SwiftData/Core Data SQLite store and its sidecars as one live database, not one copyable file. A coherent diagnostic export or quarantine requires exclusive ownership and a store-aware coordinator operation or another proven database snapshot mechanism.
- Do not claim that `NSFileCoordinator` alone makes a live database snapshot consistent; it coordinates file access, not the database transaction/WAL boundary.
- When Core Data coexists directly, route its lightweight, staged, or manual migration separately from SwiftData `MigrationStage`. Verify the exact store type, coordinator, journal mode, and migration API before moving or replacing files.
