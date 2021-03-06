import os
import flaskr
import unittest
import tempfile

class FlaskerTestCase(unittest.TestCase):
    """
    Testing class for Flaskr application. setUp and tearDown methods are executed for each test!
    That means that for every single test, a temp database is created and subsequently destroyed!
    """
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


    # WRITE METHOD FUNCTIONALITY
    def test_write_entry(self):
        """
        Test the write_entry() method of flaskr.
        """
        expected = ("My Title", "My Text")
        with self.app.test_request_context('/'):
            self.app.preprocess_request()
            # Insert our test data into the test database.
            flaskr.write_entry(*expected)
            con = flaskr.connect_db()
            # Check for presence of test data.
            cur = con.execute("select * from entries;")
            rows = cur.fetchall()
        self.assertEquals(len(rows), 1)
        for val in expected:
            # Actually check the values against expected.
            self.assertTrue(val in rows[0])


    # READ METHOD FUNCTIONALITY
    def test_get_all_entries_empty(self):
        with self.app.test_request_context('/'):
            self.app.preprocess_request()
            entries = flaskr.get_all_entries()
            self.assertEquals(len(entries), 0)

    def test_get_all_entries(self):
        expected = ("My Title", "My Text")
        with self.app.test_request_context('/'):
            self.app.preprocess_request()
            flaskr.write_entry(*expected)
            entries = flaskr.get_all_entries()
            self.assertEquals(len(entries), 1)
            for entry in entries:
                self.assertEquals(expected[0], entry['title'])
                self.assertEquals(expected[1], entry['text'])

    # Template Tests
    # As opposed to read tests above, now we're actually testing the response values
    # recieved by the client.
    def test_empty_listing(self):
        rv = self.client.get('/')
        assert 'No entries here so far' in rv.data

    def test_listing(self):
        expected = ("My Title", "My Text")
        with self.app.test_request_context('/'):
            self.app.preprocess_request()
            flaskr.write_entry(*expected)
        rv = self.client.get('/')
        for value in expected:
            assert value in rv.data


    # Authentication Tests
    def test_login_passes(self):
        with self.app.test_request_context('/'):
            self.app.preprocess_request()
            flaskr.do_login(flaskr.app.config['USERNAME'],
                            flaskr.app.config['PASSWORD'])
            # Need to explicitly direct to flaskr session.
            self.assertTrue(flaskr.session.get('logged_in', False))

    def test_login_fails(self):
        with self.app.test_request_context('/'):
            self.app.preprocess_request()
            self.assertRaises(ValueError, flaskr.do_login,
                              flaskr.app.config['USERNAME'],
                              'incorrectpassword')

    # Login/Logout
    # These methods are required to fake a login during the test_login_logout execution.
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout',
                               follow_redirects=True)

    def test_login_logout(self):
        """
        Test different types of login possibilities.
        e.g. Valid, logged out, wrong user, wrong pass.
        """
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid Login' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid Login' in rv.data

    def test_add_entries(self):
        self.login('admin', 'default')
        rv = self.client.post('/add', data=dict(
            title='Hello',
            text='This is a post'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert 'Hello' in rv.data
        assert 'This is a post' in rv.data

if __name__ == '__main__':
    unittest.main()