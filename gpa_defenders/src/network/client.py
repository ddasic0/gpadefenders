
import json
import socket
import threading
from queue import Empty, Queue

PORT = 5555


class NetworkClient:

    def __init__(self):
        self.player_id: int | None = None
        self.connected: bool = False
        self.game_started: bool = False
        self.selected_map_id: str | None = None
        self._sock: socket.socket | None = None
        self._inbox: Queue[dict] = Queue()
        self._buf: bytes = b""

                                                                                

    def connect(self, host: str, port: int = PORT, timeout: float = 5.0) -> bool:
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(timeout)
            self._sock.connect((host, port))
            self._sock.settimeout(None)
            self.connected = True
            threading.Thread(target=self._recv_loop, daemon=True).start()
            return True
        except OSError as e:
            print(f"[Client] Verbinding mislukt: {e}")
            return False

    def disconnect(self) -> None:
        self.connected = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass

                                                                                

    def send(self, msg: dict) -> None:
        if not self.connected or self._sock is None:
            return
        try:
            self._sock.sendall(json.dumps(msg).encode() + b"\n")
        except OSError:
            self.connected = False

    def poll(self) -> dict | None:
        try:
            return self._inbox.get_nowait()
        except Empty:
            return None

                                                                                

    def _recv_loop(self) -> None:
        while self.connected:
            try:
                chunk = self._sock.recv(4096)
                if not chunk:
                    break
                self._buf += chunk
                while b"\n" in self._buf:
                    line, self._buf = self._buf.split(b"\n", 1)
                    msg = json.loads(line)
                    self._on_message(msg)
            except (OSError, json.JSONDecodeError):
                break
        self.connected = False

    def _on_message(self, msg: dict) -> None:
        if msg["type"] == "CONNECTED":
            self.player_id = msg["player_id"]
        elif msg["type"] == "GAME_START":
            self.game_started = True
        elif msg["type"] == "MAP_SELECTED":
            self.selected_map_id = msg.get("map_id")
        self._inbox.put(msg)
