import unittest
import numpy as np
from unittest.mock import MagicMock
from app.model.vectorizer import Vectorizer

class TestVectorizer(unittest.TestCase):
    def setUp(self):
        self.vectorizer = Vectorizer()
        self.mock_model = MagicMock()
        self.mock_model.vector_size = 100
        self.mock_model.wv = {'hello': np.random.rand(100), 'world': np.random.rand(100)}
        
    def test_vectorization_single_known_word(self):
        vector = self.vectorizer.get_sentence_vector("hello", self.mock_model)
        self.assertEqual(vector.shape, (100,))
        
    def test_vectorization_multiple_known_words(self):
        vector = self.vectorizer.get_sentence_vector("hello world", self.mock_model)
        self.assertEqual(vector.shape, (100,))
        
    def test_vectorization_unknown_words(self):
        vector = self.vectorizer.get_sentence_vector("xyz", self.mock_model)
        self.assertTrue(np.array_equal(vector, np.zeros(100)))
        
    def test_vectorization_empty_string(self):
        vector = self.vectorizer.get_sentence_vector("", self.mock_model)
        self.assertTrue(np.array_equal(vector, np.zeros(100)))
        
    def test_vectorization_mixed_known_unknown_words(self):
        vector = self.vectorizer.get_sentence_vector("hello xyz", self.mock_model)
        self.assertEqual(vector.shape, (100,))
        
    def test_vector_size_consistency(self):
        vector = self.vectorizer.get_sentence_vector("hello", self.mock_model)
        self.assertEqual(len(vector), self.mock_model.vector_size)