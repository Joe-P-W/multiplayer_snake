import socket
import threading

from constants.connection_details import ADDRESS, SERVER
from connection_handler.connection import Connection

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(connection: socket.socket, address):
    print(f"[NEW CONNECTION] {address} has connected to the server.")
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    with Connection(connection, address) as client_connection:
        client_connection()

    print(f"[DISCONNECTION] {address} has disconnected")
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()


print("[STARTING] Server is starting.")
start()
