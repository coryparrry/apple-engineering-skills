# Apple documentation review

Last reviewed through Xcode `DocumentationSearch`: **2026-08-30**.

## Scope and freshness

This review covers ScreenCaptureKit usage-description and first-grant restart guidance, output registration, start/stop callbacks, terminal delegate events, shareable-content filtering, one-frame capture, and CoreGraphics Screen Recording permission preflight/request APIs. The skill adds application-level ownership, teardown, privacy, and runtime-proof guidance; Apple does not prescribe that architecture.

API availability and permission requirements can change by SDK and deployment target. Re-run Xcode `DocumentationSearch` for the exact symbols being changed before updating `apple-docs-reviewed`. Do not infer an async overload or platform availability solely from the callback declaration shown here.

Fresh queries used for this review:

- `ScreenCaptureKit macOS NSScreenCaptureUsageDescription relaunch permission SCStream startCapture stopCapture asynchronous completion output microphone audio permission SCScreenshotManager availability`
- `ScreenCaptureKit SCStreamOutputType microphone macOS NSMicrophoneUsageDescription permission capturesAudio captureMicrophone privacy usage description`
- `ScreenCaptureKit SCStream capturesAudio NSAudioCaptureUsageDescription system audio macOS AudioCapture`
- `SCScreenshotManager macOS availability introduced captureImage contentFilter configuration`

## URIs consulted

Retrieved using Xcode MCP `DocumentationSearch`:

- `/documentation/ScreenCaptureKit`
- `/documentation/ScreenCaptureKit/capturing-screen-content-in-macos#Configure-the-sample-code-project`
- `/documentation/ScreenCaptureKit/SCShareableContent`
- `/documentation/ScreenCaptureKit/SCShareableContent#Retrieving-shareable-content`
- `/documentation/ScreenCaptureKit/SCContentFilter`
- `/documentation/ScreenCaptureKit/SCStream`
- `/documentation/ScreenCaptureKit/SCStream#Adding-and-removing-stream-output`
- `/documentation/ScreenCaptureKit/SCStream/addStreamOutput(_:type:sampleHandlerQueue:)`
- `/documentation/ScreenCaptureKit/SCStream/removeStreamOutput(_:type:)`
- `/documentation/ScreenCaptureKit/SCStream#Starting-and-stopping-a-stream`
- `/documentation/ScreenCaptureKit/SCStream/startCapture(completionHandler:)`
- `/documentation/ScreenCaptureKit/SCStream/stopCapture(completionHandler:)`
- `/documentation/ScreenCaptureKit/SCStreamDelegate/stream(_:didStopWithError:)`
- `/documentation/ScreenCaptureKit/SCStreamOutput/stream(_:didOutputSampleBuffer:of:)`
- `/documentation/ScreenCaptureKit/SCStreamOutputType#Output-types`
- `/documentation/BundleResources/Information-Property-List/NSAudioCaptureUsageDescription`
- `/documentation/BundleResources/Information-Property-List/NSMicrophoneUsageDescription`
- `/documentation/BundleResources/requesting-authorization-for-media-capture-on-macos#Configure-Your-Camera-and-Microphone-Apps`
- `/documentation/AVFoundation/requesting-authorization-to-capture-and-save-media#Enable-entitlements-in-macOS`
- `/documentation/ScreenCaptureKit/SCStreamError/Code#Stream-management`
- `/documentation/ScreenCaptureKit/SCStreamError/Code#User-cancellation`
- `/documentation/ScreenCaptureKit/SCScreenshotManager`
- `/documentation/ScreenCaptureKit/SCScreenshotManager#Individual-frame-capture`
- `/documentation/ScreenCaptureKit/SCScreenshotManager/captureImage(contentFilter:configuration:completionHandler:)`
- `/documentation/ScreenCaptureKit/capturing-screen-content-in-macos#Create-a-content-filter`
- `/documentation/ScreenCaptureKit/capturing-screen-content-in-macos#Start-the-capture-session`
- `/documentation/CoreGraphics/CGPreflightScreenCaptureAccess()`
- `/documentation/CoreGraphics/CGRequestScreenCaptureAccess()`
- `/documentation/Xcode/resetting-access-to-protected-resources-in-macOS`
- `/documentation/Xcode/resetting-access-to-protected-resources-in-macOS#Look-up-a-service-name`
