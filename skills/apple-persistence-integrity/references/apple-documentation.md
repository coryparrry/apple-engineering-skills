# Apple Documentation Index

Reviewed with Xcode MCP `DocumentationSearch` on **2026-08-30**.

Fresh query: `ModelContext transaction autosave rollback pending changes PersistentIdentifier isTemporary coherent SQLite WAL store copy NSPersistentStoreCoordinator`.

Scope: SwiftData container/context ownership, isolation, transactions, batching, migration, and custom-store capabilities. These are the returned documentation URIs consulted for this skill. Search again when the SDK or deployment target differs.

- Containers and contexts: [`ModelContainer`](https://developer.apple.com/documentation/SwiftData/ModelContainer), [`ModelContext`](https://developer.apple.com/documentation/SwiftData/ModelContext), [save/transaction/rollback](https://developer.apple.com/documentation/SwiftData/ModelContext#Persisting-unsaved-changes), and [`ModelConfiguration`](https://developer.apple.com/documentation/SwiftData/ModelConfiguration).
- Isolation: [`ModelActor()`](https://developer.apple.com/documentation/SwiftData/ModelActor()), [model executors](https://developer.apple.com/documentation/SwiftData/ConcurrencySupport#Model-executors), and [`DefaultSerialModelExecutor`](https://developer.apple.com/documentation/SwiftData/DefaultSerialModelExecutor).
- Commit boundaries: [`transaction(block:)`](https://developer.apple.com/documentation/SwiftData/ModelContext/transaction(block:)), [`autosaveEnabled`](https://developer.apple.com/documentation/SwiftData/ModelContext/autosaveEnabled), and [`rollback()`](https://developer.apple.com/documentation/SwiftData/ModelContext/rollback()).
- Identity: [`PersistentIdentifier.isTemporary`](https://developer.apple.com/documentation/SwiftData/PersistentIdentifier/isTemporary).
- Migration: [`SchemaMigrationPlan`](https://developer.apple.com/documentation/SwiftData/SchemaMigrationPlan), [`VersionedSchema`](https://developer.apple.com/documentation/SwiftData/VersionedSchema), [`MigrationStage`](https://developer.apple.com/documentation/SwiftData/MigrationStage), and [migration errors](https://developer.apple.com/documentation/SwiftData/SwiftDataError#Migration-errors).
- Custom stores: [`DataStore`](https://developer.apple.com/documentation/SwiftData/DataStore), [`DataStoreBatching`](https://developer.apple.com/documentation/SwiftData/DataStoreBatching), and [`HistoryProviding`](https://developer.apple.com/documentation/SwiftData/HistoryProviding).
- Bounded reads: [`fetch(_:batchSize:)`](https://developer.apple.com/documentation/SwiftData/ModelContext/fetch(_:batchSize:)), [`fetchIdentifiers(_:batchSize:)`](https://developer.apple.com/documentation/SwiftData/ModelContext/fetchIdentifiers(_:batchSize:)), and [`fetchCount(_:)`](https://developer.apple.com/documentation/SwiftData/ModelContext/fetchCount(_:)).
- Fetch errors: [`SwiftDataError`](https://developer.apple.com/documentation/SwiftData/SwiftDataError#Fetch-errors) documents pending-change/batching failures.
- Store operations: [`NSPersistentStoreCoordinator`](https://developer.apple.com/documentation/CoreData/NSPersistentStoreCoordinator#Modifying-a-store), [accessing data when a store changes](https://developer.apple.com/documentation/CoreData/accessing-data-when-the-store-changes), and [`NSFileCoordinator`](https://developer.apple.com/documentation/Foundation/NSFileCoordinator).
