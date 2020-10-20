"""
    TODO: make nsfw a switch that's off by default. If enabled, show nsfw posts in
    the overboard.
"""
from flask import Blueprint, request
from nmtchan import auth, utils
from nmtchan import db as database
import json, collections

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}

bp = Blueprint("api", __name__, url_prefix="/api/v1")

@bp.route("/posts", methods=['GET'])
@auth.require_login
def apiRecents():
    db = database.get_db()
    board = request.args.get("board", "all")
    limit = request.args.get("limit", "10")
    nsfw = request.args.get("nsfw", "1")

    posts = []
    if board == "all":
        nsfw = "0"
        query = "SELECT * FROM post WHERE parent=0 ORDER BY last_updated DESC LIMIT ?"
        posts = db.execute(query, (limit,)).fetchall()
    else:
        query = "SELECT * FROM post WHERE parent=0 AND board=? ORDER BY last_updated DESC LIMIT ?"
        posts = db.execute(query, (board,limit)).fetchall()

    posts = [dict(i) for i in posts]
    for post in posts:
        post["subject"] = utils.sanitize(post["subject"])
        post["body"] = utils.sanitize(post["body"])

    if nsfw != "1":
        query = "SELECT * FROM board WHERE category=?"
        boards = db.execute(query, ("nsfw",)).fetchall()
        boards = [dict(i)["link"][1:-1] for i in boards]
        posts = [i for i in posts if i["board"] not in boards]
    
    return {"status": "success", "data": json.dumps(posts)}

@bp.route("/post", methods=['GET'])
@auth.require_login
def getPost():
    db = database.get_db()
    post = request.args.get("id", "0")

    if post == "0":
        return {"status": "failure", "data": ""}

    # get op
    query = "SELECT * FROM post WHERE id=?"
    op = db.execute(query, (post,)).fetchone()
    op = dict(op)
    op["subject"] = utils.sanitize(op["subject"])
    op["body"] = utils.sanitize(op["body"])

    # get replies
    query = "SELECT * FROM post WHERE parent=?"
    replies = db.execute(query, (post,)).fetchall()
    replies = [dict(i) for i in replies]
    for r in replies:
        r["body"] = utils.sanitize(r["body"])

    data = {"op": op, "replies": replies}

    return {"status": "success", "data": json.dumps(data)}

@bp.route("/boards", methods=['GET'])
@auth.require_login
def getBoards():
    db = database.get_db()
    items = db.execute('SELECT * FROM board').fetchall()
    items = [dict(i) for i in items]

    boards = {}
    for i in items:
        if i["category"] in boards:
            boards[i["category"]].append(i)
        else:
            boards[i["category"]] = [i]

    sortedBoards = collections.OrderedDict(sorted(boards.items()))

    return {"status": "success", "data": json.dumps(sortedBoards)}