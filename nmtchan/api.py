from flask import Blueprint, request
from nmtchan import auth
from nmtchan import db as database
import json

bp = Blueprint("api", __name__, url_prefix="/api/v1")

@bp.route("/posts", methods=['GET'])
#@auth.require_login
def apiPosts():
    db = database.get_db()
    board = request.args.get("board", "all")
    limit = request.args.get("limit", "10")

    posts = []
    if board == "all":
        query = "SELECT * FROM post WHERE parent=0 ORDER BY last_updated ASC LIMIT ?"
        posts = db.execute(query, (limit,)).fetchall()
    else:
        query = "SELECT * FROM post WHERE parent=0 AND board=? ORDER BY last_updated ASC LIMIT ?"
        posts = db.execute(query, (board,limit)).fetchall()
    posts = [dict(i) for i in posts]
    
    return {"status": "success", "data": json.dumps(posts)}