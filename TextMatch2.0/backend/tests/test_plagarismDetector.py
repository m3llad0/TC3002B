import unittest
from gensim.models import Word2Vec
from app.model.plagarsimDetector import PlagiarismDetector

class TestPlagiarismDetector(unittest.TestCase):

    def setUp(self):
        self.detector = PlagiarismDetector()
        self.model = Word2Vec.load("word2vec_model.bin")
        self.input = """Facial recognition technology (FRT) is becoming quite popular worldwide due to its contactless biometric characteristics, moving the world towards contactless FRT after the COVID-19 pandemic. It is one of the most successful and fascinating technologies of modern times, with businesses replacing conventional fingerprint scanners with artificial intelligence-based FRT, opening up enormous commercial prospects. Security and surveillance, authentication/access control systems, digital healthcare, photo retrieval, etc., are some sectors where its use has become essential. The face, with its distinctive traits, is the most essential part of the human body, crucial for recognizing people. In the present communication, we presented the global adoption of FRT, its rising trend in the market, utilization of the technology in various sectors, its challenges, and rising concerns with special reference to India and worldwide."""

    def test_set_user_input(self):
        input_text = self.input
        self.detector.set_user_input(input_text)
        self.assertEqual(self.detector.user_input_text, input_text)

    def test_compare_sentences(self):
        sentences1 = ["This is a test.", "Another test sentence."]
        sentences2 = ["This is a test.", "Yet another sentence for testing."]
        similar_sentences = self.detector.compare_sentences(sentences1, sentences2)
        expected_result = [(0, 0, "This is a test.", "This is a test.", 1.0)]
        self.assertEqual(similar_sentences, expected_result)

    def test_plagiarism_type(self):
        self.detector.user_input_text = self.input
        plagiarism_results = self.detector.plagiarism_type()
        expected_result = {'original_files': {'org-022.txt': 0.0}, 'plagiarism_type': 'Sentence modification'}
        self.assertEqual(plagiarism_results, expected_result)

    def test_evaluate_similarity(self):

        self.detector.user_input_text = self.input
        plagiarism_results = self.detector.plagiarism_type()
        results = self.detector.evaluate_similarity(self.model, plagiarism_results)

        expected_result = {'original_files': {'org-022.txt': '0.99844456'}, 'plagiarism_type': 'Sentence modification'}
        self.assertEqual(results, expected_result)

    def test_get_results(self):
        self.detector.user_input_text = self.input

        results = self.detector.get_results()

        expected_result = {'original_files': {'org-022.txt': '0.99844456'}, 'plagiarism_type': 'Sentence modification'}
        self.assertEqual(results, expected_result)
