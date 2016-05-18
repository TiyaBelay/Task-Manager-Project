from httplib2 import Http
import os
from apiclient import errors
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


try:
    import argparse #imported module from Gmails py lib
    #Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=False)
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Task Manager'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~') #/Users/TMD
    credential_dir = os.path.join(home_dir, '.credentials') #This line adds the directory .credentials to my home_dir so /Users/TMD/.credentials
    print credential_dir
    #If the credentials directory does not exist, the conditional creates the credential 
    #directory and joins it's json file containing the id and pwd to the credentials directory
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'task-manager.json')
    store = oauth2client.file.Storage(credential_path) #Creates an object named store <oauth2client.file.Storage object at 0x10324c6d0>
    credentials = store.get() #Applies the get() method on the object and stores the new object as credentials
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def get_api_object():
    """This is used to make API calls"""
    
    credentials = get_credentials()
    http=credentials.authorize(Http())
    gmail_service = discovery.build('gmail', 'v1', http=http)

    return gmail_service

def add_to_db():

    gmail_service = get_api_object()
