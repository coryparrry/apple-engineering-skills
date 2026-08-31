# Runtime design patterns

## Structured versus supervised unstructured work

Use structured concurrency when the scope owns the result and can wait for every child. Use supervised unstructured work when the lifetime is intentionally different from the initiating call.

Supervision requires a retained handle, cancellation trigger, observed completion/errors, stale-result identity, and bounded live/queued work.

Fire-and-forget requires loss, duplication, and lateness all to be harmless.

## Deadlines and first-result races

A task-group timeout still waits for children after canceling losers. An uncooperative dependency can therefore defeat the apparent deadline.

Choose based on the dependency:

- **Cooperative dependency:** take the first task-group result, cancel the rest, and drain.
- **Callback API with cancel handle:** bridge with a checked continuation and a cancellation handler; prove exactly-once resumption.
- **Uncooperative async dependency:** cancellation cannot force it to stop. When the caller must return, supervise the operation outside the structured race, reject late completion by identity, cap how many such losers may remain, and keep every resource they can access valid until their completion is observed. If that cannot be done, the dependency cannot satisfy the deadline contract.

Model the product deadline separately from cancellation cleanup.

## Actor reentrancy patterns

- **Generation:** for latest-wins work, increment before awaiting and commit only if it still matches. Do not use this when every result must commit.
- **Reserve/perform/commit:** reserve synchronously, await outside the invariant-changing phase, then commit or release an idempotent token.
- **State machine:** encode legal states and validate operation identity after suspension.

## Bounded admission policies

Select the policy from the meaning of work:

| Work meaning | Typical policy |
|---|---|
| Current snapshot refresh | Coalesce pending triggers; one active plus one dirty bit |
| Search as query changes | Cancel/replace latest; discard stale results |
| User-authored mutations | Bounded FIFO; surface rejection or retry state |
| Expensive background analysis | Fixed active limit plus bounded queue |
| Periodic polling | Skip tick while active; do not accumulate ticks |

## AsyncStream lifecycle

Define who starts/stops production, whether iterators share it, what the continuation retains, which events are replaceable, and how finish differs from cancellation or failure.

Assign `onTermination` before exposing the stream. Capture cancellation-safe state; signal actor cleanup through a supervised async path.

Inspect `yield` results when loss matters.

## Shutdown order

Stop admission; cancel owned tasks and upstream registrations; finish streams or unblock continuations; drain cooperative supervised work within the documented budget; release resources idempotently; publish one terminal state. Retain completion observation until draining ends.

Cancellation does not forcibly terminate Swift tasks. If an uncooperative task survives the shutdown budget, quarantine it behind a retained supervisor, prevent all late publication, keep its dependencies alive, and report that background cleanup remains. Do not claim a fully drained shutdown or release resources the task can still touch. If the process must exit, process termination—not task cancellation—is the only hard stop.
