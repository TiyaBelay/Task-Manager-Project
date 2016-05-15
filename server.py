"""Task Manager Site."""

import email
import base64
import os
import json, httplib2
import pprint

from apiclient import discovery, errors
from oauth2client import client
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Email, Task, connect_to_db, db

app = Flask(__name__) #create a flask application

app.secret_key = os.environ["FLASK_APP_KEY"]

@app.route("/")
def login():
    """Gmail login"""

    return render_template("login.html")

@app.route("/oauth2callback")
def oauth2callback():
    flow = client.flow_from_clientsecrets(
                    'client_secret.json',
                    scope='https://www.googleapis.com/auth/gmail.readonly',
                    redirect_uri=url_for('oauth2callback', _external=True),
                    )
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('login'))

@app.route('/inbox')
def inbox():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        gmail_service = discovery.build('gmail', 'v1', http_auth)
        query = 'is:inbox'
        """List all Messages of the user's inbox matching the query.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
        """
        # import pdb; pdb.set_trace() #Debugging

        header_dict = {}

        try:
            response = gmail_service.users().messages().list(userId='me', q=query).execute() #this returns a list of nested dictionary within a dict 
            list_messages = []
            if 'messages' in response:
                print 'test %s' % response
                list_messages.extend(response['messages'])
            while 'nextPageToken' in response:
                page_token = response['nextPageToken'] #returns page_token as an integer
                response = gmail_service.users().messages().list(userId='me', q=query, pageToken=page_token).execute() #returns list of messageid's and threadid's for a specific pagetoken
                msgs = response.get('messages', []) #Looks for the key messages and returns a list of dict otherwise, it returns an empty list
                print msgs

                for msg in msgs:
                    message_info = get_message_header_by_id(gmail_service, 'me', msg['id'])
                    payload_headers = message_info['payload']['headers'] #This list of a dict will be used for my subj, from, datetime info 
                    for dict_items in payload_headers:
                        key = dict_items['name']
                        print key #works
                        value = dict_items['value']
                        print value #works
                        if key in ['Subject', 'From', 'Date']:
                            header_dict[key] = value

                return render_template("inbox.html", 
                                        header_dict=header_dict
                                        )
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

def get_message_header_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    return message

@app.route('/handle-message')
def get_msg_body():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        gmail_service = discovery.build('gmail', 'v1', http_auth)
        query = 'is:inbox'

        # import pdb; pdb.set_trace() #Debugging
        #Grabs a list of nested dictionary within another dictionary {dict:[{dict:key}]}
        results = gmail_service.users().messages().list(userId='me').execute()
        print results
        msgs = results.get('messages', []) #Looks for the key messages and returns a list of dict otherwise, it returns an empty list
        # print msgs

        for msg in msgs[:1]:
            message_info = get_message_body_by_id(gmail_service, 'me', msg['id'])
        print message_info
        msg_body = base64.urlsafe_b64decode(message_info['raw'].encode('ASCII'))
        print msg_body #outputs body of message in html
        return render_template("message_body.html", 
                                msg_body=msg_body
                                )

def get_message_body_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    return message

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
    import logging
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    app.debug = True # runs flask in debug mode, reloads code every time changes are made to this file

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    
    app.run()