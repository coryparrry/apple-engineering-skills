# Test Strategy

Read before completing an authoritative mutation, identity/integrity flow, or entitlement grant.

## Simulation and transactions

- Replay fixtures in isolated stores with different insertion/concurrency schedules while preserving the same canonical accepted-command order; compare canonical hashes.
- Exercise numeric boundaries, rounding, conservation, uniqueness, locks, isolation, outbox, migrations, and crash recovery against the production transaction engine.
- Inject model timeout/refusal/malformed output; deterministic fallback preserves progression.
- Prove same command ID/payload mutates once and returns one result; changed payload conflicts.
- Race scarce resources, kill after commit/before response, fail outbox delivery, forge device time, and submit stale revisions.

Use a real database for database guarantees. Property tests complement concrete scenarios; tautological mocks prove nothing.

## Apple integrations

**Game Center:** unauthenticated/authenticated/restricted/account-changed callbacks; valid, invalid, expired, and replayed server identity material; internal identity binding and session rotation.

**App Attest:** unsupported/outage; development/production separation; attestation/assertion/key loss; used or mismatched challenge; evidence bound to another actor/payload; repeated/regressed counter; cross-account key; rollout/recovery policy. Do not weaken validation for fixtures.

**StoreKit:** verified/unverified, duplicated/delayed/reordered transactions; product/environment/signed-account mismatch; refund, revocation, expiration, and restore where applicable to the product type; notification ordering; crash between grant and finish; idempotent entitlement. Use StoreKit testing plus sandbox/device proof where mocks are insufficient.

## Offline and lifecycle

- Terminate before upload and after upload/before response; relaunch and reconcile by command ID.
- Return after the authoritative revision changes.
- Expire/cancel background work without losing queued intent.
- Treat pushes as invalidations followed by projection fetch, not state mutations.
- Change device clock/time zone without advancing authority.

## Contracts and release evidence

Generate/validate both ends from one schema in CI and exercise every supported released contract. Test canonical hashes across implementations and forward-compatible unknown values where intended.

Retain exact client/server revisions, contract and environment versions, Apple-documentation review date, replay/invariant results, device/OS coverage, and recovery policy. A happy-path purchase or command is insufficient.
