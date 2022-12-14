from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home():
    """Redirect to users page."""

    return redirect("/users")

@app.route("/users")
def users():
    """Display list of users."""

    users = User.query.order_by(User.first_name, User.last_name).all()

    return render_template("users.html", users=users)

@app.route("/users/new")
def new_user_form():
    """Display the form to create a new user."""

    return render_template("new-user.html")

@app.route("/users/new", methods=["POST"])
def create_user():
    """Add User to db with info from form."""

    new_user = User(
        first_name=request.form["first-name"],
        last_name=request.form["last-name"],
        image_url=request.form["image-url"] or None
        )
    
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    """View the user's details."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)

    return render_template("details.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Show form to edit user info."""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Update user info."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user from db."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id).all()

    for post in posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show form to create a new post."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template("new-post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """Add a new post to db."""

    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user_id=user_id
    )

    tags = request.form.getlist("tags")

    for tag in tags:
        t = Tag.query.get(int(tag))
        new_post.tags.append(t)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_details(post_id):
    """Display post."""

    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Display form to edit post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template("edit-post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Change the post to match new form content."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(id) for id in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.tag_id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/tags")
def tag_list():
    """Displays the list of tags."""

    tags = Tag.query.order_by(Tag.name).all()

    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Retreives tag details."""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("tag-details.html", tag=tag, posts=posts)

@app.route("/tags/new")
def new_tag_form():
    """Shows the form to create a new tag."""

    return render_template("new-tag.html")

@app.route("/tags/new", methods=["POST"])
def new_tag():
    """Create new tag."""

    tag = Tag(
        name=request.form["name"]
    )

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Displays form to edit an existing tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit-tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edit tag info."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Deletes tag from db."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
