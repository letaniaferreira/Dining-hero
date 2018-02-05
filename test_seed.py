import unittest
import seed
from server import app
import model
from sqlalchemy_utils import database_exists, create_database
from unittest import TestCase

class TestSeedMethods(unittest.TestCase):
    """Tests simple Seed methods"""

    def test_open_file(self):
        """Tests open_file"""
        output = seed.open_file('open_test.txt')
        self.assertEquals('this is a test', output)

class TestSeedUsingDatabase(TestCase):
    """Tests Seed methods that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        seeddb = "postgresql:///testseeddb"

        # check if db exists
        if not database_exists(seeddb):

            # if it does not exist, create it
            create_database(seeddb)

        # Connect to testseed database
        model.connect_to_db(app, seeddb)

        # Create tables
        model.db.create_all()

        #Add instance variable/attribute
        self.test_data = seed.open_file('test_data_rest_json.txt')

    def tearDown(self):
        """Do at end of every test."""

        model.db.session.close()
        model.db.drop_all()


    def test_load_restaurants(self):
        """Tests load_restaurants"""

        restaurant_name = 'Hippie Thai Street Food'

        # Do some stuff we want to test
        ## call load_restaurants with test data
        seed.load_restaurants(self.test_data)

        # Do what we need to get verification
        ## find restaurant we expect to be in database based on test data
        test_restaurant = model.Restaurant.query.filter_by(name=restaurant_name).first()
        # Verify results
        ## Assert that data is equal to what we expect
        self.assertEquals(restaurant_name, test_restaurant.name)

    def test_load_categories(self):
        """Tests load_categories"""

        seed.load_restaurants(self.test_data)
        specialty = 'Thai'
        seed.load_categories(self.test_data)
        test_category = model.Category.query.filter_by(specialty=specialty).first()
        self.assertEquals(specialty, test_category.specialty)

    def test_load_users(self):
        """Tests load_restaurants"""

        user_fname = 'Felic'
        seed.load_users(self.test_data)
        test_user = model.User.query.filter_by(fname=user_fname).first()
        self.assertEquals(user_fname, test_user.fname)

    # def test_load_ratings(self):
    #     """Tests load_ratings"""

    #     reference_score = '4'
    #     seed.load_ratings(self.test_data)
    #     test_score = model.Rating.query.filter_by(score=reference_score).first()
    #     self.assertEquals(eference_score, test_score.score)




if __name__ == "__main__":
    unittest.main()