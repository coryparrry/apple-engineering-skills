# Stream lifecycle and runtime evidence

Read this for persistent `SCStream` setup, callbacks, teardown, and recovery. It defines obligations, not a mandatory architecture.

## Consent and executable identity

Bind every permission and runtime claim to the process that makes capture calls: executable path, bundle ID, signing identity, PID, and launch method. Xcode, command-line helpers, development builds, and installed apps are separate evidence boundaries when their identities differ.

Explain capture before prompting and invoke the prompt only from clear user action. Use `CGPreflightScreenCaptureAccess()` as a current-process signal and `CGRequestScreenCaptureAccess()` deliberately; never loop prompts. Current ScreenCaptureKit documentation requires `NSScreenCaptureUsageDescription`, and Apple's macOS sample says the app must be restarted after the first grant before capture is enabled. Present that as a user-controlled next step; never relaunch automatically.

Inventory output types and bind each to the active SDK/deployment contract. `.screen` uses Screen Recording consent and `NSScreenCaptureUsageDescription`. `.audio` captures system/desktop audio; where the linked SDK requires Audio Capture consent, provide `NSAudioCaptureUsageDescription` and handle the `AudioCapture` TCC service separately. `.microphone` uses Microphone consent and `NSMicrophoneUsageDescription`; a sandboxed macOS app also needs the Audio Input capability. Do not infer one output's grant from another. Do not reset TCC, modify its database, open System Settings, relaunch processes, kill `replayd`, or restart capture services without user authorization.

Capture the narrowest source and shortest duration. Exclude private app windows where applicable. Do not log pixels, OCR, window titles, filter contents, thumbnails, or user text; lifecycle state, dimensions, duration, counters, and redacted error classes are sufficient.

## Setup and callbacks

Use one serialized owner and a session generation. Model at least `idle`, `starting`, `running`, `stopping`, and `terminal`. Transitional states must prevent overlapping start/stop requests from creating multiple streams or releasing a stream while its start completion can still fire.

Build transactionally:

1. Check consent without repeat prompting; retrieve fresh shareable content and a narrow filter.
2. Create configuration, stream, delegate, outputs, and dedicated serial callback queues.
3. Record each successful `(output, type, queue)` attachment.
4. Start capture and retain the transition operation. Publish `running` only after that exact generation's completion succeeds. If stop was requested while starting, do not publish a durable running state; issue one stop after start settles successfully.

On start failure, settle the transition once, remove attached outputs, fence their queues, and release the attempt. Never reuse a half-started stream. A caller cancellation during start records stop intent; it does not immediately tear down objects still reachable from the start completion.

Retain stream, delegate, outputs, and queues for their registration lifetime. Each callback must reject stale/terminal generations, validate status, retain only necessary data, hand off bounded work, and account for accepted/dropped/in-flight frames. Apply newest-frame replacement or a small bounded buffer when processing is slower than capture. Avoid an output/owner retain cycle.

## Idempotent teardown

Use one path after partial setup, start failure, caller cancellation, delegate stop, or repeated stop:

1. Record stop intent for the generation and cancel downstream work.
2. If starting, await or chain from the owned start completion. If start succeeds, request one `stopCapture`; if it fails, skip stop. If already running, request one stop. Coalesce caller stop and delegate stop into the same transition.
3. After the start/stop transition has settled, mark terminal and remove every successfully attached output.
4. From outside each dedicated callback queue, fence it after removal; never synchronously wait from inside that queue.
5. Drain/cancel accepted work, clear references, and publish the terminal result once.

Stopping capture and removing outputs are separate obligations. `stream(_:didStopWithError:)` can race caller stop; route both into this teardown. A registration mismatch is evidence, not a reason to abandon cleanup.

## Bounded recovery

Restart only while capture remains desired and the retry budget is not exhausted. Never retry missing consent or `userStopped`. For a transient system/connection stop, back off, re-enumerate content, re-resolve the source, and build a fresh generation and stream. Starting twice is an application lifecycle bug.

For `SCScreenshotManager`, first check API availability against the deployment target. When available, skip persistent-stream machinery but still bound concurrent requests, use a fresh narrow filter, handle absent-image and error outcomes, cancel downstream work, and discard image data promptly. Older supported systems need a tested one-frame stream fallback or an explicit higher deployment floor.

## Evidence

Record executable path/bundle/signature/PID; generation/source kind; registration/removal counts; start completion/first valid frame; stop/delegate/fence events; callback pressure; and retry reason/attempt/budget. Never record pixels, OCR, titles, application names, thumbnails, or user text.

Validate denied/granted flows, cancellation during transitions, source disappearance, rapid cycles, promised restart, and app quit on the exact executable. A shared macOS service remaining alive does not prove the app still captures.
