from client_connection_handler.client_connection import ClientConnection

with ClientConnection() as connection:
    connection.send_json({'foo': "bar"})
    connection.send("!DISCONNECT")
