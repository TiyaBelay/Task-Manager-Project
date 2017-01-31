import email
import base64
import os
from model import User, Email, Task, connect_to_db, db

def get_payload_headers(gmail_service, query):
        """List Messages of the user's inbox matching the query."""

        results = gmail_service.users().messages().list(userId='me', q=query).execute()
        msgs = results.get('messages', [])
        headers_dict = {}

        for msg in msgs:
            message_id_headers = {} #this dict is used to add the msg id as the key to the message dict payload_headers
            message_info = get_message_by_id(gmail_service, 'me', msg['id']) #msg ids and threadids
            message_id = str(message_info['id'])


            header_dict = {}
            payload_headers = message_info['payload']['headers']
            message_id_headers[message_id] = payload_headers

            for key, value in message_id_headers.items():
                for dict_items in value:
                    key = dict_items['name']
                    value = dict_items['value']
                    if key in ['Subject', 'From', 'Date']: #This is only grabbing 1 message instead of all messages
                        header_dict[key] = value

                for key in message_id_headers:
                    headers_dict[key] = header_dict

                date_str = header_dict['Date']
                From = header_dict['From']
                Subject = header_dict['Subject']
                msg_id = key

                emailpresentindb = db.session.query(Email).filter(Email.email_id == msg_id).first()

                if emailpresentindb is None:
                    message = Email(email_id=msg_id, subject=Subject, sender_email=From, received_at=date_str)
                    db.session.add(message)
                    db.session.commit()

                header_dict['Email'] = db.session.query(Email).filter(Email.email_id == msg_id).first()

        return headers_dict

def get_message_by_id(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    return message

def msg_body(gmail_service, msg_id):
        """List body of message."""

        message_info = get_message_by_id(gmail_service, 'me', msg_id)

        msg_body_str = base64.urlsafe_b64decode(message_info['payload']['parts'][1]['body']['data'].encode('ASCII'))

        msg_body_inst = email.message_from_string(msg_body_str)

        import pdb; pdb.set_trace()
        for part in msg_body_inst.walk():
            if part.get_content_type() == 'text/html' or part.get_content_type() == 'text/plain':
                message_payload = part.get_payload()
                message = message_payload.replace("\t", " ") #replaces the hard tab with single space to prevent the message rendered from concatenating

            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            counter = 1
        return message
