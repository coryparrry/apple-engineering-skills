# Diagnosis and test matrix

## Evidence ladder

1. **Bind the run:** executable, build, toolchain, Swift language mode, strict-concurrency level, default actor isolation, Approachable Concurrency, upcoming/experimental feature flags, OS, device, and feature configuration.
2. **State one observable failure:** use a transition or timing claim.
3. **Trace one lifecycle:** identity, owner, admission, suspension, cancellation, commit/discard, and terminal observation.
4. **Force the interleaving:** inject gates, clocks, or controllable dependencies instead of sleeps.
5. **Change one contract rule:** avoid broad isolation rewrites before proving the failure.
6. **Repeat:** compare event order and resource counts, not only pass/fail.

## Classify the failure

| Symptom | First question |
|---|---|
| Stale value overwrites current state | Was identity revalidated after `await`? |
| Timeout never returns | Does the losing child cooperate, and must a group scope drain it? |
| Producer continues after view/service ends | Who owns upstream cancellation, and does stream termination reach it? |
| CPU or request storm | Is admission bounded, and are triggers coalesced? |
| Missing final event | Was the stream finished before the consumer exited? |
| Duplicate callback/result | Is continuation or terminal publication exactly once? |
| UI freeze despite async code | Is synchronous work executing on the main actor before suspension? |
| Clean Thread Sanitizer run but wrong state | Is this a logical reentrancy race rather than a memory data race? |

## Deterministic test controls

Use test-controlled clocks, dependencies suspended at named phases, cancellation/admission probes, upstream registrations recording cancellation/release, and an actor recording ordered events.

Assert the required effect, not merely `isCancelled`: capacity released, upstream stopped, stale result ignored, stream ended, or shutdown completed.

## Minimum adversarial scenarios

Cover cancellation before start, during a dependency, and before commit; actor changes at suspension; cooperative and supervised deadline losers; rapid replacement; capacity saturation; stream overflow and early consumer exit; shutdown across queued/running/publishing work; an uncooperative task that outlives the shutdown budget without touching released state; and error/cancellation without double completion.
