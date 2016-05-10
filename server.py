"""Task Manager Site."""

import json
import sys
import os

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Email, Task, connect_to_db, db

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

app.secret_key = "Tobefilledin"

#Use os.envir (see lecture notes on how to store )

@app.route("/")
def base():
    """Index Page."""

    return render_template("login.html")

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

@app.route("/signout")
def signout():
    """Signout"""

    return redirect("/")

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    #Use the DebugToolbar
    #DebugToolbarExtension(app)
    
    app.run()