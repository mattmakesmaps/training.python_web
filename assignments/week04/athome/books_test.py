__author__ = 'matt'
"""
Testing methods in the books class, from books_test.py.
"""

if __name__ == '__main__':
    from bookdb import BookDB

    books = BookDB()

    print books.titles()
    print books.title_info('id1')
