"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
# os environ get url
os.environ["DEFAULT_IMAGE_URL"] = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"
DEFAULT_IMAGE_URL = os.environ.get("DEFAULT_IMAGE_URL")

def connect_db(app):
    """Connect to database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )
