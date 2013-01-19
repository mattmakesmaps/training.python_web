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
from email.utils import formatdate
from os import path, listdir
import socket, re

def make_response(body, status_code='200 OK', content_type='text/plain'):
    """Return a formatted HTTP Response."""
    header = 'HTTP/1.0 %s\r\nContent-Type: %s\r\n' % (status_code, content_type)
    # Add Date Header
    header += 'Date: %s\r\n\r\n' % formatdate()
    response = header + body
    return response

def resolve_uri(inuri):
    """Given a URI, return an HTTP Response."""
    # strip leading forward slash from path.
    if inuri[0] == '/':
        inuri = inuri[1:]
    # associate request with web folder.
    joined_path = path.join('./web',inuri)
    # Check for path
    if path.isdir(joined_path):
        print 'this is a directory'
        # Get Contents of Directory
        dir_contents = listdir(joined_path)
        # Create a string representing links for all files/dirs
        resource_links = ''
        for resource in dir_contents:
            resource_links += '<a href=./%s>%s</a><br/>'%(path.join(inuri, resource), resource)
        # Return header and response
        response = make_response(resource_links,'200 OK','text/html')
        return response
    elif path.isfile(joined_path):
        print 'this is a file'
        # Get file extension
        ext = path.splitext(joined_path)
        # need a dict of extensions as keys, content type string as values.
        content_type_listing = {'.html':'text/html', '.txt':'text/plain',
                                '.png':'image/png', '.jpg':'image/jpeg',
                                '.jpeg': 'image/jpeg'}
        # Pass appropriate content/type value and file to make_response
        if ext[1] in content_type_listing.iterkeys():
            content_type = content_type_listing[ext[1]]
            file = open(joined_path, 'r').read()
            response = make_response(file,'200 OK', content_type)
            return response
    else:
        response = make_response('ERROR: File Not Found','404 Not Found')
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
        response_body = 'ERROR: Bad Request. Please send an HTTP GET Request.'
        response = make_response(response_body,'400 Bad Request')
        return response

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

while True: # keep looking for new connections forever
    try:
        client, address = s.accept() # look for a connection
        data = client.recv(size)
        # Parse data
        getURI = parse_request(data)
        resolved_response = resolve_uri(getURI)
        print "Get URI %s" % getURI
        # Create a list of headers as tuples. Got this from SO.
        # Might be useful to know user-agent value. e.g. mobile formatted?
#        headers = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", data)

        if data: # if the connection was closed there would be no data
            print "received: %s, sending it back"%data
            client.send(resolved_response)
            client.close()
    except Exception:
        # Not too sure what to do here
        # Need some generic error handling code, maybe a 5XX error?
        pass
