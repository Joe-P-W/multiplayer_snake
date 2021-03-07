import json
import socket

from constants.connection_details import ADDRESS, FORMAT, HEADER


class ClientConnection:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.client.connect(ADDRESS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def send_json(self, body: dict):
        self.send(json.dumps(body))

    def send(self, message: str):
        message = message.encode(FORMAT)
        message_length = len(message)
        send_length = str(message_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
