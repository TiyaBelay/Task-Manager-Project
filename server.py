"""Task Manager Site."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Email, Task, connect_to_db, db

app = Flask(__name__)

app.secret_key = "Tobefilledin"


@app.route("/")
def homepage():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/login")
def Signin():
    """Gmail Signin."""

    return render_template("login.html")

@app.route("/account-page")
def account_page():
    """Choose Gmail account."""

    return render_template("choose_account.html")

@app.route("/access")
def access_page():
    """Gmail access authorization."""

    return render_template("allow_access.html")

@app.route("/inbox")
def inbox_page():
    """Inbox page."""

    return render_template("inbox.html")

@app.route("/search-task")
def search_task():
    """Page with all tasks."""

    return render_template("tasks.html")
  
@app.route("/setting")
def settings_page():
    """Settings page."""

    return render_template("settings.html")
  

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    #Use the DebugToolbar
    #DebugToolbarExtension(app)
    
    app.run()