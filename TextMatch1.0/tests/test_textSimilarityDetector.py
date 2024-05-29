import unittest
import os
from textSimilarityDetector import TextSimilarityDetector

class TestTextSimilarityDetector(unittest.TestCase):

    def setUp(self):
        self.test_directory = "dataset/test_texts"
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)

        texts = [
            "This is a test document.",
            "Another test document with some different content.",
            "A third test document for testing purposes."
        ]
        for i, text in enumerate(texts):
            with open(os.path.join(self.test_directory, f"test_{i}.txt"), "w", encoding="utf-8") as file:
                file.write(text)

        self.detector = TextSimilarityDetector(self.test_directory)

    def tearDown(self):
        # Remove the test text files and directory
        for filename in os.listdir(self.test_directory):
            os.remove(os.path.join(self.test_directory, filename))
        os.rmdir(self.test_directory)

    def test_load_and_preprocess_texts(self):
        self.assertEqual(len(self.detector.texts), 3)
        self.assertEqual(len(self.detector.file_names), 3)

    def test_vectorize_texts(self):
        self.assertIsNotNone(self.detector.tfidf_vectorizer)
        self.assertIsNotNone(self.detector.X)

    def test_check_similarity(self):
        input_text = "This is a document for testing text similarity."
        result = self.detector.check_similarity(input_text)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        filename, similarity = result
        self.assertIsInstance(filename, str)
        self.assertIsInstance(similarity, float)

    def test_no_similar_texts(self):
        input_text = "Hello"
        result = self.detector.check_similarity(input_text)
        self.assertEqual(result[0], "No se encontraron textos similares")
        self.assertEqual(result[1], 0.0)
