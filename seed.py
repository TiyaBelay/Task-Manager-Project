from model import User, Email, Task, connect_to_db, db
from server import app


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    
def CreateDraft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()

    print 'Draft id: %s\nDraft message: %s' % (draft['id'], draft['message'])

    return draft
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None


# def load_users():
#     """Load games from data/games.csv into database."""

#     #FIXME: write a function that parses users and adds it to the database.


#         # Need to add to the session or it won't ever be stored
#         db.session.add()

#     # Always commit
#     db.session.commit()

# def load_emails():
#     """Load games from data/games.csv into database."""

#     #FIXME: write a function that parses emails and adds it to the database.


#         # Need to add to the session or it won't ever be stored
#         db.session.add()

#     # Always commit
#     db.session.commit()

# def load_tasks():
#     """Load games from data/games.csv into database."""

#     #FIXME: write a function that parses tasks and adds it to the database.


#         # Need to add to the session or it won't ever be stored
#         db.session.add()

#     # Always commit
#     db.session.commit()


# if __name__ == "__main__":
#     connect_to_db(app)

#     db.create_all()
#     load_users()
#     load_emails()
#     load_tasks()