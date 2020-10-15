"""
TODO: Make "parent" SQL field a string, containing comma separated
    parents to the comment, allowing one comment to be a reply to 
    many. Or, add a table holding holding post relationships. I.e, 
    column 1 is post ID, column 2 is parent ID.
"""

from flask import Blueprint, render_template, request, redirect, flash
from nmtchan import auth, utils
from nmtchan import db as database

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, HiddenField
from wtforms.validators import DataRequired

from datetime import datetime

class ThreadForm(FlaskForm):
    rules = BooleanField('I have read the rules', validators=[DataRequired()])
    body = StringField('Body', validators=[])
    media = FileField('Media', validators=[])
    replyTo = HiddenField()

def getComments(post, posts):
    db = database.get_db()
    
    posts = posts + items
    for i in items[1:]:
        posts = posts + getComments(i, posts)
    return posts

bp = Blueprint("post", __name__)
@bp.route("/<board>/<post>/", methods=['GET', 'POST'])
@auth.require_login
def handlePost(board, post):
    form = ThreadForm()

    if request.method == "GET":
        form.media(accept='image/*,.webm')
        db = database.get_db()

        replies = db.execute('SELECT * FROM post WHERE parent = ?', (post,)).fetchall()
        replies = [dict(i) for i in replies]

        for reply in replies:
            print(reply["id"])
            childrenIDs = db.execute('SELECT * FROM reply WHERE opID = ?', (reply["id"],)).fetchall()
            childrenIDs = [dict(i) for i in childrenIDs]
            print(childrenIDs)

        post = db.execute('SELECT * FROM post WHERE id = ?', (post,)).fetchone()
        return render_template("post.html", boardname=board, post=post, replies=replies, form=form)

    if not form.validate_on_submit():
        flash("invalid form fields")
        return redirect(request.url)

    rules = form.rules.data
    body = form.body.data
    media = form.media.data
    replyTo = int(form.replyTo.data)
    parent = post
    created = datetime.now().timestamp()
    print("REPLYTO:", replyTo)

    if not rules:
        flash("rules required")
        return redirect(request.url)

    thumbname, medianame = None, None
    try:
        thumbname, medianame = utils.uploadFile(media, request)
    except Exception as e:
        if not body:
            flash("content is required")
            return redirect(request.url)

    db = database.get_db()
    query = "INSERT INTO post (parent, board, subject, body, thumb, media, last_updated, created) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    t = db.execute(query, (parent, board, "", body, thumbname, medianame, created, created))

    query = "UPDATE post SET last_updated = ? WHERE id = ?"
    db.execute(query, (created, parent))

    query = "INSERT INTO reply (opID, replyID) VALUES (?, ?)"
    db.execute(query, (replyTo, t.lastrowid))
    db.commit()

    return redirect(request.url)