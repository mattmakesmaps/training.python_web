import os
import flaskr
import unittest
import tempfile

class FlaskerTestCase(unittest.TestCase):

    def setUp(self):
        db_fd = tempfile.mkstemp()
        self.db_fd, flaskr.app.config['DATABASE'] = db_fd
        flaskr.app.config['TESTING'] = True
        self.client = flaskr.app.test_client()
        self.app = flaskr.app
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_database_setup(self):
        """
        Testing that table info returns three rows,
        as the SQL statement should return one row for each
        table column.
        """
        con = flaskr.connect_db()
        cur = con.execute('PRAGMA table_info(entries);')
        rows = cur.fetchall()
        self.assertEquals(len(rows), 3)

if __name__ == '__main__':
    unittest.main()