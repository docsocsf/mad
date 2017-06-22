import string
import unittest

from common.util.generator import get_random_id


class GeneratorTests(unittest.TestCase):
    def test_default_length(self):
        self.assertEqual(len(get_random_id()), 8)

    def test_length_as_specified(self):
        for i in range(1, 10):
            self.assertEqual(len(get_random_id(i)), i)

    def test_random_ids_are_different(self):
        self.assertNotEqual(get_random_id(), get_random_id())

    def test_only_characters_or_digits(self):
        for c in get_random_id(20):
            self.assertTrue(c in string.ascii_letters + string.digits)
