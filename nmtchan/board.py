from flask import Blueprint, render_template, request, redirect, flash
from nmtchan import auth, utils
from nmtchan import db as database

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from datetime import datetime

class ThreadForm(FlaskForm):
    rules = BooleanField('I have read the rules', validators=[DataRequired()])
    subject = StringField('Subject', validators=[])
    body = StringField('Body', validators=[], widget=TextArea())
    media = FileField('Media', validators=[DataRequired()])

bp = Blueprint("board", __name__)
@bp.route("/<board>/", methods=['GET', 'POST'])
@auth.require_login
def handleBoard(board):
    form = ThreadForm()

    if request.method == "GET":
        form.media(accept='image/*,.webm')
        return render_template("board.html", boardname=board, form=form)

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
    i = db.execute(query, (0, board, subject, body, thumbname, medianame, created, created))
    db.commit()

    query = "SELECT * FROM post WHERE board=? AND parent=0 ORDER BY last_updated ASC"
    rows = db.execute(query, (board,)).fetchall()
    rows = [dict(i) for i in rows]
    while len(rows) > 20:
        p = rows.pop(0)
        query = "DELETE FROM post WHERE id=?"
        db.execute(query, (p["id"],))
        db.commit()

    for row in rows:
        row["body"] = utils.sanitize(row["body"])
        

    return redirect(request.url + str(i.lastrowid))