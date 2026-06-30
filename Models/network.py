import socket

HOST = "127.0.0.1"
PORT = 6767

class NetworkModel:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: str):
        self.socket.sendto(message.encode("utf-8"), (HOST, PORT))

    def receive(self, buffer: int = 4096) -> str:
        data, _ = self.socket.recvfrom(buffer)
        return data.decode("utf-8")

    def close(self):
        self.socket.close()
