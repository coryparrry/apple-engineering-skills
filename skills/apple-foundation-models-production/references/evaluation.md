# Evaluation and Release Evidence

Use this workflow for a new generative feature, a meaningful prompt/schema change, a model-provider change, or release qualification.

## Version the behavior

Assign an application-owned version to the combined behavior of:

- instructions and prompt template;
- schema and guides;
- preprocessing and context selection;
- tool definitions and their result format;
- validators and fallback policy;
- selected model/provider and generation options.

Include that version in privacy-safe telemetry and evaluation reports. Do not assume an operating-system update leaves model behavior unchanged.

## Build a representative fixture set

Start with real task shapes, then sanitize them so fixtures contain no private user data. Cover:

- ordinary inputs across supported languages and locales;
- empty, minimal, long, malformed, and duplicate data;
- contradictory and stale evidence;
- prompt injection or instructions embedded in untrusted source text;
- sensitive inputs likely to exercise guardrails;
- unsupported device, language, capability, and attachment states;
- cancellation before dispatch, during generation, and before publication;
- tool timeout, duplicate tool calls, denied permission, and invalid tool arguments;
- invalid citation identifiers and claims unsupported by supplied evidence.

Keep a small release-gating set fast enough to run for every prompt change and a larger exploratory set for periodic review.

## Measure in the right order

1. **Deterministic contract checks:** schema validation, source-ID membership, forbidden actions, length bounds, privacy redaction, fallback and cancellation behavior.
2. **Ground-truth comparisons:** task-specific known answers where a verified answer exists.
3. **Semantic measurements:** appropriate for meaning-preserving summaries and rewrites, with thresholds calibrated to the task.
4. **Model-based judgment:** tone or nuanced quality only after comparing judge decisions with human review.
5. **Human review:** high-impact, ambiguous, safety-sensitive, and novel failure cases.

Do not use exact string matching as the primary quality test for probabilistic prose. Do use exact checks for identifiers, permissions, output structure, forbidden content, and other deterministic invariants.

## Record useful evidence

For each evaluation run, capture:

- behavior/prompt version and source revision;
- device family, OS, SDK, locale, and model/provider when available;
- fixture-set revision and sanitization status;
- pass/fail counts per quality criterion;
- latency distribution, cancellation, fallback, and framework error categories;
- validator rejections and citation failures;
- human-reviewed examples of each material failure mode;
- the release decision and named unresolved risks.

Avoid storing raw production prompts or transcripts. Evaluation evidence should be reproducible without user data.

## Evaluate runtime behavior

Build success is not model evidence. Exercise the feature on eligible hardware when validating availability, latency, memory pressure, guardrails, tool calls, image understanding, and actual output quality.

Use Instruments and Apple's Foundation Models performance tooling when response time or token/context behavior matters. Compare cold and warmed requests separately. Test foreground and background behavior separately, especially when streaming.

## Handle regressions

When a prompt change improves one criterion and harms another:

- retain the prior run for comparison;
- identify the smallest instruction, schema, context, or validator change responsible;
- add the observed failure shape to the fixtures;
- prefer deterministic preprocessing or validation over more prompt prose;
- roll back if the release gate cannot justify the tradeoff.

Do not keep stacking emphatic instructions onto an unstable prompt. Split the task, reduce context, narrow the schema, or reconsider model fit.

## Review cadence

Review this skill and its source set when any of the following occurs:

- a new major Apple SDK or Foundation Models API wave;
- a deployment-target change;
- a material model behavior change observed after an OS update;
- a new provider, capability, guardrail mode, attachment type, or tool-calling mode;
- a production privacy, safety, latency, or grounding incident.

Update `last-reviewed` only after checking the workflow and invariants. Update `apple-docs-reviewed` only after reviewing the current Apple documentation through Xcode DocumentationSearch.
