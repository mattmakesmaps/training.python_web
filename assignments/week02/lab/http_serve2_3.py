#!/usr/bin/env python

import socket, re

def ok_response(body):
    """Return a formatted HTTP Response."""
    header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n'
    response = header + body
    return response

def client_error_response(body):
    """Return a formatted HTTP Response."""
    header = 'HTTP/1.0 400 BAD REQUEST\r\nContent-Type: text/plain\r\n\r\n'
    response = header + body
    return response

def parse_request(request):
    """Return the URI from the header"""
    # Create a list from the first line of the request header.
    # Should be formatted ['VERB','URI','PROTOCOL']
    uriHeader = request.splitlines()[0].split()
    # Only return URI if valid GET and HTTP.
    if uriHeader[0] == 'GET' and 'HTTP' in uriHeader[2]:
        return uriHeader[1]
    else:
        raise ValueError

host = '' # listen on all connections (WiFi, etc) 
port = 50030
backlog = 5 # how many connections can we stack up
size = 1024 # number of bytes to receive at once

## create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# set an option to tell the OS to re-use the socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# the bind makes it a server
s.bind( (host,port) )
s.listen(backlog)
html = open('./tiny_html.html','r').read()

response = ok_response(html)

while True: # keep looking for new connections forever
    try:
        client, address = s.accept() # look for a connection
        data = client.recv(size)
        getURI = parse_request(data)
        print "Get URI %s" % getURI
        headers = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", data)

        if data: # if the connection was closed there would be no data
            print "received: %s, sending it back"%data
            client.send(response)
            client.close()
    except ValueError:
        response = client_error_response('Bad Request, we only take GETs from HTTP.')
        client.send(response)
        client.close()
