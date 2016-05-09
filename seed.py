from model import User, Email, Task, connect_to_db, db
from server import app


def load_users():
    """Load games from data/games.csv into database."""

    #FIXME: write a function that parses users and adds it to the database.


        # Need to add to the session or it won't ever be stored
        db.session.add()

    # Always commit
    db.session.commit()

def load_emails():
    """Load games from data/games.csv into database."""

    #FIXME: write a function that parses emails and adds it to the database.


        # Need to add to the session or it won't ever be stored
        db.session.add()

    # Always commit
    db.session.commit()

def load_tasks():
    """Load games from data/games.csv into database."""

    #FIXME: write a function that parses tasks and adds it to the database.


        # Need to add to the session or it won't ever be stored
        db.session.add()

    # Always commit
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    load_users()
    load_emails()
    load_tasks()