# Production pipeline contracts

Use this reference when implementation work crosses image ingestion, decoding, normalization, Vision analysis, or encoding. Keep policy values product-specific; this document defines what must be bounded and proven, not universal numeric limits.

## Canonical ingress

Convert each source into the same value before decode. A useful contract records:

- immutable bytes or a bounded data provider;
- declared and detected type separately;
- source kind without retaining a sensitive filename or pasteboard value in telemetry;
- a request/session generation for stale-result rejection;
- policy limits and the selected metadata-retention mode.

Do not let an AppKit/UIKit convenience-image initializer become an alternate decoder. If a platform object is the only clipboard representation available, export it into a documented canonical representation and send that through the same validation stages. Record any unavoidable loss of original metadata or color fidelity.

## Staged decode

### 1. Bound ingress

Reject an input that exceeds the compressed-byte policy before parsing it. Resolve the effective type through ImageIO and compare it with the allowlist; do not trust only a filename extension, MIME type, pasteboard type, or caller claim.

### 2. Inspect the container

Create a `CGImageSource` without forcing full decode. Inspect source status, type, image count, and properties for the selected index. Unless animation or multi-page content is explicitly supported, require exactly one intended image or apply an explicit first-frame policy.

Read width, height, and orientation as untrusted numeric metadata. Reject zero, negative, nonnumeric, or out-of-policy values. Define a conservative policy bytes-per-pixel value from the intended or worst-case decoded format, including row alignment, then use operations that report overflow when calculating:

```text
pixelCount = width * height
estimatedRowBytes = aligned(width * policyBytesPerPixel)
estimatedDecodedBytes = estimatedRowBytes * height
```

Reject immediately if any checked conversion, multiplication, addition, or row-alignment operation reports overflow. Do not use a partial result merely because the API also returned a numeric value.

This is an application-owned admission estimate, not an ImageIO guarantee or a promise of actual decoder allocation. Include intermediate conversions, thumbnails, concurrent requests, and output buffers in the process-level memory budget. After decode, use checked `CGImage.bytesPerRow * CGImage.height` together with the actual bits-per-pixel, color, and alpha format as the decoded-buffer evidence.

### 3. Decode at the needed size

When analysis or display does not require source resolution, request a thumbnail bounded by the longest allowed dimension and enable orientation transformation only if the pipeline is choosing canonical upright pixels at this stage. Otherwise decode without transforming and retain `CGImagePropertyOrientation` for Vision.

After decode, verify `CGImage.width`, `CGImage.height`, bits/component, bits/pixel, bytes/row, alpha information, and color space against policy. Do not rely solely on pre-decode metadata.

### 4. Canonicalize once

Choose one contract:

- **Oriented evidence:** retain encoded pixel layout plus `CGImagePropertyOrientation`; call Vision with that orientation and map results through it.
- **Upright pixels:** render the orientation/mirroring into a new bitmap, make width/height match the visible result, discard or write `.up`, and call Vision with `.up`.

Document whether normalized coordinates use encoded, oriented, cropped, or rendered dimensions. Centralize coordinate conversion so overlays, stored evidence, crops, and exports cannot disagree.

## Color and alpha

Decide separately whether the pipeline preserves source appearance and whether it emits a canonical exchange format.

- If preserving appearance, keep a valid embedded ICC color space through rendering and encoding where the destination supports it.
- If canonicalizing, render through a named, calibrated destination such as sRGB or Display P3. Record the conversion in artifact metadata owned by the application, not by copying arbitrary source tags.
- Do not silently assign sRGB to untagged or unsupported input and call that preservation. It is a fallback interpretation and should be part of policy.
- Define alpha handling. Preserve straight/premultiplied semantics through rendering, or composite against an explicit background when output cannot retain alpha.
- Reject unsupported indexed, CMYK, Lab, extended-range, or malformed profile inputs when the pipeline cannot prove its intended result. Conversion may be appropriate, but it must be tested.

Color correctness is observable. Validate profile identity/properties and use reference pixel or perceptual comparisons for fixtures where appearance matters.

## Incremental sources

For streamed bytes:

1. create one incremental image source;
2. append only while accumulated bytes, elapsed time, and expected dimensions remain in policy;
3. use `CGImageSourceUpdateData` with the correct final flag;
4. inspect source and selected-image status to distinguish incomplete, complete, and invalid input;
5. decode only at policy-approved milestones;
6. stop on cancellation, byte/time limits, terminal invalid status, or completion.

An incremental preview is not final evidence. Revalidate properties and final output after the source becomes complete.

## Vision analysis and admission

Keep decode/normalization separate from request policy. A serialized owner or bounded task group should enforce:

- maximum concurrent decodes and Vision requests;
- queue, reject, or latest-wins behavior;
- cancellation propagation and a session generation;
- stale-result suppression after cancellation or replacement;
- bounded memory across queued and active images.

Do not move CPU-heavy decode or analysis onto `MainActor`. Publish only the final UI state on the main actor. Cancellation is an intent signal; if an underlying decoder or framework call completes late, discard its result when the generation no longer matches.

Choose the Vision request family against the package or app deployment floor. Swift-native `RecognizeTextRequest` and `ClassifyImageRequest` are not drop-in declarations for every OS version supported by the legacy `VNRequest` APIs. Put the modern path behind compile-time and runtime availability checks, preserve equivalent orientation/result policy in any legacy path, and exercise both paths on their oldest supported OS.

### OCR evidence

Record only what the feature needs:

- request settings and relevant OS/request revision;
- the selected candidate string, confidence, and an application-owned stable result index when needed;
- alternative candidates when ambiguity affects behavior;
- normalized region plus the coordinate/orientation contract;
- language information when it drives downstream behavior.

Normalize whitespace only after retaining or deliberately discarding spatial structure. Do not merge lines, repair spelling, or infer document order without an explicit product rule.

### Classification evidence

Retain the scored candidate set needed by the acceptance rule. Apply a minimum confidence, ambiguity margin when appropriate, an allowed-label map, and an explicit unknown result. Keep UI labels separate from framework identifiers so localization and product wording do not rewrite evidence.

## Encode and validate

Build an output destination using an explicitly supported UTI, an expected image count, and a deliberate metadata dictionary. Treat failure to create the destination or finalize it as a hard failure.

After finalization, create a new image source from the encoded bytes and verify:

- source status is complete and the type matches the requested output;
- image count, width, height, orientation convention, alpha, and color policy;
- decoded pixels are available under the same safety limits;
- retained metadata is allowlisted and stripped metadata is absent;
- any content digest is computed over a clearly defined representation.

PNG is lossless for represented pixels, but the file bytes are not automatically a canonical serialization. If stable hashes are required, define the exact pixel buffer, row order, channel order, color space, alpha convention, metadata, and encoder boundary that the hash covers.

## Privacy and diagnostics

Prefer stage and policy telemetry: compressed-byte bucket, admitted dimensions, decode/analysis duration, cancellation, result count, and redacted error class. Avoid raw OCR content, candidate labels tied to user content, pixels, thumbnails, file paths, pasteboard values, or source metadata.

Derived images should carry only required metadata. In particular, do not copy EXIF, GPS, camera, author, comment, or XMP dictionaries by default. If preservation is a user-facing feature, make it explicit and test each retained field.
