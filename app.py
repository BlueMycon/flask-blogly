"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///blogly"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "a-very-big-secret"

connect_db(app)


@app.get("/")
def show_home_page():
    """Display Home Page"""

    flash("Redirected to Users")
    return redirect("/users")


@app.get("/users")
def show_all_users():
    """Show All users"""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("user_listing.html", users=users)


@app.get("/users/new")
def show_add_users_form():
    """Show and add form for users"""

    return render_template("new_user.html")


@app.post("/users/new")
def process_add_form():
    """Process the add form, adding a new user and going back to /users"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form.get("img-url") or None

    new_user = User(first_name=first_name, last_name=last_name, image_url = img_url)
    db.session.add(new_user)
    db.session.commit()

    flash("Redirected to Profile")
    return redirect(f"/users/{new_user.id}")


@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    # posts = user.posts
    posts = Post.query.filter(user_id == user_id).all()

    return render_template('user_detail.html', user = user, posts = posts)



@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user = user)


@app.post("/users/<int:user_id>/edit")
def process_edit_form(user_id):
    """Process the edit form, returning the user to the /users page."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"] if request.form["img-url"] else None

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url

    db.session.commit()

    flash("Redirected to Users")
    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash("Redirected to Users")
    return redirect("/users")

# Post routes

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)

@app.post('/users/<int:user_id>/posts/new')
def create_new_post(user_id):
    """Add post and redirect to the user detail page."""

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.get('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Show a post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_detail.html", post=post)

@app.get('/posts/<int:post_id>/edit')
def show_post_edit(post_id):
    """Show form to edit a post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_edit.html", post=post)


@app.post('/posts/<int:post_id>/edit')
def handle_post_edit(post_id):
    """Handle editing of a post"""

    title = request.form["title"]
    content = request.form["content"]


    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.post('/posts/<int:post_id>/delete')
def handle_post_delete(post_id):
    """Delete the post"""


    post = Post.query.get_or_404(post_id)

    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404