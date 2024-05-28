import unittest
from textPreprocessor import TextPreprocessor

class TestTextPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = TextPreprocessor()

    def test_clean_text(self):
        text = "Hello, World! 123"
        expected_output = "hello world "
        self.assertEqual(self.preprocessor.clean_text(text), expected_output)

    def test_remove_stopwords(self):
        tokens = ["this", "is", "a", "test"]
        expected_output = ["test"]
        self.assertEqual(self.preprocessor.remove_stopwords(tokens), expected_output)

    def test_lemmatize_tokens(self):
        tokens = ["cats", "are", "running"]
        expected_output = ["cat", "be", "run"]
        self.assertEqual(self.preprocessor.lemmatize_tokens(tokens), expected_output)

    def test_stem_tokens(self):
        tokens = ["running", "jumps", "leaves"]
        expected_output = ["run", "jump", "leav"]
        self.assertEqual(self.preprocessor.stem_tokens(tokens), expected_output)

    def test_preprocess_text(self):
        text = "Hello, World! This is a test."
        expected_output = "hello world test"
        self.assertEqual(self.preprocessor.preprocess_text(text), expected_output)