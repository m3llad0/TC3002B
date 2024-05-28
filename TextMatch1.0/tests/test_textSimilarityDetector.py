import unittest
import os
from textSimilarityDetector import TextSimilarityDetector
from textPreprocessor import TextPreprocessor

class TestTextSimilarityDetector(unittest.TestCase):
    def setUp(self):
        self.detector = TextSimilarityDetector('dataset/files')
        self.test_directory = 'dataset/test_files'

    def test_plagiarized_texts(self):
        
        for filename in os.listdir(self.test_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.test_directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    test_text = file.read()
                    print(f"Results for {filename}:")
                    result, similarity = self.detector.check_similarity(test_text, similarity_threshold=0.3)
                    print(f"File: {result}, Similarity: {similarity:.4f}")