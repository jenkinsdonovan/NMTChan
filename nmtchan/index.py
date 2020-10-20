from flask import Blueprint, render_template, g
from nmtchan import auth
from nmtchan import db as database
import git, time

bp = Blueprint("index", __name__)
@bp.route("/")
@auth.require_login
def handleIndex():
    repo = git.Repo(".")
    commit = ""
    if repo is not None:
        commit = repo.head.commit
    return render_template("index.html", level=g.user["level"], commit=commit)

@bp.route("/rules/")
def handleRules():
    return render_template("rules.html")