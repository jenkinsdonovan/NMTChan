from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
import sqlite3, os

def get_db():
    if 'db' not in g:
        sqlitepath = current_app.config['DATABASE']
        g.db = sqlite3.connect(sqlitepath, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(d=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    # create folders
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["MEDIA_FOLDER"], exist_ok=True)

    # connect to db
    with app.app_context():
        get_db()

        # create tables
        with app.open_resource('schema.sql') as f:
            g.db.executescript(f.read().decode('utf8'))

        # create admin user
        g.db.execute("DELETE FROM user WHERE level=1")
        username = app.config["admin"]["username"]
        password = generate_password_hash(app.config["admin"]["password"])
        user = g.db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user is None:
            query = 'INSERT INTO user (username, password, level) VALUES (?, ?, ?)'
            level = 1
            g.db.execute(query, (username, password, level))
            g.db.commit()

    app.teardown_appcontext(close_db)