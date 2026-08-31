# Production Contracts

Read the sections relevant to the feature being implemented or reviewed. Keep the application's contract stricter when its domain requires it.

## Availability and capability boundary

`SystemLanguageModel.availability` answers whether the system model can accept requests now. Treat each unavailable reason as a product state rather than an exception to obscure. A feature should remain usable through a deterministic fallback when the device is ineligible, Apple Intelligence is disabled, or model assets are not ready.

Admission is provider-specific. `PrivateCloudComputeLanguageModel` itself requires the current SDK/platform availability gate: the reviewed SDK introduces it on iOS, macOS, visionOS, and watchOS 27 and marks it unavailable on tvOS. Below that floor, use an available system-model path or a deterministic non-model fallback. Where PCC can be referenced, check its runtime availability and required managed entitlement/eligibility, inspect quota separately, and handle request-time network, service-unavailable, and quota errors. An available provider is not proof that quota or the next network request will succeed.

When code supports more than one `LanguageModel`, apply any provider-specific admission or availability check that provider exposes, then inspect `capabilities` before using guided generation, tool calling, reasoning, or image input. `availability` is not a requirement of the `LanguageModel` protocol, and capability support does not prove provider admission.

Do not copy an availability switch from documentation without checking exhaustiveness against the project's SDK. Preserve an unknown/default path when writing source intended to span SDK versions.

## Session admission and lifetime

A `LanguageModelSession` contains transcript state and permits only one response operation at a time. Choose one policy explicitly:

- **Queue:** serialize requests whose ordering matters.
- **Latest wins:** cancel and discard older work for interactive previews or rapidly changing selections.
- **Reject while busy:** appropriate for an explicit action whose UI already shows progress.
- **Independent sessions:** use only when requests do not share a transcript and separate model work is acceptable.

An actor is a suitable ownership boundary for session state, request identity, and cancellation. Still treat cancellation as cooperative: compare a captured request identifier immediately before publishing the result.

Prewarm only when a near-term request is likely and the latency benefit is worth the resource cost. Never make prewarming a hidden requirement for correctness.

## Error and fallback taxonomy

Map framework errors by meaning, not by a single generic catch:

| Category | Product treatment |
| --- | --- |
| Cancellation or superseded request | End quietly; never publish stale partial output |
| Model unavailable or assets unavailable | Show the appropriate capability state and use fallback |
| Guardrail violation or refusal | Respect the boundary; offer safe wording or a non-model path |
| Unsupported language, locale, capability, or guide | Disable that route or select a supported configuration |
| Context limit | Reduce application-owned context deterministically; do not blindly retry |
| Rate or capacity limit | Bound retries and preserve a useful fallback |
| Concurrent session request or transcript mutation | Fix the admission bug rather than retrying |
| Tool failure | Preserve tool-specific semantics; do not let the model mask authorization or integrity failures |
| Output validation failure | Reject the output and use the declared recovery path |

Inspect the exact error types in the current SDK. Error cases have evolved across Foundation Models releases.

## Guided generation contract

Use guided generation for shape and constrained choices, not factual correctness.

- Design the smallest type that represents what the caller needs.
- Use descriptive property names and short descriptions.
- Constrain ranges, counts, patterns, and closed choices when they are actual domain rules.
- Put context-setting properties before dependent properties only when evaluation shows that order improves this task; preserve the schema's required structural order.
- Avoid free-form strings for identifiers, actions, or permissions when a closed type is possible.
- Validate cross-field relationships, evidence membership, domain rules, and current state after decoding.

For a dynamic schema, validate references and dependencies when constructing the schema and keep a deterministic decoder from `GeneratedContent` into an application-owned type.

## Evidence and citation contract

Grounding requires more than putting source text in a prompt.

1. The application selects authoritative source records.
2. It assigns opaque stable identifiers such as `source-0007`.
3. The prompt includes only the minimum evidence needed for the task.
4. Generated output refers to identifiers, not self-invented URLs or quotations.
5. Application code rejects unknown, duplicated, or out-of-scope identifiers.
6. The UI reconstructs source labels, excerpts, timestamps, and links from authoritative records.
7. Claims without valid supporting identifiers are removed, marked uncertain, or cause fallback according to the product contract.

Do not treat a cited source as proof that a claim follows from it. For high-risk claims, add deterministic extraction, human review, or a domain-specific verifier.

## Multimodal contract

Use `Attachment` for supported image inputs. Prefer the source representation the application already owns; Apple documents that the framework performs necessary scaling and color conversion. Supply orientation when the source pixels do not already encode the intended display transform. Label attachments when a response or tool must distinguish them.

Before attaching an image:

- verify its type, source, orientation, and lifecycle;
- crop or redact regions the feature does not need;
- remove unrelated metadata when the file may leave the process through a tool;
- define how an empty, corrupt, protected, or unsupported image falls back;
- ensure generated descriptions are labeled as interpretations rather than ground truth.

Use dedicated structured Vision OCR or barcode tools when extracted data matters. Treat their observations as evidence that can vary by framework/OS revision, validate the result for the domain, and let a language model explain only accepted extraction.

## Tool-calling contract

Every `Tool` is an application API exposed to probabilistic routing. Keep tools few, names unambiguous, arguments constrained, and results compact.

Tools must enforce:

- authentication and authorization independent of the model;
- argument validation and safe resource limits;
- privacy boundaries for remote I/O;
- idempotency or duplicate-call handling;
- cancellation and timeouts;
- user confirmation immediately before consequential side effects;
- concurrency safety when tool instances contain mutable state.

Prefer read-only tools. Separate lookup from mutation so a model can gather context without gaining write authority.

If using a mode that requires tool calls, define an explicit exit condition. Apple's current documentation warns that repeatedly requiring a tool call can form an infinite loop. Use a bounded state machine, maximum calls, or a profile transition that disallows further tools after sufficient data is collected. Do not use a thrown error as normal control flow unless transcript preservation and recovery behavior are deliberately tested against the selected SDK.

Tool output joins model context. Return only what the next generation step needs, and never include secrets merely because the tool can access them.

## Privacy contract

On-device inference reduces transport exposure; it does not make every surrounding data path private.

Review separately:

- prompt construction and temporary files;
- retained session transcripts;
- image attachments and their metadata;
- tools that read network, database, file, calendar, mail, health, or account data;
- analytics, crash reports, logs, feedback attachments, and evaluation fixtures;
- optional alternate providers, including Private Cloud Compute or third-party services.

Prefer derived counters and categorical telemetry. If debug capture of content is genuinely required, make it explicit, time-bounded, access-controlled, and removable.
