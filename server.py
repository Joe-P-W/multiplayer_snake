import socket
import threading
import os

HEADER = 16
PORT = 5050
SERVER = os.getenv("snake_server_address")
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_COMMAND = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(connection: socket.socket, address):
    print(f"[NEW CONNECTION] ({address}) has connected to the server.")
    connected = True

    while connected:
        message_length = connection.recv(HEADER,).decode(FORMAT)
        if message_length:
            message_length = int(message_length)

            message = connection.recv(message_length).decode(FORMAT)
            print(f"[CLIENT ACTIVITY] {address} - {message}")

            if message == DISCONNECT_COMMAND:
                print(f"[DISCONNECTION] {address} has disconnected")
                connected = False

    connection.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")


print("[STARTING] Server is starting.")
start()
