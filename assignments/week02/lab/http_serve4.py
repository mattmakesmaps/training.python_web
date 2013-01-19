#!/usr/bin/env python
"""
Lab Time - Step 4
-----------------

Serve directory listings:

* Save the file as ``http_serve4.py`` * Add a method called ``resolve_uri``
  which takes as an argument the URI returned from our previous step and
  returns an HTTP response. The method should start from a given directory
  ('web') and check the URI:

    * If the URI names a directory, return the content listing as a ``200 OK``

    * If the URI names a file, raise a NotImplementedError (coming soon)

    * If the URI does not exist, raise a ValueError

* Bonus points: add a ``notfound_response`` method that returns a proper ``404
  Not Found`` response to the client. Use it when appropriate. (where is
  that?)
"""

import socket, re, os

def ok_response(body):
    """Return a formatted HTTP Response."""
    header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n'
    response = header + body
    return response

def resolve_uri(inuri):
    """Given a URI, return an HTTP Response."""
    # strip leading forward slash from path.
    if inuri[0] == '/':
        inuri = inuri[1:]
    # associate request with web folder.
    joined_path = os.path.join('./web',inuri)
    # Check for path
    if os.path.isdir(joined_path):
        print 'this is a directory'
        header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n'
    elif os.path.isfile(joined_path):
        print 'this is a file'
        raise NotImplementedError
    else:
        header = 'HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
        print 'not found error'
    return header


def client_error_response(body):
    """Return a formatted HTTP Response."""
    header = 'HTTP/1.0 400 BAD REQUEST\r\nContent-Type: text/html\r\n\r\n'
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

#response = ok_response(html)

while True: # keep looking for new connections forever
    try:
        client, address = s.accept() # look for a connection
        data = client.recv(size)
        # Parse data
        getURI = parse_request(data)
        resolved_response_header = resolve_uri(getURI)
        print "Get URI %s" % getURI
        # Create a list of headers as tuples. Got this from SO.
        headers = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", data)

        if data: # if the connection was closed there would be no data
            print "received: %s, sending it back"%data
            client.send(resolved_response_header)
            client.close()
    except ValueError:
        client_error_response('Bad Request, we only take GETs from HTTP.')