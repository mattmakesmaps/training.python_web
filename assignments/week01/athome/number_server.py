__author__ = 'matt'
"""
1. Create a socket server which can take two numbers, add them together, and
return the result

Reference:
http://www.binarytides.com/python-socket-programming-tutorial/2/
"""

import socket
import sys
from ast import literal_eval

# create socket
server_socket = socket.socket()
try:
    addy = ('127.0.0.1',8888)
    print "Server Starting %s" % (str(addy))
    # bind socket
    server_socket.bind(('127.0.0.1',8888))
    # backlog of 5
    server_socket.listen(5)
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

while 1:
    conn, addr = server_socket.accept()
    print "Connection Established."
    # Keep connection alive.
    while 1:
        data = conn.recv(4096)
        if data:
            listIn = literal_eval(data)
            print 'Values: %s, Type: %s' % (listIn, type(listIn))
            conn.sendall('Sum: %s\n' % sum(listIn))
        else:
            pass

conn.close()
server_socket.close()
