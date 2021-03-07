import socket

from constants.connection_details import ADDRESS, HEADER, FORMAT, DISCONNECT_COMMAND


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
    message = msg.encode(FORMAT)
    print(message)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


while True:
    msg = input("What do you want to send? ")
    send(msg)

    if msg == DISCONNECT_COMMAND:
        break
