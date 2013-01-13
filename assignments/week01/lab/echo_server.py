import socket
import sys

# Create a TCP/IP socket
server_socket = socket.socket()

# Bind the socket to the port
server_address = ('localhost', 50000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

while True:
    # Wait for a connection
    connection, addr = server_socket.accept()

    try:
        # Receive the data and send it back
        data = connection.recv(4096)
        connection.sendall(data)

    finally:
        # Clean up the connection
        server_socket.close()
