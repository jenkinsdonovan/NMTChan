from flask import Blueprint, render_template, request, redirect, flash
from nmtchan import auth, utils
from nmtchan import db as database

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired

from datetime import datetime

class ThreadForm(FlaskForm):
    rules = BooleanField('I have read the rules', validators=[DataRequired()])
    subject = StringField('Subject', validators=[])
    body = StringField('Body', validators=[])
    media = FileField('Media', validators=[DataRequired()])

bp = Blueprint("board", __name__)
@bp.route("/<board>/", methods=['GET', 'POST'])
@auth.require_login
def handleBoard(board):
    form = ThreadForm()

    if request.method == "GET":
        form.media(accept='image/*,.webm')
        db = database.get_db()
        items = db.execute('SELECT * FROM post WHERE board = ? AND parent = 0', (board,)).fetchall()
        posts = [dict(i) for i in items]
        posts = sorted(posts, key = lambda i: i['last_updated'], reverse=True) 
        return render_template("board.html", boardname=board, posts=posts, form=form)

    if not form.validate_on_submit():
        flash("invalid form fields")
        return redirect(request.url)

    if not form.rules.data:
        return redirect(request.url)

    subject = form.subject.data
    body = form.body.data
    media = form.media.data
    created = datetime.now().timestamp()

    thumbname, medianame = None, None
    try:
        thumbname, medianame = utils.uploadFile(media, request)
    except Exception as e:
        flash(str(e))
        return redirect(request.url)

    db = database.get_db()
    query = "INSERT INTO post (parent, board, subject, body, thumb, media, last_updated, created) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    db.execute(query, (0, board, subject, body, thumbname, medianame, created, created))
    db.commit()

    i = db.execute("SELECT * FROM post WHERE thumb=? AND created=?", (thumbname, created)).fetchone()

    return redirect(request.url + str(i["id"]))