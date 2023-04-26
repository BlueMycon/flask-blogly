"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///blogly"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.get("/")
def show_home_page():
    """Display Home Page"""

    return redirect("/users")


@app.get("/users")
def show_all_users():
    """Show All users"""

    users = User.query.all()

    return render_template("user_listing.html", users=users)


@app.get("/users/new")
def show_add_users_form():
    """Show and add form for users"""

    return render_template("new_user.html")


@app.post("/users/new")
def process_add_form():
    """Process the add form, adding a new user and going back to /users"""

    f_name = request.form["first-name"]
    l_name = request.form["last-name"]
    img_url = request.form["img-url"]

    new_user = User(first_name=f_name, last_name=l_name, image_url = img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""

    user = User.query.get(user_id)

    return render_template('user_detail.html', user = user)

    # Have a button to get to their edit page, and to delete the user.


@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """Show the edit page for a user."""

    user = User.query.get(user_id)

    return render_template('user_edit.html', user = user)
    # Have a cancel button that returns to the detail page for a user, and a save button that updates the user.


@app.post("/users/<int:user_id>/edit")
def process_edit_form(user_id):
    """Process the edit form, returning the user to the /users page."""

    f_name = request.form["first-name"]
    l_name = request.form["last-name"]
    img_url = request.form["img-url"]

    user = User.query.get(user_id)

    user.first_name = f_name
    user.last_name = l_name
    user.image_url = img_url

    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
