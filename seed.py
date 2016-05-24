from model import User, Email, Task, connect_to_db, db
from apiclient import errors
from server import app
import base64
import email




# def load_users():
    #FIXME: write a function that parses users and adds it to the database.


        # Need to add to the session or it won't ever be stored
    #     db.session.add()

    # # Always commit
    # db.session.commit()

def oauth2callback():
    # import pdb; pdb.set_trace() #Debugging

    #created an object used to operate OAuth 2.0 operations
    flow = client.flow_from_clientsecrets(
                    'client_secret.json',
                    scope='https://www.googleapis.com/auth/gmail.readonly',
                    redirect_uri=url_for('oauth2callback', _external=True),
                    )
    # print flow
    if 'code' not in request.args:#This will redirect the user to Google's OAuth 2.0 server and based of the response of the user will redirect accordingly
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code) #once the authorization code is recieved from the user, it will be exchanged for an access token using step2_exchange
        # http_auth = credentials.authorize(httplib2.Http())
        # gmail_service = discovery.build('gmail', 'v1', http_auth)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('inbox'))

def api_call():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        gmail_service = discovery.build('gmail', 'v1', http_auth)
        query = 'is:inbox'  


def get_message_by_id(service, user_id, msg_id):
    """Get a message when passed a msg_id for a user"""

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        return message

    except errors.HttpError, error:
        print 'An error occurred: %s' % error

def load_emails():
    #FIXME: write a function that parses emails and adds it to the database.
    results = api_call().users().messages().list(userId='me', q=query).execute()
    # print results
    msgs = results.get('messages', [])
    # print msgs

    for msg in msgs:
        msg_id = msg['id']
        # print msg_id
        message_info = get_message_by_id(gmail_service, 'me', msg['id'])
        # print message_info
        msg_body_str = base64.urlsafe_b64decode(message_info['raw'].encode('ASCII'))
        # print msg_body_str
        msg_body_inst = email.message_from_string(msg_body_str) #converts my message body string to an instance using python's install lib 'email'
        # print msg_body_inst
        Subject = msg_body_inst['Subject']
        # print Subject
        Date = str(msg_body_inst['Date'])
        # print Date
        From = msg_body_inst['From']
        # print From
        

        message = Email(email_id=msg['id'], subject=Subject, sender_email=From, received_at=Date)

        # Need to add to the session or it won't ever be stored
        db.session.add()

    # Always commit
    db.session.commit()

# def load_tasks():
    #FIXME: write a function that parses tasks and adds it to the database.


        # Need to add to the session or it won't ever be stored
        # db.session.add()

    # Always commit
    # db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    # load_users()
    load_emails()
    # load_tasks()