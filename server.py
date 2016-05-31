"""Task Manager Site."""
import timestring
import email
import base64
import os
import json, httplib2
import pprint

from psycopg2 import IntegrityError
from bs4 import BeautifulSoup
from jinja2 import StrictUndefined
from datetime import datetime
from apiclient import discovery, errors
from oauth2client import client
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Email, Task, connect_to_db, db

#Import search function to query from db
from sqlalchemy_searchable import search

app = Flask(__name__) #create a flask application

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
    # print flow
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

        # import pdb; pdb.set_trace() #Debugging

        credentials = get_credentials()
        if not credentials:
            return redirect(url_for('oauth2callback'))

        gmail_service = get_api(credentials)
        query = 'is:inbox'

        try:
            results = gmail_service.users().messages().list(userId='me', q=query).execute()
            msgs = results.get('messages', [])
            headers_dict = {}

            for msg in msgs:
                message_id_headers = {} #this dict is used to add the msg id as the key to the message dict payload_headers
                message_info = get_message_by_id(gmail_service, 'me', msg['id']) #msg ids and threadids
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

                    emailpresentindb = db.session.query(Email).filter(Email.email_id == msg_id).first()

                    if emailpresentindb is None:
                        message = Email(email_id=msg_id, subject=Subject, sender_email=From, received_at=Date)
                        db.session.add(message)
                        db.session.commit()

            return render_template("index.html", 
                                    headers_dict=headers_dict)
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

@app.route('/handle-message')
def get_msg_body():
        """List body of message."""

        credentials = get_credentials()
        if not credentials:
            return redirect(url_for('oauth2callback'))

        gmail_service = get_api(credentials)
        query = 'is:inbox'

        msg_id = request.args.get('id')

        message_info = get_message_by_id(gmail_service, 'me', msg_id)

        msg_body_str = base64.urlsafe_b64decode(message_info['payload']['parts'][1]['body']['data'].encode('ASCII'))

        msg_body_inst = email.message_from_string(msg_body_str) #converts my message body string to an instance using python's install lib 'email'

        for part in msg_body_inst.walk(): #this walk method from the email lib is a generator
            if part.get_content_type() == 'text/html' or part.get_content_type() == 'text/plain':
                message_payload = part.get_payload()
                message = message_payload.replace("\t", " ") #replaces the hard tab with single space to prevent the message rendered from concatenating

            #     message_body = Email(email_id=msg_id, body_content=message)

            #     db.session.add(message_body)
            # db.session.commit()
                return jsonify(message=message, msg_id=msg_id)

# @app.route('/handle-message/<msg_id>')
# def get_msg_body(msg_id):
#         """List body of message."""

#         credentials = get_credentials()
#         if not credentials:
#             return redirect(url_for('oauth2callback'))

#         gmail_service = get_api(credentials)
#         query = 'is:inbox'

#         message_info = get_message_by_id(gmail_service, 'me', msg_id)

#         msg_body_str = base64.urlsafe_b64decode(message_info['payload']['parts'][1]['body']['data'].encode('utf-8'))

#         msg_body_inst = email.message_from_string(msg_body_str) #converts my message body string to an instance using python's install lib 'email'

#         for part in msg_body_inst.walk(): #this walk method from the email lib is a generator
#             if part.get_content_type() == 'text/html' or part.get_content_type() == 'text/plain':
#                 message_payload = part.get_payload()
#                 message = message_payload.replace("\t", " ") #replaces the hard tab with single space to prevent the message rendered from concatenating

#                 # import pdb; pdb.set_trace() #Debugging

#                 # soup = BeautifulSoup(message, "html5lib")
#                 # g = soup.prettify() #This will render an html without the need to render a template, which is a problem since I need to be able to render a page to add the ability to create a task
#                 # g = str(g)
#             #     message_body = Email(email_id=msg_id, body_content=message)

#             #     db.session.add(message_body)
#             # db.session.commit()
#                 # return message
#         return render_template("message_body.html",
#                                 message=message,
#                                 msg_id=msg_id)

def get_message_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    return message

@app.route('/task/<msg_id>')
def create_task(msg_id):
    """Create new task"""

    return render_template("tasks.html",
                            msg_id=msg_id)

# @app.route('/task-list/<msg_id>', methods=['POST'])
# def search_task(msg_id):
#     """Show list of all tasks."""
    
#     # import pdb; pdb.set_trace()
#     task = request.form.get('entertask')
#     duedate = request.form.get('duedate')
#     taskcomp = request.form.get('comp')

#     taskpresentindb = db.session.query(Task).filter(Task.task_name == task).first()

#     if taskpresentindb is None:
#         task = Task(email_id= msg_id, task_name=task, due_date=duedate, task_completed=taskcomp)
#         db.session.add(task)
#         db.session.commit()

#     return redirect("/task-list")

@app.route('/task-list')
def search_task():
    """Show list of all tasks."""
    
    # import pdb; pdb.set_trace()
    task = request.form.get('entertask')
    duedate = request.form.get('duedate')
    taskcomp = request.form.get('comp')

    taskpresentindb = db.session.query(Task).filter(Task.task_name == task).first()

    if taskpresentindb is None:
        task = Task(email_id= msg_id, task_name=task, due_date=duedate, task_completed=taskcomp)
        db.session.add(task)
        db.session.commit()

    return redirect("/task-list")

@app.route("/task-list")
def list_of_tasks():

    tasks = Task.query.all()

    return render_template("listoftasks.html",
                            tasks=tasks)

#Got help from this doc in regards to SQLAlchemy-Searchable
#https://sqlalchemy-searchable.readthedocs.io/en/latest/search_query_parser.html
@app.route("/search-tasks")
def seach_tasks():
    """Search for tasks"""

    task_search = request.args.get("queryterm") #this correctly prints the value of my search
    
    taskdb = db.session.query(Task) #this is querying my task db
    results = search(taskdb, task_search) #the search query parser should look for the results of task_search against my db query

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

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    
    app.run()