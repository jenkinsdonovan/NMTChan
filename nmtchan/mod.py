from flask import Blueprint, render_template, request, redirect, flash
from nmtchan import auth, utils
from nmtchan import db as database
import secrets, string

bp = Blueprint("mod", __name__, url_prefix="/mod")
@bp.route("/", methods=['GET', 'POST'])
@auth.require_login
@auth.require_admin
def handleMod():
    db = database.get_db()
    codes = db.execute("SELECT * FROM code")
    codes = [dict(i) for i in codes]
    accounts = db.execute("SELECT * FROM user")
    accounts = [dict(i) for i in accounts]
    return render_template("mod.html", codes=codes, accounts=accounts)

@bp.route("/newCode/", methods=['GET', 'POST'])
@auth.require_login
@auth.require_admin
def handleNewCode():
    db = database.get_db()
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(10))
    query = "INSERT INTO code (accessCode) VALUES (?)"
    db.execute(query, (code,))
    db.commit()
    return redirect("/mod/")