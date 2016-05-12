"""Task Manager Site."""

import json
import httplib2

from apiclient import discovery
from oauth2client import client
from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Email, Task, connect_to_db, db

app = Flask(__name__)

# CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

app.secret_key = "\xa5\x85"

#Use os.envir (see lecture notes on how to store )

@app.route("/")
def base():
    """Index Page."""

  # if 'credentials' not in flask.session:
  #   return flask.redirect(flask.url_for('oauth2callback'))
  # credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  # if credentials.access_token_expired:
  #   return flask.redirect(flask.url_for('oauth2callback'))
  # else:
  #   http_auth = credentials.authorize(httplib2.Http())
  #   gmail_service = discovery.build('gmail', 'v1', http_auth)
  #   files = gmail_service.files().list().execute()
  #   return json.dumps(files)

    return render_template("login.html")

@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secret.json',
      scope='https://www.googleapis.com/auth/gmail.modify',
      redirect_uri=flask.url_for('oauth2callback', _external=True),
      include_granted_scopes=True)
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))

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