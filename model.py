from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User details"""

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s f_name=%s l_name=%s email=%s>" % (self.user_id, self.f_name, self.l_name, self.email)

class Email(db.Model):
    """Email details"""

    __tablename__ = "emails"
    email_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    subject = db.Column(db.String(120), nullable=False)
    sender_email = db.Column(db.String(80), nullable=False)
    sender_f_name = db.Column(db.String(30), nullable=True)
    sender_l_name = db.Column(db.String(30), nullable=True)
    received_at = db.Column(db.DateTime, nullable=False)
    attachment_received = db.Column(db.Boolean, nullable=True)
    body_content = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Email email_id=%s user_id=%s subject=%s sender_email=%s received_at=%s>" % (self.email_id, user_id, self.subject, self.sender_email, self.received_at)

class Task(db.Model):
    """Task details"""

    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(db.Integer, db.ForeignKey('emails.email_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    task_name = db.Column(db.String(20), nullable=False)
    task_created_at = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    task_completed = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Task task_id=%s task_name=%s task_created_at=%s task_completed=%s>" % (self.task_id, self.task_name, self.task_created_at, self.task_completed)

class Checklist(db.Model):
    """Checklist information"""

    __tablename__ = "checklists"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checklist = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Checklist task_id=%s checklist=%s>" % (self.task_id, self.checklist)

##############################################################################
# Test functions

def example_user_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a user and adds it to the database.

    tiya = User(f_name='Tiya', l_name='Belay', email='tiya@gmail.com')
    din = User(f_name='Din', l_name='Kostka', email='dinny@gmail.com')

    db.session.add_all([tiya, din])
    db.session.commit()
 
    pass

def example_email_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates an email and adds it to the database.

    testing = Email(subject='Check in', sender_email = 'test@gmail.com', sender_f_name = 'Test', sender_l_name = 'Junior', received_at = '05/09/2016', attachment_received = 'False', body_content = 'Wanted to check in on you and make sure everything is good!')

    db.session.add(testing)
    db.session.commit()

    pass

def example_task_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a task and adds it to the database.

    firsttask = Task(task_name='Complete test db', task_created_at='05/09/2016', due_date='05/09/2016', task_completed='False')

    db.session.add(firsttask)
    db.session.commit()

    pass

def example_checklist_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a checklist and adds it to the database.

    db.session.add()
    db.session.commit()

    pass

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to the Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///taskmanager'
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

    from server import app
    import os

    os.system("dropdb taskmanager")
    os.system("createdb taskmanager")

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()