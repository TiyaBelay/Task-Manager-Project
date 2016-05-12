from httplib2 import Http
import os
from apiclient import errors
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import email
import base64

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


def get_messages_by_labelid(service, user_id, label_id):
    """Get messages given label ID.
    Args:
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_id: The ID of the label required.
    Returns:
    Messages in Label.
    """
    #Grabs a list of nested dictionary within another dictionary {dict:[{dict:key}]}
    results = service.users().messages().list(userId=user_id, labelIds=label_id).execute()
    # print results
    msgs = results.get('messages', []) #Looks for the key messages and returns a list of dict otherwise, it returns an empty list
    # print msgs

    for msg in msgs[:1]:
        message_info = get_message_by_id(service, 'me', msg['id'])
    # print message_info
    msg_str = base64.urlsafe_b64decode(message_info['raw'].encode('ASCII'))
    print msg_str #outputs body of message in html


        # payload_info = message_info['payload']['headers']
        # print payload_info
        #Best way to approach this is create own dictionary with the new key and values names that I want
        #Need to make the values of the keys in the list of dictionaries by my keys and values
        # for i in payload_info:
        #     for key, value in i.items():
        #         if key == 'name':
        #             print value


def get_message_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    return message


# #The dunder name tells you what the name of your file is and in this case since
# #we're calling the functions directly from the file, we can have our dunder name
# #equal to __main__. However, if this file was imported into another file, everything
# #outside of the function doesnt get called to the other file.
# print "this file's dunder name is", __name__
if __name__ == '__main__':

    #Since the below will be called throughout the entirety of the file, I left it outside the function
    credentials = get_credentials() 
    service = discovery.build('gmail', 'v1', http=credentials.authorize(Http()))
    msgs = get_messages_by_labelid(service, 'me', 'INBOX')
