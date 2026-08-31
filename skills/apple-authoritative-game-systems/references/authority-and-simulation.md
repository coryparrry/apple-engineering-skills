# Authority and Simulation

Read for domain ownership, replay, settlement, or generative behavior.

## Authority map

For every valuable fact record its sole writer, client projection, transaction boundary, and audit evidence. Typical mappings:

| Fact | Authority | Client behavior |
| --- | --- | --- |
| Currency/inventory | Server ledger/aggregate | Render versioned projection |
| Timer completion | Server clock | Display an estimate |
| Purchase entitlement | Server after verified evidence | Show pending until receipt |
| Narrative wording | Presentation provider | Cite accepted facts |

A prediction or cache is never authority.

## Replay envelope

Identify each run by starting snapshot, ruleset/content versions, logical time, ordered accepted commands, named random-stream state, and stored external decisions. Canonicalize ordering. Avoid ambient randomness, wall-clock timing, locale-sensitive parsing, binary floating-point money, hash-map iteration, and task-completion order.

Persist output hashes and invariant results. Replay must not call external providers.

## Staged settlement

1. Freeze an input snapshot.
2. Compute retryable partitions into staged results.
3. Validate conservation, uniqueness, totals, and references.
4. Publish one new snapshot only after all mandatory stages pass.

Failure leaves the prior snapshot published and the work resumable. Clients never see mixed epochs.

## Generative boundary

Separate narration, natural-language interpretation, and NPC strategy proposal. Each returns a finite typed candidate that deterministic code validates against current state. Store accepted NPC intentions before applying them and provide a deterministic fallback for timeout, refusal, malformed output, or model changes.

Never ask a model for final prices, rewards, probabilities, balances, ownership, settlement results, or random seeds. Generated text cannot be the only explanation of an outcome.
