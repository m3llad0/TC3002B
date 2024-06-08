import unittest
from app.model.preprocessor import Preprocessor

class TestCleanText(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor()

    def test_lowercase_conversion(self):
        self.assertEqual(self.preprocessor.clean_text("TEST"), "test")

    def test_digit_removal(self):
        self.assertEqual(self.preprocessor.clean_text("123test"), "test")

    def test_non_word_character_replacement(self):
        self.assertEqual(self.preprocessor.clean_text("test!@#$%^&*()+"), "test ")

    def test_empty_string(self):
        self.assertEqual(self.preprocessor.clean_text(""), "")

    def test_mixed_input(self):
        self.assertEqual(self.preprocessor.clean_text("Hello World! 123"), "hello world ")