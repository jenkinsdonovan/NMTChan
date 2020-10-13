from flask import Blueprint, render_template, g
from nmtchan import auth
from nmtchan import db as database

bp = Blueprint("index", __name__)
@bp.route("/")
@auth.require_login
def handleIndex():
    db = database.get_db()
    items = db.execute('SELECT * FROM board').fetchall()
    items = [dict(i) for i in items]

    categories = set([i["category"] for i in items])
    categories = sorted(categories) 

    boards = {}
    for category in categories:
        boards[category] = [i for i in items if i["category"] == category]

    sfws = db.execute("SELECT link FROM board WHERE category!='nsfw'").fetchall()
    sfws = [dict(i)["link"][1:-1] for i in sfws]

    query = "SELECT * FROM post WHERE parent=0 AND board IN (%s) LIMIT 10" % ','.join('?'*len(sfws))
    items = db.execute(query, sfws).fetchall()
    
    posts = [dict(i) for i in items]
    posts = sorted(posts, key = lambda i: i['last_updated'], reverse=True) 

    return render_template("index.html", boardlist=boards, posts=posts, level=g.user["level"])

@bp.route("/rules/")
def handleRules():
    return render_template("rules.html")