"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
dt = datetime.datetime.now()

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()


class User(db.Model):
    """User info."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.image_url == None}>"

    @property
    def full_name(self):
        """Returns the full name of the user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post info."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.replace(second=0, microsecond=0))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # create relationship between models & through relationship
    user = db.relationship("User", backref="posts")
    tags = db.relationship('Tag', secondary="post_tags", backref="posts")

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at} {self.user_id}>"

    
class Tag(db.model):
    """Tag model to tag posts."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    

class PostTag(db.model):
    """Mapping of a post to a tag."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
