"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User info."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    @property
    def full_name(self):
        """Returns the full name of the user."""

        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)
    