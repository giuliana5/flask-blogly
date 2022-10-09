from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

    users = User.query.order_by(User.last_name, User.first_name).all()

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

    return render_template("details.html", user=user)
