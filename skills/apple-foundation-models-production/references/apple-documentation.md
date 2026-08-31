# Apple Documentation Evidence

## Scope and freshness

Reviewed through Xcode MCP `DocumentationSearch` on 2026-08-30 with the `FoundationModels` framework filter. The results reflect the Apple documentation indexed by the installed Xcode toolchain on that date. They are evidence for this skill's workflow, not a substitute for checking the deployment target and current SDK.

Fresh query: `PrivateCloudComputeLanguageModel availability quota entitlement network errors LanguageModelError unsupported capability rate limited OCRTool barcode deterministic`.

Re-run DocumentationSearch before using an API not represented below, after an Xcode/SDK update, or when `apple-docs-reviewed` no longer matches the skill's current documentation review.

## Sources consulted

- `doc://com.apple.documentation/documentation/FoundationModels`
  - Framework scope, on-device and alternate model roles, guided generation, tools, device eligibility, and current capability model.
- `doc://com.apple.documentation/documentation/FoundationModels/generating-content-and-performing-tasks-with-foundation-models`
  - Model-fit boundaries, availability-first workflow, and single-turn versus multi-turn session lifetime.
- `doc://com.apple.documentation/documentation/FoundationModels/SystemLanguageModel/Availability-swift.enum`
  - Available and unavailable states and unavailable reasons.
- `doc://com.apple.documentation/documentation/FoundationModels/LanguageModelCapabilities`
  - Capability inspection for guided generation, reasoning, tool calling, and vision.
- `doc://com.apple.documentation/documentation/FoundationModels/LanguageModelSession`
  - Session creation, response generation, streaming, prewarming, transcript state, and error surface.
- `doc://com.apple.documentation/documentation/FoundationModels/LanguageModelSession/Error`
  - Concurrent-request and transcript-mutation misuse errors.
- `/documentation/FoundationModels/LanguageModelError`
  - Provider-neutral generation errors including capability, guide, locale, guardrail, refusal, context, and rate-limit failures.
- `/documentation/FoundationModels/PrivateCloudComputeLanguageModel/Availability-swift.enum`
  - Provider-specific runtime availability and unavailable reasons after compile-time/platform gating.
- `/documentation/FoundationModels/PrivateCloudComputeLanguageModel`
  - Platform availability for the provider type; the reviewed SDK introduces it on iOS, macOS, visionOS, and watchOS 27 and marks it unavailable on tvOS.
- `/documentation/BundleResources/Entitlements/com.apple.developer.private-cloud-compute`
  - Managed entitlement and signing eligibility are setup/admission evidence, not a request-time PCC error case.
- `/documentation/FoundationModels/PrivateCloudComputeLanguageModel/QuotaUsage-swift.struct`
  - Quota is an admission dimension separate from availability.
- `/documentation/FoundationModels/PrivateCloudComputeLanguageModel/Error`
  - Request-time network, service-unavailable, and quota-limit failures.
- `doc://com.apple.documentation/documentation/FoundationModels/GenerationSchema`
  - Deterministically constrained output format.
- `doc://com.apple.documentation/documentation/FoundationModels/GenerationGuide`
  - Value-level generation constraints.
- `doc://com.apple.documentation/documentation/FoundationModels/analyzing-images-with-multimodal-prompting`
  - `Attachment`, supported image representations, orientation, labels, and dedicated structured Vision tools for OCR/barcodes; observations remain revision-sensitive and require application validation.
- `/documentation/Vision/OCRTool`
- `/documentation/Vision/BarcodeReaderTool`
- `doc://com.apple.documentation/documentation/FoundationModels/Attachment`
  - Media attachments in prompts and attachment labels.
- `doc://com.apple.documentation/documentation/FoundationModels/improving-the-safety-of-generative-model-output`
  - Default guardrails, guardrail errors, refusals, and the limits of permissive content transformations.
- `doc://com.apple.documentation/documentation/FoundationModels/expanding-generation-with-tool-calling`
  - Tool definitions and model-directed tool invocation.
- `doc://com.apple.documentation/documentation/FoundationModels/FoundationModels_Extended_API_Documentation`
  - Tool-calling modes, required-mode loop risk, dynamic profiles, and transcript error-handling policies in the current indexed SDK.
- `doc://com.apple.documentation/documentation/FoundationModels/prompting-an-on-device-foundation-model`
  - Small-model prompt design, task decomposition, iteration, and feedback attachments.
- `doc://com.apple.documentation/documentation/FoundationModels/evaluating-prompts-to-measure-performance-and-improve-model-responses`
  - Versioned, structured prompt evaluation and measurement approaches.
- `doc://com.apple.documentation/documentation/FoundationModels/analyzing-the-runtime-performance-of-your-foundation-models-app`
  - Instruments-based latency and token/context analysis.
- `doc://com.apple.documentation/documentation/FoundationModels/managing-the-context-window`
  - Context-budget management.
- `doc://com.apple.documentation/documentation/FoundationModels/updating-prompts-for-new-model-versions`
  - Prompt versioning across model changes.

## Review notes

- Apple's current documentation describes `LanguageModelSession.ResponseStream` values as snapshots of partially generated content.
- Apple advises non-streaming generation for background work to reduce rate-limit risk.
- Availability and capability are distinct gates.
- Guided generation constrains representation; application validation remains necessary for semantics and authority.
- Permissive content transformations do not remove every safety boundary and are not a general bypass for guided generation.
- A required tool-calling mode needs an explicit exit condition to avoid an unbounded loop.
