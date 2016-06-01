"""Task Manager Site."""
import timestring
import email
import base64
import os
import json, httplib2

from parser import *
from jinja2 import StrictUndefined
from apiclient import discovery, errors
from oauth2client import client
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Email, Task, connect_to_db, db

#Imported search function to query from db
from sqlalchemy_searchable import search

app = Flask(__name__)

app.secret_key = os.environ["FLASK_APP_KEY"]

#Added this to raise an error when an undefined variable is used in Jinja
app.jinja_env.undefined = StrictUndefined 

@app.route("/")
def login():
    """Gmail login"""

    return render_template("login.html")

@app.route("/oauth2callback")
def oauth2callback():
    #created an object used to operate OAuth 2.0 operations
    flow = client.flow_from_clientsecrets(
                    'client_secret.json',
                    scope='https://www.googleapis.com/auth/gmail.readonly',
                    redirect_uri=url_for('oauth2callback', _external=True))

    if 'code' not in request.args:#This will redirect the user to Google's OAuth 2.0 server and based of the response of the user will redirect accordingly
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code) #once the authorization code is recieved from the user, it will be exchanged for an access token using step2_exchange
        session['credentials'] = credentials.to_json()
        return redirect(url_for('inbox'))

def get_credentials():
    if 'credentials' not in session:
        return False
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return False
    return credentials

def get_api(credentials):
    http_auth = credentials.authorize(httplib2.Http())
    gmail_service = discovery.build('gmail', 'v1', http_auth)

    return gmail_service

@app.route('/inbox')
def inbox():
        """List Messages of the user's inbox matching the query."""

        credentials = get_credentials()
        if not credentials:
            return redirect(url_for('oauth2callback'))

        gmail_service = get_api(credentials)
        query = 'is:inbox'

        headers_dict = get_payload_headers(gmail_service, query)

        return render_template("index.html", 
                                headers_dict=headers_dict)

@app.route('/handle-message')
def get_msg_body():
        """Retrieve body of message."""

        credentials = get_credentials()
        if not credentials:
            return redirect(url_for('oauth2callback'))

        gmail_service = get_api(credentials)
        query = 'is:inbox'

        msg_id = request.args.get('id')

        message = msg_body(gmail_service, msg_id)

        return jsonify(message=message, msg_id=msg_id)

@app.route('/add-tasks')
def search_task():
    """Show list of all tasks."""
    
    # import pdb; pdb.set_trace()
    msg_id = request.args.get('msgid')
    task = request.args.get('entertask')
    duedate = request.args.get('duedate')

    taskpresentindb = db.session.query(Task).filter(Task.task_name == task).first()

    if taskpresentindb is None:
        task = Task(email_id=msg_id, task_name=task, due_date=duedate)
        db.session.add(task)
        db.session.commit()

    return jsonify(msg_id=msgid)

@app.route("/task-list")
def list_of_tasks():

    # import pdb; pdb.set_trace()
    task_completion = request.args.get("comp") #this returns None
    task_name = request.args.get("task")

    taskindb = db.session.query(Task).filter(Task.task_name == task_name).first()

    if taskindb:
        task_comp = Task(task_completed=task_completion).update()
        db.session.add(task_comp)
        db.session.commit()

    tasks = Task.query.all()

    return render_template("listoftasks.html",
                            tasks=tasks)

#Got help from this doc in regards to SQLAlchemy-Searchable
#https://sqlalchemy-searchable.readthedocs.io/en/latest/search_query_parser.html
@app.route("/search-tasks")
def seach_tasks():
    """Search for tasks"""

    task_search = request.args.get("queryterm")
    
    taskdb = db.session.query(Task)
    results = search(taskdb, task_search)

    return render_template("search_tasks.html",
                            results=results)

@app.route("/signout")
def signout():
    """Signout"""

    session.clear()

    flash("You are now logged out!")

    return redirect("/")

if __name__ == "__main__":
    app.debug = True # runs flask in debug mode, reloads code every time changes are made to this file

    connect_to_db(app)
    
    app.run()