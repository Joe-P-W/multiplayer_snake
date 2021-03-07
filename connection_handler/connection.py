import socket
from constants.connection_details import HEADER, FORMAT, DISCONNECT_COMMAND


class Connection:
    def __init__(self, connection: socket.socket, address):
        self.connected = True
        self.connection = connection
        self.address = address

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def __call__(self):
        while self.connected:
            message_length = self.connection.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)

                message = self.connection.recv(message_length).decode(FORMAT)
                print(f"[CLIENT ACTIVITY] {self.address} - {message}")

                if message == DISCONNECT_COMMAND:
                    self.connected = False
