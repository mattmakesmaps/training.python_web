import socket
import sys

# Create a TCP/IP socket
client_socket = socket.socket()

# Connect the socket to the port where the server is listening
server_address = ('localhost', 50000)
client_socket.connect(server_address)

try:
    # Send data
    message = 'This is the message.  It will be repeated.'
    client_socket.sendall(message)

    # print the response
    # try to recieve data in smaller chunks, and close
    # when it's recieved data the same size as the message sent.
    counter = 0
    while counter < len(message):
        data = client_socket.recv(8)
        print "Response: %s" % data
        counter += len(data)

finally:
    # close the socket to clean up
    client_socket.close()
