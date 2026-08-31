# Apple documentation review

Last reviewed through Xcode `DocumentationSearch` and the installed Apple SDK declarations: **2026-08-30**.

## Scope and freshness

This review covers current-process Accessibility trust, PID-bound `AXUIElement` clients, `AXObserver` registration/run-loop ownership, attribute error handling, secure text-field classification, and macOS protected-resource reset behavior. The lifecycle, consent, privacy, and runtime-proof policy in this skill is application-level guidance derived from those API contracts.

Xcode `DocumentationSearch` did not return dedicated symbol pages for several legacy ApplicationServices C APIs during this review. Their exact declarations and header comments were therefore checked in the current Xcode macOS SDK's `ApplicationServices.framework/Frameworks/HIServices.framework/Headers`. Re-run both DocumentationSearch and SDK-header checks when changing those areas. Do not mark `apple-docs-reviewed` current from a general accessibility UI article alone.

Fresh query used for this review: `Accessibility client App Sandbox incompatible CFRunLoopRemoveSource callback quiescence AXUIElement cannotComplete action retry timeout`.

## Xcode DocumentationSearch URIs consulted

- `/documentation/Xcode/resetting-access-to-protected-resources-in-macOS`
- `/documentation/Security/protecting-user-data-with-app-sandbox#Review-functionality-that-is-incompatible-with-App-Sandbox`
- `/documentation/CoreFoundation/CFRunLoopRemoveSource(_:_:_:)`
- `/documentation/Xcode/resetting-access-to-protected-resources-in-macOS#Look-up-a-service-name`
- `/documentation/Xcode/resetting-access-to-protected-resources-in-macOS#Reset-access`
- `/documentation/Accessibility/accessibility-api`
- `/documentation/Accessibility/integrating-accessibility-into-your-app`
- `/documentation/AppKit/NSAccessibilityProtocol`
- `/documentation/AppKit/accessibility-functions`

The last four documents describe accessibility support exposed by an app. They were consulted to preserve the routing boundary: this skill is for an Accessibility client inspecting or controlling other processes, not for implementing an app's own accessible interface.

## Apple SDK declarations consulted

- `ApplicationServices.framework/Frameworks/HIServices.framework/Headers/AXUIElement.h`
  - `AXIsProcessTrusted`
  - `AXIsProcessTrustedWithOptions`
  - `kAXTrustedCheckOptionPrompt`
  - `AXUIElementCreateApplication`
  - `AXUIElementCopyAttributeValue`
  - `AXUIElementPerformAction`
  - `AXObserverCreate`
  - `AXObserverAddNotification`
  - `AXObserverRemoveNotification`
  - `AXObserverGetRunLoopSource`
- `ApplicationServices.framework/Frameworks/HIServices.framework/Headers/AXRoleConstants.h`
  - `kAXSecureTextFieldSubrole`
- `ApplicationServices.framework/Frameworks/HIServices.framework/Headers/AXAttributeConstants.h`
  - `kAXRoleAttribute`
  - `kAXSubroleAttribute`
  - `kAXValueAttribute`
- `ApplicationServices.framework/Frameworks/HIServices.framework/Headers/AXError.h`
