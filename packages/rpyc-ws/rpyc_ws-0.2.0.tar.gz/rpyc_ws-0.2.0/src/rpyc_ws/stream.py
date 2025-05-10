from typing import Callable

from rpyc.core.consts import STREAM_CHUNK
from rpyc.core.stream import Stream
from rpyc.lib import Timeout


class CallbackStream(Stream):
    """RPyC stream that uses callbacks to read and write to the stream."""

    __slots__ = ("ws_recv", "ws_send", "ws_close", "ws_closed", "_buf")
    MAX_IO_CHUNK = STREAM_CHUNK

    def __init__(
        self,
        ws_recv: Callable[[float], bytes],
        ws_send: Callable[[bytes], None],
        ws_close: Callable[[], None],
    ):
        self.ws_recv = ws_recv
        self.ws_send = ws_send
        self.ws_close = ws_close
        self._buf = bytearray()

    def close(self):
        self._buf.clear()

    @property
    def closed(self) -> bool:
        return False

    def read(self, count: int):
        out = bytearray()

        # Drain buffered spill-over first
        if self._buf:
            take = self._buf[:count]
            out.extend(take)
            del self._buf[: len(take)]

        while len(out) < count:
            try:
                msg = self.ws_recv(0.01)
            except Exception as exc:
                self.close()
                raise EOFError("connection closed while reading") from exc

            if not msg:
                continue

            needed = count - len(out)
            out.extend(msg[:needed])
            if len(msg) > needed:
                self._buf.extend(msg[needed:])

        return bytes(out)

    def write(self, data: bytes | bytearray | memoryview):
        mv = memoryview(data)
        idx = 0
        try:
            while idx < len(mv):
                chunk = mv[idx : idx + self.MAX_IO_CHUNK]
                self.ws_send(chunk.tobytes())
                idx += len(chunk)
        except Exception as exc:
            self.close()
            raise EOFError("connection closed while writing") from exc

    def poll(self, timeout: float | Timeout | None) -> bool:
        timeout = Timeout(timeout)
        timeout = timeout.timeleft()
        if timeout is not None and timeout <= 0:
            return False

        msg = self.ws_recv(timeout)
        if not msg:
            return False

        self._buf.extend(msg)
        return True
