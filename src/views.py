from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user

from src import db
from src.models import Post

views = Blueprint("views", __name__)

@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html',
                           name=current_user,
                           posts=posts)

@views.route("/create-post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()

            flash('Post Created', category='success')
            return redirect(url_for('views.home'))