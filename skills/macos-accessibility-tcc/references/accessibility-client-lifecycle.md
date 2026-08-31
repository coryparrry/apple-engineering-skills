# Accessibility client lifecycle and runtime evidence

Read this for `AXObserver`, callback context, target relaunch, teardown, or trust diagnosis. It is for clients of other processes, not an app's own accessibility implementation.

## Session identity and setup

A session owns client generation, target bundle/PID, application element, observer, run loop/mode, successful registrations, callback context, and in-flight work.

`AXIsProcessTrustedWithOptions` checks the caller. The prompt option may inform the user asynchronously, but the call returns current trust. Explain the feature, prompt once from user action, and remain untrusted until a later check succeeds. Development, runner, helper, and installed identities require separate proof when they make AX calls.

Setup transaction:

1. Check trust without prompting; resolve the target's current PID.
2. Create the application element and observer for that PID.
3. Create callback context owned for the observer lifetime.
4. Add the observer source to a known live run loop/mode.
5. Register required notifications, recording successful pairs.
6. Publish active only after required registration succeeds.

Rollback on failure. Relaunch means a new PID, generation, elements, and observer.

## Callback ownership

A common safe shape strongly owns Swift context in the session and passes an unretained opaque `refcon`; the callback calls `takeUnretainedValue()` only while that lifetime is guaranteed. If using `passRetained`, release once after registrations and callbacks quiesce—never `takeRetainedValue()` per notification.

Callbacks validate PID/generation/terminal state, copy minimal identity, account for in-flight asynchronous work, use bounded processing, and finish accounting reliably. Avoid blocking the AX run-loop thread on work that calls back into it.

## Error and sensitive-input policy

Check `AXError`, then validate the Core Foundation type. Treat no-value/unsupported as capability outcomes; `cannotComplete` as a messaging/health failure; invalid element as re-resolution; API disabled as a trust re-check; illegal argument as caller code to fix. Retry `cannotComplete` only for explicitly idempotent reads or registrations, with a small budget while the same PID is alive. Never replay an action merely because its result was `cannotComplete`: the target may have performed the action before the reply failed. Do not retain a full AX tree.

Before any value-like read:

1. Read role and subrole only.
2. Treat `kAXSecureTextFieldSubrole` as sensitive.
3. Treat editable/focused elements with failed classification as sensitive.
4. Never request value, selected text, ranges, text markers, or descendant text for sensitive elements.
5. Emit only a content-free suppression event.

Redaction after reading is too late.

## Idempotent teardown and recovery

Keep callback context alive while stopping. On the observer's recorded run loop/mode, mark the session terminal, remove all successful notification pairs, and remove the source. Callback entry and exit must participate in a synchronized in-flight lease. Release the context, observer, and elements only after the run-loop removal operation has completed and every callback lease plus accepted asynchronous callback task has quiesced. Do not block the callback thread while waiting for itself. If the owner cannot establish that barrier, retain the context rather than risking a stale `refcon` dereference. Continue after invalid-element or not-registered cleanup errors and record the mismatch.

Re-resolve invalid elements and reconstruct after PID change. Never poll trust indefinitely or reset consent without authorization.

## Evidence

Record client path/bundle/signature/PID, target bundle/PID, generation, registration/removal and callback counts, categorized errors, and sensitive-suppression counts. Never record titles, documents, labels, descriptions, values, selected text, or tree dumps.

Validate untrusted/trusted/revoked behavior on the exact client, balanced observer cycles, teardown during callback load, target relaunch, unsupported attributes, bounded unresponsive-target recovery, and value-call suppression for secure and ambiguous inputs.
