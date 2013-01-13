"""
2. Create a socket client that sends two numbers to the above server, and
receives and prints the returned result.
"""
import socket
import sys

client_socket = socket.socket()

try:
    client_socket.connect(('127.0.0.1', 8888))
except socket.error, msg:
    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Send a list of numbers
listIn = [0,1,2,3]
client_socket.sendall(str(listIn))
response = client_socket.recv(4096)
print response

# close socket.
client_socket.close()
