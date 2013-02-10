import sqlite3
from flask import Flask, g, render_template, session, flash, request, redirect, url_for, abort
from contextlib import closing


# configuration goes here
DATABASE = '/tmp/flaskr.db'
SECRET_KEY = 'development_key'
# admin auth stuff
USERNAME = 'admin'
PASSWORD = 'default'

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

def get_all_entries():
    """
    Execute a SQL statement retrieve values from our single table.
    Returns a list of dictionaries with titles as keys and text as values.
    """
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return entries

@app.route('/')  # This is the first function with an app route decorator. Pointed to '/'
def show_entries():
    """
    Grab all entries from the database and render to a template.
    This feels most similar to a typical django view function.
    """
    entries = get_all_entries()
    return render_template('show_entries.html', entries=entries)

def do_login(usr, pwd):
    """
    Check input values against the hard-coded config vals representing user/pass.
    """
    if usr != app.config['USERNAME']:
        raise ValueError
    elif pwd != app.config['PASSWORD']:
        raise ValueError
    else:
        session['logged_in'] = True

# Login Logout Functionality.
# Note still using do_login() to check against config values for user/pass.
# TODO: Review flash method.
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            do_login(request.form['username'],
                     request.form['password'])
        except ValueError:
            error = "Invalid Login"
        else:
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    try:
        write_entry(request.form['title'], request.form['text'])
        flash('New entry was successfully posted')
    except sqlite3.Error as e:
        flash('There was an error: %s' % e.args[0])
    return redirect(url_for('show_entries'))
if __name__ == '__main__':
    app.run(debug=True)
