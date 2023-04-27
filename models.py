"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(50),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime(timezone = True),
        nullable = False,
        default= datetime.datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    user = db.relationship("User", backref = "posts")



