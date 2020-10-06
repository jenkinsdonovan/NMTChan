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
        post = db.execute('SELECT * FROM post WHERE id = ?', (post,)).fetchone()
        return render_template("post.html", boardname=board, post=post, replies=replies, form=form)

    if not form.validate_on_submit():
        flash("invalid form fields")
        return redirect(request.url)

    rules = form.rules.data
    body = form.body.data
    media = form.media.data
    replyTo = form.replyTo.data # currently unused
    parent = post
    created = datetime.now().timestamp()

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
    db.execute(query, (parent, board, "", body, thumbname, medianame, created, created))

    query = "UPDATE post SET last_updated = ? WHERE id = ?"
    db.execute(query, (created, parent))

    db.commit()


    return redirect(request.url)

    
