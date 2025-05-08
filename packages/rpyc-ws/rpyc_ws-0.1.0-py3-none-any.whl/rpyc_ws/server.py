"""
ASGI application factory for RPyC over WebSocket.
"""

import asyncio

from rpyc.utils.classic import connect_stream
from websockets.exceptions import ConnectionClosed

from rpyc_ws.stream import WebSocketStream


async def rpyc_handler(websocket, path):
    # wrap the raw WebSocket in your Stream API
    stream = WebSocketStream(websocket)
    # get current event loop
    loop = asyncio.get_running_loop()
    # establish a classic (SlaveService) RPyC connection over it in executor
    conn = await loop.run_in_executor(None, connect_stream, stream)
    try:
        # serve_all() is blocking—run it in a thread so we don't block the event loop
        await loop.run_in_executor(None, conn.serve_all)
    finally:
        # close the connection in executor to avoid blocking the event loop
        await loop.run_in_executor(None, conn.close)


class ASGIWebSocketAdapter:
    def __init__(self, receive, send):
        self._receive = receive
        self._send = send

    async def recv(self):
        event = await self._receive()
        event_type = event["type"]
        if event_type == "websocket.receive":
            if "bytes" in event:
                return event["bytes"]
            elif "text" in event:
                return event["text"].encode()
        elif event_type == "websocket.disconnect":
            raise ConnectionClosed(1000, "Client disconnected")
        return b""

    async def send(self, data):
        if isinstance(data, bytes):
            await self._send({"type": "websocket.send", "bytes": data})
        else:
            await self._send({"type": "websocket.send", "text": data})

    async def close(self):
        await self._send({"type": "websocket.close", "code": 1000})


def create_rpyc_asgi_app(path: str = "/"):
    """
    Factory method to create an ASGI app for RPyC over WebSocket.

    path: WebSocket path to mount on (default "/")
    """

    async def asgi_app(scope, receive, send):
        if scope.get("type") != "websocket" or scope.get("path") != path:
            # Not a WebSocket or wrong path, return 404
            await send(
                {
                    "type": "http.response.start",
                    "status": 404,
                    "headers": [(b"content-type", b"text/plain")],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": b"Not Found",
                }
            )
            return

        # Accept the WebSocket connection
        await send({"type": "websocket.accept"})

        adapter = ASGIWebSocketAdapter(receive, send)
        # Delegate to existing RPyC handler
        await rpyc_handler(adapter, scope.get("path", ""))

    return asgi_app
