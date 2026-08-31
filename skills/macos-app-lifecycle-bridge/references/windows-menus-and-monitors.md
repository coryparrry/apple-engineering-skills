# Windows, Menus, Panels, and Monitors

Read this when implementing a concrete AppKit resource.

## Windows and Panels

- Decide whether each identity is singleton, keyed, or disposable.
- Retain its `NSWindowController`/coordinator and hosting controller.
- Inject stable feature state; do not recreate the AppKit shell for SwiftUI updates.
- Choose one sizing authority and test restoration after a normal quit/relaunch.
- Specify panel activation, key/main eligibility, level, hide-on-deactivate, outside-click dismissal, release policy, and Spaces/full-screen behavior independently.

## Menus and Status Items

- Retain the status item and its target for their full usable lifetime.
- Update structure in `menuNeedsUpdate`; use validation for enabled state.
- Keep menu tracking free of I/O and expensive model work.
- Remove the status item through `NSStatusBar.removeStatusItem` during shutdown.

## Monitor Ownership

An owner needs idempotent `start()` and `stop()`: install only when no token exists; capture the owner weakly; on stop, take and clear the token, then call `NSEvent.removeMonitor` once.

Local monitors observe this app before dispatch and may replace or suppress events. Global monitors observe other apps asynchronously, cannot alter delivery, and global key monitoring may require Accessibility trust. If a panel uses a local/global pair for outside-click dismissal, own and stop both together.

Do not treat a local monitor as proof that every event inside the app is observable. Menus, controls, window dragging, and other components can run tracking loops with their own event retrieval and run-loop modes. When correctness depends on behavior during tracking, use that component's lifecycle/delegate hooks or an explicitly designed tracking-mode mechanism, then test the exact interaction. Accessibility trust is specifically relevant to global key monitoring; do not turn it into a blanket prerequisite for global mouse monitoring.

Call explicit teardown when the feature stops. Treat `deinit` only as a backstop; avoid using it to sidestep main-actor cleanup.
