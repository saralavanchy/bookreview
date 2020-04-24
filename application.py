import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from User import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/signin", methods=["POST"])
def signin():
    """Signin the webpage."""
    # Get form information.
    name = request.form.get("name")
    surname = request.form.get("surname")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    try:
        if db.execute("SELECT * FROM users WHERE USERNAME = :username",{"username" : username}).rowcount > 0:
            return render_template("error.html", message="your username is already in use, or you already have an account in our page")

        newuser = User(name=name, surname=surname, username=username, email=email,  password=password)
        print(newuser.name)
        newuser.create()
        return render_template("success.html", message="Your library registration has been generated successfully! Now you can return and start to enjoy all our sevices. "+
        "All the books are waiting foy your review!")

    except Exception as err:
        return render_template("error.html", message=err)

@app.route("/login", methods=["POST"])
def login():
    """Login the webpage"""
