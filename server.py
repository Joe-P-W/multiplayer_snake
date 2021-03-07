import socket
import threading

from constants.connection_details import ADDRESS, SERVER
from server_connection_handler.server_connection import ServerConnection


def handle_client(connection: socket.socket, address: tuple):
    print(f"[NEW CONNECTION] {address} has connected to the server.")
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    with ServerConnection(connection, address) as server_connection:
        server_connection()

    print(f"[DISCONNECTION] {address} has disconnected")
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


def run_server(server: socket.socket):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    print("[STARTING] Server is starting.")
    run_server(server)
