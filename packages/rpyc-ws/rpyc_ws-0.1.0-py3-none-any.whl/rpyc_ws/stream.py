"""
stream.py

Provides WebSocketStream: a Stream implementation over asyncio WebSockets
using the `websockets` library, suitable for RPyC transport.
"""

import asyncio
import queue
import threading

from rpyc.core.consts import STREAM_CHUNK
from rpyc.core.stream import Stream
from rpyc.lib import Timeout
from websockets.exceptions import ConnectionClosed


class WebSocketStream(Stream):
    """
    A Stream implementation on top of an asyncio WebSocket (`websockets` library).
    Must be instantiated within an asyncio event loop thread; it spawns reader/writer tasks
    to shuttle data between the WebSocket and the synchronous RPyC layer.
    """

    MAX_IO_CHUNK = STREAM_CHUNK

    def __init__(self, websocket):
        self._websocket = websocket
        self._in_q = queue.Queue()
        self._out_q = queue.Queue()
        self._inbuf = bytearray()
        self._closed = False
        # Detect async or sync context
        try:
            self._loop = asyncio.get_running_loop()
            self._async = True
        except RuntimeError:
            self._loop = None
            self._async = False

        # launch background threads
        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._reader_thread.start()
        self._writer_thread = threading.Thread(target=self._writer_loop, daemon=True)
        self._writer_thread.start()

    def _reader_loop(self):
        try:
            while True:
                if self._async:
                    future = asyncio.run_coroutine_threadsafe(
                        self._websocket.recv(), self._loop
                    )
                    msg = future.result()
                else:
                    msg = self._websocket.recv()
                if isinstance(msg, str):
                    data = msg.encode()
                else:
                    data = msg
                self._in_q.put(data)
        except ConnectionClosed:
            pass
        finally:
            # signal EOF
            self._in_q.put(None)

    def _writer_loop(self):
        try:
            while True:
                data = self._out_q.get()
                if data is None:
                    break
                if self._async:
                    future = asyncio.run_coroutine_threadsafe(
                        self._websocket.send(data), self._loop
                    )
                    future.result()
                else:
                    self._websocket.send(data)
        except ConnectionClosed:
            pass

    def read(self, count):
        """
        Read exactly `count` bytes, or raise EOFError if the websocket closed.
        """
        if count <= 0:
            return b""
        while len(self._inbuf) < count:
            chunk = self._in_q.get()
            if chunk is None:
                raise EOFError("WebSocket closed")
            self._inbuf.extend(chunk)
        result = bytes(self._inbuf[:count])
        del self._inbuf[:count]
        return result

    def write(self, data):
        """
        Queue `data` for sending as a WebSocket message.
        """
        if self._closed:
            raise EOFError("WebSocketStream is closed")
        self._out_q.put(data)

    def poll(self, timeout):
        """
        Return True if there is data ready to read within `timeout` seconds.
        """
        timeout = Timeout(timeout)
        if self._inbuf:
            return True
        try:
            chunk = self._in_q.get(timeout=timeout.timeleft())
        except queue.Empty:
            return False
        if chunk is None:
            return False
        self._inbuf.extend(chunk)
        return True

    def fileno(self):
        """
        Not supported for WebSocketStream.
        """
        raise NotImplementedError("fileno() not supported by WebSocketStream")

    @property
    def closed(self):
        return self._closed

    def close(self):
        """
        Close the WebSocketStream: stop writer, and close the underlying websocket.
        """
        if not self._closed:
            self._closed = True
            # wake up writer so it can exit
            self._out_q.put(None)
            # schedule websocket close appropriately
            if self._async:
                self._loop.call_soon_threadsafe(
                    asyncio.create_task, self._websocket.close()
                )
            else:
                try:
                    self._websocket.close()
                except Exception:
                    pass
