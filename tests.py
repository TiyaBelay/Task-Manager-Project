import unittest

from server import app
from model import db, example_user_data, example_email_data, example_task_data, connect_to_db


# class TaskManagerTests(unittest.TestCase):
#     """Tests for Task Manager site."""

#     def setUp(self):
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#     def test_homepage(self):
#         # FIXME: Add a test

#     pass

#     def test_signin(self):
#         # FIXME: Add a test

#     pass

#     def test_account_page(self):
#         # FIXME: Add a test

#     pass

#     def test_access_page(self):
#         # FIXME: Add a test

#     pass

#     def test_inbox(self):
#         # FIXME: Add a test

#     pass

#     def test_settings(self):
#         # FIXME: Add a test

#     pass

#     def test_search_tasks(self):
#         # FIXME: Add a test

#     pass


class TMTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        # Use name of test database here to override default database in model.py
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_pages(self):
        #FIXME: test that the pages displays from all example_()_data() functions

        pass

if __name__ == "__main__":
    unittest.main()