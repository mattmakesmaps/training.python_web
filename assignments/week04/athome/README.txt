README
======

# Overview

Assignment URL: http://block647055-hm6.blueboxgrid.com/book_wsgi_server

# Comments

* I decided to create a separate WSGI script alias for this assignment, to try
  and give it a cleaner looking URL.
* I'm betting that there is a better way to handle things then using a URL
  query string.

# Deploy Notes

* Restart Apache: $ sudo /etc/init.d/apache2 restart
* Apache Conf For WSGIScriptAlias: $ sudo vim /etc/apache2/sites-available/default
* WSGI-Bin Directory: /usr/lib/wsgi-bin/
