from flask import Flask, redirect, render_template
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
