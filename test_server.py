import unittest
import server
from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class TestServerIntegration(unittest.TestCase):
    """Flask tests for routes."""

    def test_main_page(self):
        """Tests main route"""
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('What are you in the mood for?', result.data)

    def test_shows_user_form(self):
        """Tests adavnced search route"""
        client = server.app.test_client()
        result = client.get('/advanced_search_form')
        self.assertIn('What are you looking for today?', result.data)

    def test_login_form(self):
        """Tests route to login_form"""
        client = server.app.test_client()
        result = client.get('/login')
        self.assertIn('Enter your information:', result.data)

    def test_resgistration_form(self):
        """Tests route to registration_form"""
        client = server.app.test_client()
        result = client.get('/registration')
        self.assertIn('Please register to create an account', result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Connect to test database
        connect_to_db(app, "postgresql:///testserverdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Tests login"""
        client = server.app.test_client()
        result = client.post('/login', data={'email': 'andre@gmail.com',
                                             'password': 'andrepassword'},
                                            follow_redirects=True)
        self.assertIn('Login sucessful!', result.data)

    def test_registration(self):
        """Tests registration"""
        client = server.app.test_client()
        result = client.post('/registration', data={'fname': 'marco',
                                                    'username': 'marcof',
                                                    'email': 'marco@gmail.com',
                                                    'password': 'marcopassword',
                                                    'phone': '123-456-7890'},
                                                    follow_redirects=True)
        self.assertIn('You have been registered!', result.data)

    def test_profile(self):
        """Tests profile search"""
        client = server.app.test_client()
        client.post('/login', data={'email': 'andre@gmail.com',
                                    'password': 'andrepassword'},
                                    follow_redirects=True)
        result = client.get('/profile', follow_redirects=True)
        self.assertIn('Your favorite spots:', result.data)

    def test_results(self):
        """Tests basic search"""
        client = server.app.test_client()
        result = client.get('/results?type_of_food=Spicy',
                                            follow_redirects=True)
        self.assertIn('Try this place:', result.data)

    def test_rating_route(self):
        """Tests rating routing"""
        client = server.app.test_client()
        result = client.get('/rating_results') #needs to be in this class because it uses db.
                                                  
        self.assertIn('Rate another restaurant:', result.data)

    def test_rating(self):
        """Tests rating"""
        client = server.app.test_client()
        client.post('/login', data={'email': 'andre@gmail.com',
                                             'password': 'andrepassword'},
                                            follow_redirects=True)
        result = client.post('/rating', data={'restaurant': '02',
                                            'score': '4',
                                            'user_review': 'Great herb chicken'},
                                            follow_redirects=True)
        self.assertIn('You gave', result.data)

    def test_sending_sms(self):
        """Tests sending sms"""
        client = server.app.test_client()
        client.post('/login', data={'email': 'joana@gmail.com',
                                             'password': 'joanapassword'},
                                            follow_redirects=True)
        result = client.post('/sms', data={'message': 'Live music today'},
                                            follow_redirects=True)
        self.assertIn('You have sucessfully sent the following sms to customers', result.data)


if __name__ == "__main__":
    unittest.main()