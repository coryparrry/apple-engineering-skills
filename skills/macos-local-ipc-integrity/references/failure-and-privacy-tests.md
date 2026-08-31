# Failure and Privacy Tests

Read this when implementing or reviewing transport, authority, diagnostics, or recovery. Prefer deterministic fault injection and fresh-process integration over timing sleeps.

## Framing

Feed every split point, several coalesced frames, and one frame byte-by-byte. Assert identical messages and no residue.

Reject signed, overflowing, conflicting, oversized, invalid-UTF-8/JSON, unsupported, and truncated frames, including valid-then-malformed input and incomplete input near the buffer limit.

## I/O and Flow

Inject short/interrupted writes at every offset and verify frame contiguity. Exercise exit/reset, supported half-close, listener failure, startup race, cancellation, repeated close, and shutdown in flight.

Cross each slow-peer threshold; assert bounded memory, client fairness, the specified overload action, and either a delivered outcome or an explicit `unknown` result that resolves through authoritative operation lookup. Do not assert impossible lossless delivery after disconnect.

## Commit Cuts

Terminate or disconnect:

1. before and during request framing;
2. after decode, preparation, and revalidation;
3. between mutation and a separate operation record;
4. after atomic commit, during response, and before caller persistence.

Restart and query the original operation ID. Prove non-commit followed by one permitted application, or one committed result without reapplication. Never infer state from a client exception.

## Authorization

With two principals/resources, test forbidden pairs, identifier/path substitution, policy/revision changes during awaits, cross-principal replay, changed payload under one ID, and token expiry/scope reduction. Prevent unauthorized existence disclosure.

## Privacy and Evidence

Canary payloads, paths, environments, tokens, identifiers, and malformed input. Exercise all outcomes, diagnostics, telemetry, stderr, and exports; search artifacts for canaries. Assert stdout contains only protocol frames.

Unit tests prove parsers and state machines. Integration tests cross the real process boundary. Delivery-integrity tests reopen or independently query authoritative state and its operation record. Enqueue success, bytes written, mock calls, or `accepted` responses are not commit evidence.
