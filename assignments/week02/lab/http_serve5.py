#!/usr/bin/env python
"""
Lab Time - Step 5
-----------------

Serve different types of files:

* Save the file as ``http_serve5.py``

* Update the ``resolve_uri`` method. If the URI names a file, return it as the
  body of a ``200 OK`` response.

* You'll need a way to return the approprate ``Content-Type:`` header.

* Support at least ``.html``, ``.txt``, ``.jpeg``, and ``.png`` files

* Try it out.

.. class:: incremental

You've now got a reasonably functional HTTP web server.  Congratulations!
"""

import socket, re, os

def ok_response(body, content_type='text/plain'):
    """Return a formatted HTTP Response."""
    header = 'HTTP/1.0 200 OK\r\nContent-Type: %s\r\n\r\n' % content_type
    file = open(body,'r').read()
    response = header + file
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
        return header
    elif os.path.isfile(joined_path):
        print 'this is a file'
        ext = os.path.splitext(joined_path)
        # need a dict of extensions as keys, content type string as values.
        content_type_listing = {'.html':'text/html', '.txt':'text/plain'}
        if ext[1] in content_type_listing.iterkeys():
            content_type = content_type_listing[ext[1]]
            response = ok_response(joined_path,content_type)
            return response
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