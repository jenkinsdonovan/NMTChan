from flask import g, redirect, session
from functools import wraps
from nmtchan import db as database

def require_login(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            db = database.get_db()
            u = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            g.user = u
        if g.user is None:
            return redirect("/login")
        return view(**kwargs)
    return wrapped_view

def require_admin(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            db = database.get_db()
            u = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            g.user = u
        if g.user is None:
            return redirect("/")
        if g.user["level"] != 1:
            return redirect("/")
        return view(**kwargs)
    return wrapped_view