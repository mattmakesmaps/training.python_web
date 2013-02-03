#!/usr/bin/python

"""
Using what you've learned this week, Attempt the following:

* Create a small, multi-page WSGI application
* Use ``assignments/week04/athome/bookdb.py`` as a data source
* Your app index page should list the books in the db
* Each listing should supply a link to a detail page
* Each detail page should list information about the book

HINT:

Use the Armin Ronacher reading from the class outline as a source for hints:
http://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/

Submitting Your Work:

This week we are going to do something a bit different. Get your application
running on your VM. Then add the following to ``assignments/week04/athome``
and submit a pull request:

* A README.txt file containing the URL I can visit to see your application.
  You can also put questions or comments in this file.

* Your source code, whatever is up on your VM.
"""

class BookDB():
    def titles(self):
        titles = [dict(id=id, title=database[id]['title']) for id in database.keys()]
        return titles

    def title_info(self, id):
        return database[id]


# let's pretend we're getting this information from a database somewhere
database = {
    'id1' : {'title' : 'CherryPy Essentials: Rapid Python Web Application Development',
             'isbn' : '978-1904811848',
             'publisher' : 'Packt Publishing (March 31, 2007)',
             'author' : 'Sylvain Hellegouarch',
             },
    'id2' : {'title' : 'Python for Software Design: How to Think Like a Computer Scientist',
             'isbn' : '978-0521725965',
             'publisher' : 'Cambridge University Press; 1 edition (March 16, 2009)',
             'author' : 'Allen B. Downey',
             },
    'id3' : {'title' : 'Foundations of Python Network Programming',
             'isbn' : '978-1430230038',
             'publisher' : 'Apress; 2 edition (December 21, 2010)',
             'author' : 'John Goerzen',
             },
    'id4' : {'title' : 'Python Cookbook, Second Edition',
             'isbn' : '978-0-596-00797-3',
             'publisher' : 'O''Reilly Media',
             'author' : 'Alex Martelli, Anna Ravenscroft, David Ascher',
             },
    'id5' : {'title' : 'The Pragmatic Programmer: From Journeyman to Master',
             'isbn' : '978-0201616224',
             'publisher' : 'Addison-Wesley Professional (October 30, 1999)',
             'author' : 'Andrew Hunt, David Thomas',
             },
    }

from urlparse import parse_qs

def makeTitlesHTML(content, html_header, html_footer):
    """
    Return an HTML Page Listing Book Titles.

    The general pattern is to use populate different blocks of html
    into a list, then convert that list into a string.

    The string is then returned back to the calling application for
    use as a response.
    """
    titles = content.titles()

    html_list = [html_header]
    for element in titles:
        url = '<a href="%s">%s' % ('book_wsgi_server?id=' + element['id'], element['title'])
        html_list.append('<li>' + url + '</li>')
    html_list.append(html_footer)

    return html_list_to_string(html_list)

def makeDetailHTML(queryResults, id, html_header, html_footer):
    """Given an ID, return an HTML Response Detail Page."""
    try:
        selected_title_info = queryResults.title_info(id)
    except:
        raise ValueError('ID Given Does Not Exist.')

    html_list = [html_header]
    html_list.append('<h4>%s</h4>' % selected_title_info['title'])
    for key, value in selected_title_info.iteritems():
        html_list.append('<li><b>%s:</b> %s</li>'% (key, value))

    home_link = '</br><a href="%s">Back to Title Index</a>' % 'book_wsgi_server?'

    html_list.append(home_link)
    html_list.append(html_footer)

    return html_list_to_string(html_list)


def html_list_to_string(html_list):
    """
    Convert a list of html blocks into a string
    for output as wsgi response.
    """
    html_string = ''
    for html_block in html_list:
        html_string+=html_block

    return html_string

def application(environ, start_response):
    """
    Need to look at query string. If an id parameter is passed,
    return that book's detail page or a not-found error.
    If no id parameter is passed, return the index page.
    """
    html_header = """<html>
    <head>
    <title>Homework Week Four - WSGI Server</title>
    </head>
    <body>
    """

    html_footer = """
    </body>
    </html>"""
    try:
        # Query the database
        queryResults = BookDB()

        # Look for an id key.
        parseDict = parse_qs(environ['QUERY_STRING'])
        titleID = parseDict.get('id',None)

        if titleID is None:
            """No ID given"""
            response_body = makeTitlesHTML(queryResults, html_header, html_footer)
        else:
            """We have proper title, pass to detail func"""
            id = titleID[0]
            response_body = makeDetailHTML(queryResults, id, html_header, html_footer)

        status = '200 OK'
        content_length = str(len(response_body))

    except Exception, e:
        error_text = 'ERROR Encountered: %s' % str(e)
        content_length = str(len(str(error_text)))
        response_body = error_text
        status = '404 NOT FOUND'

    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', content_length)]
    start_response(status, response_headers)
    return [response_body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8090, application)
    srv.serve_forever()
