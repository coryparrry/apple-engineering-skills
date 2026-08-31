# Apple Documentation Review

Reviewed with Xcode MCP `DocumentationSearch`: **2026-08-30**.

Scope: Apple trust signals, server identity binding, transaction verification, networking, and bounded background execution. Re-search before changing availability, entitlements, cryptographic validation, purchases, or lifecycle behavior.

Fresh query on 2026-08-30: `StoreKit appAccountToken signed transaction account binding BGTaskRequest earliestBeginDate execution not guaranteed App Attest assertion counter`.

## App Attest

- [Establishing app integrity](https://developer.apple.com/documentation/DeviceCheck/establishing-your-app-s-integrity)
- [Validating server connections](https://developer.apple.com/documentation/DeviceCheck/validating-apps-that-connect-to-your-server)
- [Providing a challenge](https://developer.apple.com/documentation/DeviceCheck/validating-apps-that-connect-to-your-server#Provide-a-challenge)
- [Verifying attestation](https://developer.apple.com/documentation/DeviceCheck/validating-apps-that-connect-to-your-server#Verify-the-attestation)
- [Preparing App Attest](https://developer.apple.com/documentation/DeviceCheck/preparing-to-use-the-app-attest-service)
- [Assessing fraud risk](https://developer.apple.com/documentation/DeviceCheck/assessing-fraud-risk)
- [`DCAppAttestService`](https://developer.apple.com/documentation/DeviceCheck/DCAppAttestService)

Queries: `App Attest establishing app integrity generate key attest assertion server validation replay protection`; `App Attest isSupported failures fallback gradual adoption assertions counters`.

## Game Center

- [Initialize the local player](https://developer.apple.com/documentation/GameKit/initializing-and-configuring-game-center#Initialize-the-local-player)
- [Authenticate a player](https://developer.apple.com/documentation/GameKit/authenticating-a-player)
- [`fetchItems(forIdentityVerificationSignature:)`](https://developer.apple.com/documentation/GameKit/GKLocalPlayer/fetchItems(forIdentityVerificationSignature:))
- [Scoped player identifiers](https://developer.apple.com/documentation/GameKit/protecting-the-player-s-privacy-using-scoped-identifiers)
- [Custom server games](https://developer.apple.com/documentation/GameKit/finding-players-for-custom-server-based-games)

Queries: `Game Center authenticate local player server player identity`; `Game Center server identity verification signature fetchItems authentication is not SSO`.

## StoreKit

- [`Transaction` verification](https://developer.apple.com/documentation/StoreKit/Transaction#Verify-transactions)
- [`VerificationResult`](https://developer.apple.com/documentation/StoreKit/VerificationResult)
- [`AppTransaction` verification](https://developer.apple.com/documentation/StoreKit/AppTransaction#Verifying-the-app-transaction)
- [`Transaction.deviceVerification`](https://developer.apple.com/documentation/StoreKit/Transaction/deviceVerification)
- [`Product.PurchaseOption.appAccountToken(_:)`](https://developer.apple.com/documentation/StoreKit/Product/PurchaseOption/appAccountToken(_:))
- [`Transaction.appAccountToken`](https://developer.apple.com/documentation/StoreKit/Transaction/appAccountToken)
- [Server receipt validation](https://developer.apple.com/documentation/StoreKit/validating-receipts-with-the-app-store)

Queries: `StoreKit 2 Transaction verification result verified unverified AppTransaction currentEntitlements`; `StoreKit server transaction verification`.

## BackgroundTasks and URLSession

- [`BGTaskScheduler`](https://developer.apple.com/documentation/BackgroundTasks/BGTaskScheduler)
- [`BGTaskRequest.earliestBeginDate`](https://developer.apple.com/documentation/BackgroundTasks/BGTaskRequest/earliestBeginDate) — the system may launch later and does not guarantee execution.
- [Long-running iOS tasks](https://developer.apple.com/documentation/BackgroundTasks/performing-long-running-tasks-on-ios-and-ipados)
- [Background downloads](https://developer.apple.com/documentation/Foundation/downloading-files-in-the-background)
- [Background cancellation reasons](https://developer.apple.com/documentation/Foundation/url-session-background-task-cancellation-reasons)
- [`NSURLErrorBackgroundSessionWasDisconnected`](https://developer.apple.com/documentation/Foundation/NSURLErrorBackgroundSessionWasDisconnected-swift.var)
- [`URLSession` asynchronous transfers](https://developer.apple.com/documentation/Foundation/URLSession#Performing-asynchronous-transfers)
- [`URLSessionConfiguration` general properties](https://developer.apple.com/documentation/Foundation/URLSessionConfiguration#Setting-general-properties)

Queries: `iOS background execution limits background tasks URLSession background transfers app suspension`; `URLSession typed Codable requests idempotency retry HTTP status security server APIs`.

## Freshness

Repeat the queries, check availability/platform notes, update guidance/tests, then update metadata. Change `last-reviewed` after review, `last-updated` only after content changes, and `apple-docs-reviewed` only after a fresh Xcode documentation pass.
