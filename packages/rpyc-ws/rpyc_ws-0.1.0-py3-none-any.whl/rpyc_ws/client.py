from contextlib import contextmanager

from rpyc.utils.classic import connect_stream
from websockets.sync.client import connect

from rpyc_ws.stream import WebSocketStream


@contextmanager
def connect_ws(uri: str):
    with connect(uri) as websocket:
        stream = WebSocketStream(websocket)
        yield connect_stream(stream)
