# Apple Documentation Index

Reviewed with Xcode MCP `DocumentationSearch` on **2026-08-30** for Foundation process streams, Network framework connections/listeners, and custom framing. Search again when the SDK, deployment target, or transport differs.

Fresh query used for this review: `NSXPCListener accept connection code signing requirement interruption invalidation FileHandle pipe EOF NWConnection receive framing`.

## Foundation

- Process endpoints: [`standardInput`](https://developer.apple.com/documentation/Foundation/Process/standardInput), [`standardOutput`](https://developer.apple.com/documentation/Foundation/Process/standardOutput), and [`standardError`](https://developer.apple.com/documentation/Foundation/Process/standardError).
- Pipe endpoints: [`fileHandleForReading`](https://developer.apple.com/documentation/Foundation/Pipe/fileHandleForReading) and [`fileHandleForWriting`](https://developer.apple.com/documentation/Foundation/Pipe/fileHandleForWriting); closing the writer signals end-of-data.
- Byte I/O: [`FileHandle.bytes`](https://developer.apple.com/documentation/Foundation/FileHandle/bytes), [`read(upToCount:)`](https://developer.apple.com/documentation/Foundation/FileHandle/read(upToCount:)), [`write(contentsOf:)`](https://developer.apple.com/documentation/Foundation/FileHandle/write(contentsOf:)), and [`close()`](https://developer.apple.com/documentation/Foundation/FileHandle/close()). A write is transport progress, not application commit.

## Network

- [`NWConnection` data operations](https://developer.apple.com/documentation/Network/NWConnection#Sending-and-Receiving-Data), one-shot [`receive(minimumIncompleteLength:maximumLength:completion:)`](https://developer.apple.com/documentation/Network/NWConnection/receive(minimumIncompleteLength:maximumLength:completion:)), [`SendCompletion`](https://developer.apple.com/documentation/Network/NWConnection/SendCompletion), and [`State`](https://developer.apple.com/documentation/Network/NWConnection/State-swift.enum).
- [`NWListener` creation/state](https://developer.apple.com/documentation/Network/NWListener#Creating-Listeners) and [connection admission](https://developer.apple.com/documentation/Network/NWListener#Receiving-Connections).
- Custom framing: [`NWProtocolFramer`](https://developer.apple.com/documentation/Network/NWProtocolFramer), [`NWProtocolFramerImplementation`](https://developer.apple.com/documentation/Network/NWProtocolFramerImplementation), and [`handleOutput(framer:message:messageLength:isComplete:)`](https://developer.apple.com/documentation/Network/NWProtocolFramerImplementation/handleOutput(framer:message:messageLength:isComplete:)).
- Local-address surfaces: [`nw_endpoint_create_address(_:)`](https://developer.apple.com/documentation/Network/nw_endpoint_create_address(_:)), [Foundation streams, sockets, and ports](https://developer.apple.com/documentation/Foundation/streams-sockets-and-ports), and [`SocketPort` with `AF_LOCAL`](https://developer.apple.com/documentation/Foundation/SocketPort/init(remoteWithProtocolFamily:socketType:protocol:address:)).

Xcode search returned no high-level Swift `NWEndpoint.unix` constructor. Do not invent one; verify the current SDK before choosing Network framework or POSIX Unix-domain sockets.

## XPC routing boundary

- [`NSXPCListener`](https://developer.apple.com/documentation/Foundation/NSXPCListener) and [providing access to clients](https://developer.apple.com/documentation/Foundation/NSXPCListener#Providing-access-to-clients)
- [`NSXPCListener` code-signing checks](https://developer.apple.com/documentation/Foundation/NSXPCListener#Working-with-code-signing)
- [`NSXPCListener` connection state](https://developer.apple.com/documentation/Foundation/NSXPCListener#Managing-connection-state)
- [`NSXPCConnection` interface configuration](https://developer.apple.com/documentation/Foundation/NSXPCConnection#Managing-the-connection-interface) and [connection state](https://developer.apple.com/documentation/Foundation/NSXPCConnection#Managing-connection-state)
