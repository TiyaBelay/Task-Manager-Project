"""Models and database functions for TM."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of TM website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s first_name=%s last_name=%s >" % (self.user_id, self.email, self.first_name, self.last_name)


# Put your Emails and Task model classes here.

class Emails(db.Model):
    """Emails received from Gmail"""

    __tablename__ = "Emails"

    email_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(70), nullable=False)
    sender_name = db.Column(db.String(80), nullable=False)
    received_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Email email_id=%s subject=%s sender_email=%s sender_name=%s received_at=%s>" % (self.email_id, self.subject, self.sender_email, self.sender_name, self.received_at)


class Task(db.Model):
    """Tasks associated to Emails."""

    __tablename__ = "Tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('emails.email_id'), nullable=False)
    checklist = db.Column(db.String(800), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating task_id=%s user_id=%s email_id=%s checklist=%s timestamp>" % (self.task_id, self.user_id, self.email_id, self.checklist, self.timestamp)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("tasks", order_by=task_id))

    # Define relationship to email
    email = db.relationship("Email",
                            backref=db.backref("tasks", order_by=task_id))
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///taskmanager'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."