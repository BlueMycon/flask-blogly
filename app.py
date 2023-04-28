"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Post, Tag, PostTag

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

    flash("Redirected to Users List.")
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

    flash(f"New user '{new_user.full_name}' joined.")
    return redirect(f"/users/{new_user.id}")


@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    # posts = user.posts
    posts = user.posts

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

    flash(f"User '{user.full_name}' edited.")
    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts

    for post in posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()

    flash(f"User '{user.full_name}' successfully deleted.")
    return redirect("/users")

# Post routes

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)

@app.post('/users/<int:user_id>/posts/new')
def create_new_post(user_id):
    """Add post and redirect to the user detail page."""

    title = request.form["title"]
    content = request.form["content"]
    tags_checked = request.form.getlist("tags-checked")

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added to your posts!")

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


    flash(f"Post '{post.title}' was edited.")

    return redirect(f"/posts/{post_id}")

@app.post('/posts/<int:post_id>/delete')
def handle_post_delete(post_id):
    """Delete the post"""


    post = Post.query.get_or_404(post_id)
    post.tags = []

    # user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' successfully deleted.")

    return redirect(f"/users/{post.user_id}")

@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404

# Tag Routes

@app.get("/tags")
def list_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()

    return render_template("tag_listing.html", tags=tags)

@app.get("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_detail.html", tag=tag)

@app.get("/tags/new")
def show_new_tag_form():
    """Shows a form to add a new tag."""

    return render_template("new_tag.html")

@app.post("/tags/new")
def create_new_tag():
    """Process add form, adds tag, and redirect to tag list."""
    name = request.form.get("name")

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag '{new_tag.name}' was created.")

    return redirect("/tags")

@app.get("/tags/<int:tag_id>/edit")
def get_tag_edit_form(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_edit.html", tag=tag)

@app.post("/tags/<int:tag_id>/edit")
def update_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    name = request.form.get("name")

    tag = Tag.query.get_or_404(tag_id)
    tag.name = name
    db.session.commit()

    flash(f"Tag '{tag.name}' was edited.")

    return redirect("/tags")

@app.post("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)
    post_tags = PostTag.query.filter_by(tag_id=tag_id).all()

    for post_tag in post_tags:
        db.session.delete(post_tag)

    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}'  was deleted.")

    return redirect("/tags")
