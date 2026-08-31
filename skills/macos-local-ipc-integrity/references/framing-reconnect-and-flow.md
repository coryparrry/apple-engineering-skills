# Framing, Reconnect, and Flow Control

Read this when changing the byte protocol, JSON-RPC mapping, receive/write loops, queue limits, reconnect, idempotency, or replay.

## Transport Choice

Use MCP stdio for one lifecycle-coupled parent/child, a Unix-domain stream socket for multiple clients or independent lifetimes, and Network framework when its state machine or custom framer is already justified. For an Apple-native same-host service with typed interfaces and system connection lifecycle, evaluate `NSXPCConnection`/`NSXPCListener` before inventing a byte protocol. Account respectively for stdout/pipe ownership, rendezvous and peer identity, or receive re-arming and SDK availability. Do not add a daemon or privileged helper merely to avoid owning a child process.

## Incremental Framing

The framing grammar belongs to the chosen transport; do not substitute a custom socket grammar for a standard protocol's framing.

For MCP stdio, follow the negotiated MCP transport specification: each UTF-8 JSON-RPC message is a single line, newline-delimited, with no embedded newline. Buffer arbitrary read chunks until a delimiter, enforce a maximum encoded line length while accumulating, reject invalid UTF-8 or invalid JSON-RPC, and keep stdout exclusively for MCP messages. See the [MCP stdio transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports#stdio).

For a custom Unix-domain byte stream, document and use one grammar in both directions, such as:

- a fixed-width unsigned length in a documented byte order; or
- bounded ASCII headers ending in `\r\n\r\n`, exactly one valid decimal `Content-Length`, then that many bytes.

Set header, body, undecoded-buffer, and per-cycle limits. Reject oversize before allocation, signs, overflow, conflicting lengths, or unassignable trailing bytes.

One decoder owns its buffer and delimiter or prefix/header/body state. Each read extracts zero or more frames and preserves leftovers. Decode after completion; EOF is valid only between frames unless half-close is explicit.

Give each connection one receiver and serialized writer. POSIX writes advance an offset until the frame completes, retry interruption, and classify reset or broken pipe as ambiguous. `FileHandle` or Network framework completion still proves no more than transport progress.

## JSON-RPC and MCP

JSON-RPC `id` pairs one exchange; put stable operation identity in the typed method contract. Do not reflect raw input in errors. Notifications are one-way or separately reconciled, and batches are independent unless a method explicitly creates a transaction. Preserve MCP negotiation and JSON-RPC semantics.

## Bounded Flow

Track undecoded, request, output, in-flight, and global byte/count totals. Apply limits before large copies or decoding and fair-schedule clients. On output pressure, pause admission or close the slow peer. Closing a peer may lose the transport response, so a post-submission caller observes `unknown` and uses durable operation lookup; the implementation must not claim that every outcome was delivered.

## Reconnect and Replay

Model `idle -> connecting -> negotiating -> ready -> draining/failed -> closed`, with one terminal owner for cleanup.

For a mutation:

1. Create one operation ID before sending; persist it for caller restart.
2. Retry only the same canonical request under that ID.
3. After uncertain disconnect, negotiate and query status with bounded backoff.
4. Resubmit only when the authority proves no match and permits it.
5. Accept cached results only when principal, kind, and digest match.

Define completed-record retention together with a maximum retry age or durable business key; expiry must not let a very late retry repeat a mutation silently.
