"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def show_home_page():
    """Display Home Page"""


@app.get("/users")
def show_all_users():
    """Show All users"""
#     Make these links to view the detail page for the user.

# Have a link here to the add-user form.



@app.get("/users/new")
def show_add_users_form():
    """Show an add form for users"""

@app.post("/users/new")
def process_add_form():
    """Process the add form, adding a new user and going back to /users"""

@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""
    # Have a button to get to their edit page, and to delete the user.

@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """Show the edit page for a user."""
    # Have a cancel button that returns to the detail page for a user, and a save button that updates the user.


@app.post("/users/<int:user_id>/edit")
def process_edit_form(user_id):
    """Process the edit form, returning the user to the /users page."""

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""
