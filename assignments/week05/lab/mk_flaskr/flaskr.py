import sqlite3
from flask import Flask
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

if __name__ == '__main__':
    app.run(debug=True)
