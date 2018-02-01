import unittest
import seed
from unittest import TestCase

class TestSeedMethods(unittest.TestCase):

    def open_file(self):
        assert seed.open_file('data_10_rest_json.txt') != None

    def test_clean_strings(self):
        """Tests clean_strings"""
        output = clean_strings(["one, two, three"])
        self.assertEquals(['one two three'], output)


if __name__ == "__main__":
    unittest.main()