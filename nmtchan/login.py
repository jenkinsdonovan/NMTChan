from flask import Blueprint, render_template, flash, redirect, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db as database

# form shit that protects against CSRF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

bp = Blueprint("login", __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    access = StringField('Confirm', validators=[DataRequired()])
    rules = BooleanField('I have read the rules', validators=[DataRequired()])
    submit = SubmitField('Register')

@bp.route("/login", methods=['GET', 'POST'])
def handleLogin():
    form = LoginForm()

    if request.method == "GET":
        return render_template("login.html", form=form)

    if not form.validate_on_submit():
        flash("invalid form fields")
        return redirect("/login")

    db = database.get_db()
    username = form.username.data
    password = form.password.data

    query = "SELECT * FROM user WHERE username = ?"
    user = db.execute(query, (username,)).fetchone()
    if user and check_password_hash(user["password"], password):
        session.clear()
        session['user_id'] = user["id"]
        return redirect("/")

    flash("incorrect username or password")
    return render_template("login.html", form=form)

@bp.route("/signup", methods=['GET', 'POST'])
def handleSignup():
    form = SignupForm()
    
    if request.method == "GET":
        return render_template("signup.html", form=form)
    
    if not form.validate_on_submit():
        flash("invalid form fields")
        return redirect("/signup")

    db = database.get_db()
    username = form.username.data
    password = form.password.data
    confirm = form.confirm.data
    access = form.access.data

    if not form.rules.data:
        flash("please read the rules")
        return redirect("/signup")

    if db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone():
        flash("username exists")
        return redirect("/signup")

    codes = db.execute("SELECT accessCode from code")
    codes = [dict(c)["accessCode"] for c in codes]
    if access not in codes:
        return redirect("/signup")
    db.execute("DELETE FROM code WHERE accessCode=?", (access,))

    query = "INSERT INTO user (username, password, level) VALUES (?, ?, ?)"
    db.execute(query, (username, generate_password_hash(password), 3))
    db.commit()

    # log the user in 
    query = "SELECT * FROM user WHERE username = ?"
    user = db.execute(query, (username,)).fetchone()
    if user and check_password_hash(user["password"], password):
        session.clear()
        session['user_id'] = user["id"]
        return redirect("/")
    
    flash("error in signup")
    return redirect("/signup")

@bp.route("/logout")
def handleLogout():
    session.clear()
    return redirect("/login")