# Ownership and Transitions

Read this when choosing the primary lifecycle or diagnosing duplicate, leaked, or vanishing UI resources.

## Ownership Graph

For every window, panel, menu, status item, monitor, observer, timer, and task, record its creator, strong owner, delegate/target/callback, state source, actor, start condition, and idempotent stop/release condition.

- **SwiftUI primary:** scenes own their windows and commands; `NSApplicationDelegateAdaptor` handles delegate-only integration.
- **AppKit primary:** a lifecycle coordinator retains AppKit controllers and hosts SwiftUI content.
- **Mixed:** divide ownership by stable surface identity, not by whichever framework last touched it.

Delegate callbacks should become explicit coordinator inputs rather than hold feature, persistence, or long-running work.

## Transition Table

For each launch, status-item action, reopen, activation/deactivation, close, hide/unhide, and quit event, record preconditions, state change, AppKit effects, and cleanup. Important distinctions include:

- policy versus active state;
- visible versus hidden/minimized/occluded;
- key versus main window;
- close versus order-out versus release;
- last-window close versus explicit quit;
- background-ready versus terminating.

Make repeated or reordered callbacks idempotent. Retain window controllers for surfaces that survive creation; do not use `NSApplication.shared.windows` as the owner or primary registry. A released surface must leave no active task, timer, observer, monitor, or callback targeting it.

## Runtime Evidence

Verify repeated show/reopen creates one logical window; headless launch does not activate unexpectedly; explicit action focuses the intended surface; panels dismiss and deactivate correctly; last-window close follows product policy; menus stay current without blocking; repeated start/stop removes monitors once; termination cancels owned work; and SwiftUI state changes do not recreate AppKit shells. Use pure transition tests plus focused runtime/UI tests for activation, focus, menus, panels, and Spaces behavior.
