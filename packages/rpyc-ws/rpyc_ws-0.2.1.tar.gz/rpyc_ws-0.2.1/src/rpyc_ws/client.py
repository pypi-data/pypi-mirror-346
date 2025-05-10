from functools import wraps

from rpyc.utils.classic import connect_stream
from websockets.sync.client import connect

from rpyc_ws.stream import CallbackStream


@wraps(connect)
def connect_ws(*args, **kwargs):
    websocket = connect(*args, **kwargs)

    def receive_bytes(timeout: float):
        try:
            result = websocket.recv(timeout, False)
            return result
        except TimeoutError:
            return None

    def send_bytes(data: bytes):
        websocket.send(data)

    def close():
        websocket.close()

    stream = CallbackStream(receive_bytes, send_bytes, close)
    return connect_stream(stream)
