import unittest
import seed

class TestSeedMethods(unittest.TestCase):

    def open_file(self):
        assert seed.open_file('data_10_rest_json.txt') != None


if __name__ == "__main__":
    # If called like a script, run our tests
    unittest.main()