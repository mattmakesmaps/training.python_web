import sqlite3
from flask import Flask, g
from contextlib import closing


# configuration goes here
DATABASE = '/tmp/flaskr.db'
SECRET_KEY = 'development_key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """
    Convenience function to connect to our database, based on config value.

    :return:
    """
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request  # any method decorated by this will be called before the cycle begins
def before_request():
    g.db = connect_db()

# any method decorated by this will be called at the end of the cycle, even if an unhandled exception occurs.
@app.teardown_request
def teardown_request(exception):
    g.db.close()

def write_entry(title, text):
    """
    Insert into our entries table values for title and text.
    NOTE, using the '?' is the only safe way to populate a string SQL
    statement with values.
    """
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [title, text])
    g.db.commit()

if __name__ == '__main__':
    app.run(debug=True)
