# Purchase and Spend

Read this only when a StoreKit purchase grants server-owned value that a player may spend.

## Separate state machines

Never represent purchase initiation, verified transaction ingestion, entitlement grant, and spend as one client command.

```text
StoreKit purchase
  -> signed transaction evidence
  -> server verifies evidence and signed account binding
  -> idempotent GrantReceipt(transactionID)
  -> server-owned balance increases
  -> SpendCommand depends on the grant receipt or resulting revision
  -> atomic authorization, balance check, debit, and result
```

The server catalog maps a verified product ID to a fixed entitlement. The client never supplies the amount, reward, or exchange rate.

## Typed records

Use equivalents of:

- `PurchaseEvidence(transactionID, signedData, appAccountToken, internalPlayerID)`
- `GrantReceipt(transactionID, grantID, balanceRevision, status)`
- `SpendCommand(commandID, amountOrOfferID, expectedRevision?, dependsOnGrantID?)`
- statuses `pendingVerification`, `granted`, `rejected`, `spent`, and `needsReconfirmation`

At purchase, supply an application-owned UUID through `Product.PurchaseOption.appAccountToken(_:)`. After verification, require the signed `Transaction.appAccountToken` to match the authenticated internal player mapping before granting. If another equally strong server-side binding is used, document and test why signed evidence cannot be replayed onto a different player. Never trust an unsigned client-supplied `internalPlayerID` as the binding. If Game Center account binding changes, suspend and reconfirm rather than applying work to the new account.

## Ordering and failure

- If spend arrives before its declared grant, hold it only until a documented short expiry or reject it with a stable dependency result. Expose query/cancel status and never speculate that the purchase will pass.
- If verification fails, grant nothing and reject dependent spend without debiting another balance.
- Duplicate purchase evidence returns the original grant receipt.
- Grant and spend use separate idempotency keys and transactions.
- A grant may advance the balance revision. Resolve a declared dependency against the resulting revision; unrelated stale spends require normal conflict/reconfirmation handling.
- Query transaction/grant/command status after timeouts. Do not infer outcome from UI dismissal or network failure.

## Offline and App Attest

Distinguish a transaction verified before connectivity was lost from a purchase merely initiated or displayed as pending offline. Only verified evidence can enter the grant flow. A player may queue spend intent, but it remains bounded-pending or rejected until the grant receipt exists; UI state never proves purchase completion.

For a spend policy that requires App Attest:

1. Persist the immutable semantic command and ID offline without an assertion.
2. On reconnect, authenticate the same internal player.
3. Fetch a fresh single-use server challenge.
4. Generate an assertion bound to the command semantics, actor, and challenge.
5. Submit assertion and command; query by command ID after uncertain delivery.

Do not prefetch a reusable challenge pool. A fresh assertion is transport evidence, not command semantics: exclude challenge/assertion bytes from the semantic idempotency hash while verifying their binding to that hash separately.

## End-to-end test

Delay and duplicate purchase evidence, queue spend offline, reconnect, grant, then deliver spend repeatedly. Assert one grant, one debit, no negative balance, correct player binding, and stable receipts. Repeat with failed verification, account change, stale unrelated revision, invalid assertion, and process death between each boundary.
