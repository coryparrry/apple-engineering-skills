# Contracts and Integrity

Read for command APIs, identity, App Attest, networking, or offline reconciliation. For StoreKit value followed by spending, also read [purchase-and-spend.md](purchase-and-spend.md).

## Command contract

A mutation carries a stable command ID, type, expected revision, contract version, typed payload, and separately encoded integrity evidence. Return a stable status, authoritative revision/result reference, and correlation ID.

Canonicalize command semantics before hashing. Persist command ID, actor, semantic hash, status, result, and failure class. Exclude replaceable transport evidence such as a fresh App Attest challenge/assertion from the semantic hash, but cryptographically bind that evidence to the hash.

After a timeout, query by command ID. Same ID/hash returns the stored result; same ID with changed semantics is rejected. Prefer additive contract evolution and test every supported deployed client version.

## Game Center identity

Game Center initialization enables its services; it is not the game's session protocol.

1. Initialize the local player and respect account restrictions.
2. Request identity-verification signature items.
3. Send signature, salt, timestamp, public-key URL, and expected player identity over TLS.
4. Validate signature and freshness server-side using Apple's current procedure.
5. Map the verified scoped identity to an opaque internal player ID and mint a short-lived game session.

Treat account change as identity change. Never authorize with alias/display name or use it as a primary key.

## App Attest

- Gate on runtime support and current platform documentation.
- Use a unique server challenge for attestation and each protected assertion.
- Bind assertion data to command semantics and authenticated actor.
- Verify certificate chain, app/environment identity, challenge, and key association server-side. Serialize assertions per key and atomically compare-and-set a strictly increasing stored counter; concurrent reconnects must not admit replay or create false regression handling.
- Keep development/production keys separate; permit legitimate per-device keys while preventing silent cross-account reuse.
- Define separate policy for unsupported service, outage/throttling, key loss, invalid evidence, and replay/counter regression.

Attest sparingly; assert on sensitive commands. Never prefetch reusable challenges or make client-side validation authoritative.

## Offline/background

Cache read projections with snapshot/age. Queue only immutable typed intent with its command ID—never a client-computed outcome. Competitive or expiring actions may require connectivity. On reconnect, query receipts before submission; require reconfirmation for stale meaning.

Persist queues before attempting delivery. Assume background work can be delayed, canceled, force-quit, or never run. Background `URLSession`/tasks may transport work but never prove exactly-once application. The server continues authoritative time; foreground reconciliation repairs the view.

## Anti-cheat order

First enforce server authority/invariants, then idempotency/revisions/transactions, then identity and App Attest evidence, then rate/anomaly controls and audit/recovery. Client obfuscation or client-computed state hashes are not primary defenses.
