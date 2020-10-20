from flask import Blueprint, render_template, g
from nmtchan import auth
from nmtchan import db as database

bp = Blueprint("index", __name__)
@bp.route("/")
@auth.require_login
def handleIndex():
    return render_template("index.html", level=g.user["level"])

@bp.route("/rules/")
def handleRules():
    return render_template("rules.html")