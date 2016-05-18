"""Task Manager Site."""
import timestring
import email
import base64
import os
import json, httplib2
import pprint

from datetime import datetime
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

        try:
            results = gmail_service.users().messages().list(userId='me', q=query).execute()
            # print results
            msgs = results.get('messages', [])
            headers_dict = {}

            Email.query.delete()

            for msg in msgs:
                message_id_headers = {} #this dict is used to add the msg id as the key to the message dict payload_headers
                message_info = get_message_header_by_id(gmail_service, 'me', msg['id']) #msg ids and threadids
                # print message_info
                message_id = str(message_info['id'])
                # print type(message_id)
                # print message_id
                header_dict = {} #This caused a bit of an issue due to it being originally placed on line 74
                payload_headers = message_info['payload']['headers']#This list of a dict will be used for my subj, from, datetime info 
                # print payload_headers
                message_id_headers[message_id] = payload_headers
                # print message_id_headers
                for key, value in message_id_headers.items():
                    for dict_items in value:
                        key = dict_items['name']
                        # print key #works
                        value = dict_items['value']
                        # print value #works
                        if key in ['Subject', 'From', 'Date']: #This is only grabbing 1 message instead of all messages
                            header_dict[key] = value
                    # print header_dict
                    for key in message_id_headers:
                        # print key
                        headers_dict[key] = header_dict
                    # print headers_dict #WORKS! The key is my message id
                    #Got this from Steve Peak on stackoverflow
                    date_str = header_dict['Date']
                    Date = timestring.Date(date_str)
                    From = header_dict['From']
                    Subject = header_dict['Subject']
                    msg_id = key
                    # print Date
                    # print From
                    # print Subject
                    # print msg_id
                    message = Email(email_id=msg_id, subject=Subject, sender_email=From, received_at=Date)

                    db.session.add(message)
                db.session.commit()

            return render_template("inbox.html", 
                                    headers_dict=headers_dict,
                                    )
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

def get_message_header_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    return message

@app.route('/handle-message/<msg_id>')
def get_msg_body(msg_id):
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

        message_info = get_message_body_by_id(gmail_service, 'me', msg_id)
            # print message_info
        msg_body_str = base64.urlsafe_b64decode(message_info['raw'].encode('ASCII'))
        print msg_body_str
        msg_body_inst = email.message_from_string(msg_body_str) #converts my message body string to an instance using python's install lib 'email'
        
        #Got this from Jarret Hardie on stackoverflow for how to convert an instance into plain text
        for part in msg_body_inst.walk():
            if part.get_content_type() == 'text/plain':
                message = part.get_payload()
                print message
        # print msg_body_inst
        # print type(msg_body) #outputs body of message in html
        return render_template("message_body.html", 
                                message=message
                                )

def get_message_body_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    return message

@app.route("/task")
def create_task():
    """Create new task"""

    return render_template("tasks.html")

@app.route("/search-task")
def search_task():
    """Page with all tasks."""

    return render_template("listoftasks.html")
  
@app.route("/setting")
def settings_page():
    """Settings page."""

    return render_template("settings.html")

@app.route("/signout")
def signout():
    """Signout"""

    return redirect("/")

if __name__ == "__main__":
    # import logging
    # logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    app.debug = True # runs flask in debug mode, reloads code every time changes are made to this file

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    
    app.run()