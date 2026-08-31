# Distribution-channel boundaries

Choose invariants for the actual channel; never mix their signing expectations.

## App Store and TestFlight

Apple re-signs App Store products. Do not require installed authorities or bundle bytes to match the export. Define which identity is meant—App Store Connect build resource, `CFBundleVersion`, `AppTransaction.appVersionID`, or CI build—and preserve upload/CI evidence plus non-secret provenance. Inspect delivered signing/entitlements only where platform controls expose them; otherwise bind attainable channel/build evidence and mark that observation `unproven`. Only a cryptographically verified receipt or verified `AppTransaction` proves its specific signed fields; sandbox environment alone does not uniquely identify TestFlight. Distinguish TestFlight from production.

## Developer ID

Expected chain: `source -> archive -> Developer ID export -> ZIP/DMG/PKG -> notarization -> download -> installed app`.

Verify each code object’s Developer ID signature, designated/channel requirement, hardened-runtime option, secure timestamp, and app-specific effective entitlements. Separately verify the submitted artifact's notarization result/log, staple and validate the ticket on each supported distributed object, and assess the exact delivered artifact with Gatekeeper/channel policy. ZIPs and standalone binaries cannot be stapled directly. Distinguish PKG and contained-app signatures. DMG, PKG, ZIP, bundle, and executable are separate hash domains.

## Development

Development success is not release evidence. Treat a development identity or `get-task-allow` as expected only for a development claim.

## Ad Hoc

Treat Ad Hoc as a distinct archive export for registered devices. Verify export method, distribution provisioning profile, registered-device coverage, profile expiration, effective entitlements, signing identity, installed build identity, and the exact device tested. Development evidence does not substitute for Ad Hoc evidence.

## Sparkle

Sparkle adds: `signed app -> update archive -> appcast -> download -> validation/install -> relaunched app`.

Record appcast entry, version/build, archive URL/digest, and update signature. Confirm the selected download. After install, recheck Apple signing, entitlements, notarization, version/build, executable hash, and runtime path. Sparkle signing proves neither source revision nor Apple release state; never expose its keys.
