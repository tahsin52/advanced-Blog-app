from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from src import db
from src.models import User

auth = Blueprint("auth", __name__)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Legged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exists', category='error')

    return render_template('login.html')

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password1")
        confirm_password = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password != confirm_password:
            flash('Password dont match', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password) < 6:
            flash('Password is too short', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created', category='success')

            return redirect(url_for('views.home'))

    return render_template('signup.html')

@auth.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for('views.home'))