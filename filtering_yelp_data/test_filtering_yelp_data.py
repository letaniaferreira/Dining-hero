import unittest
from filter_yelp_reviews import clean_strings, read_restaurants_file 
from filter_yelp_reviews import get_all_reviews_for_restaurant,get_file_name
from filter_yelp_reviews import get_first_non_restaurant_categories, join_strings
from unittest import TestCase


class TestFilterYelpReviews(unittest.TestCase):
    """Tests for running yelp data."""

    def test_read_restaurants_file(self):
        """Tests read_restaurants_file"""
        output = read_restaurants_file('test_dict_rest_json.txt')
        self.assertEquals([u"Domino's Pizza", [u'Sandwiches', u'Pizza', u'Chicken Wings', u'Restaurants']], output['BqsIt1BQKzS-hEKLYzBm7g'])

    # def test_get_all_reviews_for_restaurant(self):
    #     """Tests get_all_reviews_for_restaurant"""
    #     restaurants_dict = read_restaurants_file('test_dict_rest_json.txt')
    #     output = get_all_reviews_for_restaurant(restaurants_dict, 'test_review.json')
    #     self.assertEquals("gimme", output)
    #     self.assertEquals([u'This place is horrible, we were so excited to try it since I got a gift card for my birthday. We went in an ordered are whole meal and they did not except are gift card, because their system was down. Unacceptable, this would have been so helpful if we would have known this prior!!'], output['jQsNFOzDpxPmOurSWCg1vQ'])

    def test_get_file_name(self):
        """Tests get file name"""
        output = get_file_name("test", 1)
        self.assertEquals('test.1.csv', output)

    def test_get_empty_first_non_restaurant_categories(self):
        """Tests empty_first_non_restaurant_categories"""
        output = get_first_non_restaurant_categories([])
        self.assertEquals(None, output)

    def test_get_first_category_after_restaurant(self):
        """Tests get first category after the word Restaurants"""
        output = get_first_non_restaurant_categories(["Restaurants", "Chinese"])
        self.assertEquals('Chinese', output)

    def test_get_first_category_if_no_restaurant(self):
        """Tests get first category if the word Restaurants is not there"""
        output = get_first_non_restaurant_categories(["Italian", "Pasta"])
        self.assertEquals("Italian", output)

    def test_join_strings(self):
        """Tests join_strings"""
        output = join_strings(['test', 'one two three'], "Chinese")
        self.assertEquals(['test one two three', 'Chinese'], output)

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