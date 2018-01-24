import unittest
import server
from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class TestServerIntegration(unittest.TestCase):

    def test_main_page(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('What are you in the mood for?', result.data)

    def test_shows_user_form(self):
        client = server.app.test_client()
        result = client.get('/advanced_search_form')
        self.assertIn('What are you looking for today?', result.data)

    def test_login_form(self):
        client = server.app.test_client()
        result = client.get('/login')
        self.assertIn('Enter your information:', result.data)

    # def test_show_login(self):
    # client = server.app.test_client()
    # result = client.get('/show_login')
    # self.assertIn('Enter your information:', result.data)

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        client = server.app.test_client()
        result = client.post('/login', data={'email': 'andre@gmail.com',
                                             'password': 'andrepassword'},
                                            follow_redirects=True)
        self.assertIn('Rate a restaurant', result.data)




if __name__ == "__main__":
    unittest.main()