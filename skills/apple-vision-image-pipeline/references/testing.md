# Image pipeline verification matrix

Use fixtures whose licensing and provenance permit repository use. Generate synthetic hostile images when practical, and keep expected policy outcomes next to each fixture. Tests should exercise observable contracts rather than match implementation wording.

## Decode safety

Cover:

- empty and random bytes;
- valid headers followed by truncation;
- compressed input exactly below, at, and above the byte limit;
- dimensions and decoded-pixel estimates at each boundary;
- arithmetic overflow and values that cannot convert safely to the chosen integer type;
- a tiny compressed file declaring or decoding to extreme dimensions;
- unsupported and mismatched extension, MIME, UTI, pasteboard type, and actual ImageIO type;
- zero, one, and multiple images/frames according to policy;
- incomplete, complete, and invalid incremental-source statuses;
- cancellation and timeout while bytes are arriving;
- concurrent inputs whose individual sizes pass but aggregate memory must be bounded.

Measure peak memory on representative hardware for high-risk limits. Passing unit arithmetic does not prove the decoder stays inside the process budget.

## Orientation and coordinates

Use an asymmetric fixture with labeled corners and test every supported `CGImagePropertyOrientation`, including mirrored values. Verify:

- visible upright pixels;
- final width and height after quarter-turn transforms;
- Vision input orientation;
- OCR/classification region mapping to the source and displayed image;
- crop and scale transforms;
- output metadata is `.up` or absent after pixel normalization;
- no file/clipboard path applies a second transform.

Do not use a rotationally symmetric fixture; it cannot detect several orientation defects.

## Color and alpha

Include tagged sRGB and Display P3 images, grayscale, alpha edges, untagged RGB, and every additional model the product claims to accept. When relevant, include a malformed or unsupported ICC profile and extended-range input.

Verify the declared behavior: preserve, convert, or reject. Check encoded profile properties and compare decoded reference pixels or a bounded perceptual metric. A screenshot comparison alone can hide display-managed conversion.

## File and clipboard equivalence

Feed identical encoded fixture bytes through each source adapter. Assert equal:

- detected type and admission decision;
- decoded/oriented dimensions and color contract;
- normalized pixel digest when the pipeline defines one;
- Vision request configuration and coordinate transform;
- accepted OCR/classification evidence after applying the same tolerances;
- encoded artifact policy and retained metadata.

If a clipboard representation cannot preserve the original bytes, test the documented canonicalization boundary instead of claiming byte equivalence.

## OCR

Use fixtures for supported scripts, mixed languages, low contrast, small text near the configured height threshold, rotated/mirrored text, repeated lines, punctuation, and no-text images.

Assert product rules such as required phrases, minimum candidate confidence, valid normalized regions, reading-order policy, and the distinction between no result and request failure. Avoid exact full transcripts or confidence values when framework/OS revisions may legitimately change them.

## Classification

Use clear positive, clear negative, ambiguous, out-of-domain, and adversarially cropped fixtures. Exercise confidence thresholds, ambiguity margins, allowed-label mapping, and unknown results. Do not convert a missing label into a confident negative unless that is the documented model contract.

## Concurrency and lifecycle

Verify maximum in-flight decode and analysis counts, chosen overload behavior, cancellation before/during/after Vision, stale-result rejection, owner teardown, and bounded queues. Include rapid replacement of one image by another and app/feature shutdown while analysis is active.

## Output and privacy

For each successful encoded artifact, reopen it with a fresh image source and verify type, complete status, frame count, dimensions, orientation, alpha, color, and pixel availability. Test finalization failure if the destination abstraction permits injection.

Inspect the output metadata dictionary for an allowlist. Verify GPS, camera, author, comment, XMP, and source-specific private fields are absent unless explicitly preserved. Confirm diagnostics and logs do not contain pixels, OCR text, filenames, pasteboard contents, thumbnails, or raw metadata.
