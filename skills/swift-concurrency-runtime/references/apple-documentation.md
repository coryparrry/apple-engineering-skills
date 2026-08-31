# Apple documentation review

Last reviewed with Xcode DocumentationSearch: **2026-08-30**.

Scope: Swift actor isolation and `Sendable`, cooperative task cancellation, task-group cancellation and drain behavior, cancellation handlers, and `AsyncStream` buffering and termination. These links are review anchors, not copied documentation. Re-run Xcode DocumentationSearch when the toolchain, deployment SDK, Swift language mode, strict-concurrency level, default actor isolation, Approachable Concurrency or upcoming-feature state, or behavior under review has changed.

Fresh queries used for this review:

- `Strict Concurrency Checking Default Actor Isolation Approachable Concurrency Task cancellation cooperative uncooperative task group waits children shutdown`
- `Xcode build settings Strict Concurrency Checking SWIFT_STRICT_CONCURRENCY Default Actor Isolation SWIFT_DEFAULT_ACTOR_ISOLATION Approachable Concurrency upcoming features Swift 6`

## Consulted documentation

- `/documentation/Swift/AdoptingSwift6`
- `/documentation/Swift/AdoptingSwift6#Upgrade-a-project-to-Swift-6`
- `/documentation/Swift/concurrency#Actors`
- `/documentation/Swift/Sendable`
- `/documentation/Swift/Task#Task-Cancellation`
- `/documentation/Swift/Task#Canceling-Tasks`
- `/documentation/Swift/TaskGroup#Structured-Concurrency`
- `/documentation/Swift/ThrowingTaskGroup#Cancellation-behavior`
- `/documentation/Swift/ThrowingTaskGroup/cancelAll()`
- `/documentation/Swift/withTaskCancellationHandler(operation:onCancel:)#Execution-order-and-semantics`
- `/documentation/Swift/withTaskCancellationHandler(operation:onCancel:)#Cancellation-handlers-and-locks`
- `/documentation/Swift/AsyncStream/Continuation/BufferingPolicy#Buffering-Policies`
- `/documentation/Swift/AsyncStream/Continuation#Handling-Termination`
- `/documentation/Swift/AsyncStream/init(_:bufferingPolicy:_:)`
- `/documentation/Xcode/build-settings-reference#Strict-Concurrency-Checking`
- `/documentation/Xcode/build-settings-reference#Default-Actor-Isolation`
- `/documentation/Xcode/build-settings-reference#Approachable-Concurrency`
- `/documentation/Xcode/build-settings-reference#Dynamic-Actor-Isolation`
- `/documentation/PackageDescription/SwiftSetting#Configuring-Swift-Settings`
- `/documentation/PackageDescription/SwiftSetting/defaultIsolation(_:_:)`

The Xcode index exposes actor and `Sendable` API contracts but does not provide a single complete actor-reentrancy design article. The skill's reentrancy guidance therefore stays at the stable language-model invariant: actor-isolated code may suspend at `await`, so state must be revalidated when an invariant spans suspension.
