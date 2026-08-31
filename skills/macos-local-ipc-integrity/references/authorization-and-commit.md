# Authorization and Commit Integrity

Read this before adding a mutating method, opaque-resource resolver, delegated capability, idempotency record, or audit trail.

## Map Trust

For each method, record the peer principal, allowed method/resource scope, opaque-ID resolution and disclosure policy, time-varying authorization/revision/lease, single commit owner, and durable replay record.

Filesystem permissions, sandboxing, signing, parent-child relationships, and peer credentials are defense layers—not substitutes for authority-owned method authorization.

## Opaque Resources and Revalidation

Use authority-issued identifiers that reveal neither paths nor storage layout. Resolve them after authorization; avoid distinguishing missing from forbidden unless allowed.

Never accept a caller path and exercise broader service permissions on it. Represent supported file access with an authority-owned handle, bookmark, grant, or record resolved under the intended identity.

Preparation may load snapshots, ask the user, or call services, but must not hold the authoritative transaction open. After the last suspension, revalidate principal, capability, resource identity, revision/digest, grant/policy, and operation identity. Failure performs no write.

## Durable Operation Record

When restart-safe replay is required, atomically commit the mutation with:

- principal scope, operation ID/kind, and canonical digest version;
- committed revision or result reference and final outcome/sequence;
- bounded material needed to reproduce the response.

Specify canonicalization. Either hash exact immutable submitted bytes by contract or deterministically canonicalize typed fields; arbitrary JSON byte encodings are not a semantic identity.

If they cannot share a transaction, identify the partial-commit window and close it with an outbox, journal, reconciliation, or unique constraint. Claim idempotent application, not exactly-once execution.

Only the authority may issue definitive `committed`, `duplicate`, or non-commit evidence. Keep `rejected`, `accepted`, `conflicted`, `failed`, and `unknown` distinct.

## Privacy-Safe Audit

Record only principal/method categories, redacted correlation, authorization/precondition result, revision, outcome, and stable error category. Exclude payloads, tokens, environments, paths, user-bearing addresses, and parse fragments; bound retention.
