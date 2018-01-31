import unittest
from filter_yelp_reviews import clean_strings
from unittest import TestCase


class TestFilterYelpReviews(unittest.TestCase):
    """Flask tests for routes."""

    def test_clean_strings(self):
        """Tests clean_strings"""
        output = clean_strings(["one, two, three"])
        self.assertEquals(['one two three'], output)

    def test_clean_strings_wrong_quotes(self):
        """Tests correct use of quotes in clean_strings"""
        output = clean_strings(["one, two, three"])
        self.assertEquals(['one two three'], output)

    def test_clean_strings_special_characters(self):
        """Tests if clean_strings ignores special characters"""
        output = clean_strings(["test", "one, two, and three\xc5\xbe"])
        self.assertEquals(['test', 'one two and three'], output)

    def test_clean_strings_next_line(self):
        """Tests if clean_strings ignores next line character"""
        output = clean_strings(["test", "one, two, three.\n Next line."])
        self.assertEquals(['test', 'one two three. Next line.'], output)

if __name__ == "__main__":
    unittest.main()