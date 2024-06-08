from gensim.models import Word2Vec
from difflib import SequenceMatcher
from sklearn.metrics.pairwise import cosine_similarity
from app.model.preprocessor import Preprocessor
from app.model.vectorizer import Vectorizer
from collections import deque
import spacy
import os

class PlagiarismDetector:
    """
    A class to detect plagiarism in text documents using various linguistic features and similarity measures.
    """
    
    def __init__(self) -> None:
        """
        Initializes the PlagiarismDetector with necessary models and preprocessors.
        """
        self.nlp = spacy.load('en_core_web_sm')
        self.preprocessor = Preprocessor()
        self.vectorizer = Vectorizer()
        self.original_texts, self.filenames, self.preprocessed_texts, self.token_lists = self.preprocessor.load_and_preprocess_files()
        self.model = None
        self.user_input_text = None
        self.user_input_preprocessed = None

    def set_user_input(self, user_input_text):
        """
        Sets the user input text for plagiarism detection.
        
        Parameters:
        - user_input_text (str): The text input by the user to check for plagiarism.
        """
        self.user_input_text = user_input_text

    def compare_sentences(self, sentences1, sentences2):
        """
        Compares sentences between two documents to find similar sentences.
        
        Parameters:
        - sentences1 (list): A list of sentences from the first document.
        - sentences2 (list): A list of sentences from the second document.
        
        Returns:
        - list: A list of tuples containing indices and sentences from both documents that are considered similar.
        """
        similar_sentences = []
        sentence_pairs = {}
        
        for i, sent1 in enumerate(sentences1):
            for j, sent2 in enumerate(sentences2):
                if (sent1, sent2) in sentence_pairs:
                    similarity = sentence_pairs[(sent1, sent2)]
                else:
                    similarity = SequenceMatcher(None, sent1, sent2).ratio()
                    sentence_pairs[(sent1, sent2)] = similarity

                if similarity > 0.7:  # Threshold for considering a sentence as similar
                    similar_sentences.append((i, j, sent1, sent2, similarity))
        return similar_sentences

    def detect_reordering(self, similar_sentences):
        """
        Detects reordering of similar sentences between two documents.
        
        Parameters:
        - similar_sentences (list): A list of tuples containing indices and sentences from both documents that are considered similar.
        
        Returns:
        - list: A list of tuples indicating pairs of sentences that have been reordered.
        """
        reordered = deque()
        for i in range(len(similar_sentences) - 1):
            idx1_doc1, idx1_doc2, _, _, _ = similar_sentences[i]
            idx2_doc1, idx2_doc2, _, _, _ = similar_sentences[i + 1]
            if idx1_doc1 < idx2_doc1 and idx1_doc2 > idx2_doc2:
                reordered.append((similar_sentences[i], similar_sentences[i + 1]))
        return list(reordered)
    
    def detect_tense_change(self, sent1, sent2):
        """
        Detects change in tense between two sentences.
        
        Parameters:
        - sent1 (str): The first sentence.
        - sent2 (str): The second sentence.
        
        Returns:
        - bool: True if there is a change in tense between the sentences, False otherwise.
        """
        doc1 = self.nlp(sent1)
        doc2 = self.nlp(sent2)
        tenses1 = [token.tag_ for token in doc1 if token.pos_ == 'VERB']
        tenses2 = [token.tag_ for token in doc2 if token.pos_ == 'VERB']
        return tenses1 != tenses2
    
    def detect_voice_change(self, sent1, sent2):
        """
        Detects change in voice (active/passive) between two sentences.
        
        Parameters:
        - sent1 (str): The first sentence.
        - sent2 (str): The second sentence.
        
        Returns:
        - bool: True if there is a change in voice between the sentences, False otherwise.
        """
        doc1 = self.nlp(sent1)
        doc2 = self.nlp(sent2)
        persons1 = [token.tag_ for token in doc1 if token.pos_ == 'PRON']
        persons2 = [token.tag_ for token in doc2 if token.pos_ == 'PRON']
        return persons1 != persons2
    
    def plagiarism_type(self):
        """
        Determines the type of plagiarism present in the user input text compared to original documents.
        
        Returns:
        - dict: A dictionary containing the type of plagiarism detected and the original documents involved.
        """
        plagiarism_results = {}

        # Split texts into sentences
        sentences_user = self.preprocessor.split_into_sentences(self.user_input_text)
        for original_dataset_text, dataset_filename in zip(self.original_texts, self.filenames):
            sentences_dataset = self.preprocessor.split_into_sentences(original_dataset_text)

            # Compare sentences
            similar_sentences = self.compare_sentences(sentences_dataset, sentences_user)
            reordered_sentences = self.detect_reordering(similar_sentences)

            if similar_sentences:
                plagiarism_type = None
                for idx1, idx2, sent1, sent2, similarity in similar_sentences:
                    if similarity < 1:
                        if self.detect_voice_change(sentences_user[idx2], sentences_dataset[idx1]):
                            plagiarism_type = "Voice change"
                            break
                        elif self.detect_tense_change(sentences_user[idx2], sentences_dataset[idx1]):
                            plagiarism_type = "Tense change"
                            break
                if not plagiarism_type:
                    if reordered_sentences:
                        plagiarism_type = "Sentence reordering"
                    else:
                        plagiarism_type = "Sentence modification"

                if "original_files" not in plagiarism_results:
                    plagiarism_results["original_files"] = {}
                if dataset_filename not in plagiarism_results["original_files"]:
                    plagiarism_results["original_files"][dataset_filename] = 0.0
                plagiarism_results["plagiarism_type"] = plagiarism_type

        return plagiarism_results
    
    def evaluate_similarity(self, model, plagiarism_results):
        """
        Evaluates the similarity of the user input text with original documents using a vector model.
        
        Parameters:
        - model: The vector model used for calculating similarity.
        - plagiarism_results (dict): The current plagiarism results to be updated with similarity scores.
        
        Returns:
        - dict: Updated plagiarism results including similarity scores.
        """
        similarity_threshold = 0.7
        input_vector = self.vectorizer.get_sentence_vector(self.user_input_text, model)
        for dataset_text, dataset_filename in zip(self.original_texts, self.filenames):
            dataset_vector = self.vectorizer.get_sentence_vector(dataset_text, model)
            similarity = cosine_similarity([input_vector], [dataset_vector])[0][0]

            if similarity > similarity_threshold:
                if "original_files" not in plagiarism_results:
                    plagiarism_results["original_files"] = {}
                plagiarism_results["original_files"][dataset_filename] = str(similarity)
            else:
                if "original_files" in plagiarism_results and dataset_filename in plagiarism_results["original_files"]:
                    del plagiarism_results["original_files"][dataset_filename]

        return plagiarism_results
    
    def get_results(self):
        """
        Gets the final plagiarism detection results after evaluating all aspects of plagiarism.
        
        Returns:
        - dict: The final results of plagiarism detection including types and similarity scores.
        """
        if os.path.exists("word2vec_model.bin"):
            self.model = Word2Vec.load("word2vec_model.bin")
        else:
            self.model = Word2Vec(sentences=self.token_lists, vector_size=150, window=2, min_count=2, workers=4,epochs=5000)
            self.model.save("word2vec_model.bin")


        plagarism_results = self.plagiarism_type()
        similarity_results = self.evaluate_similarity(self.model, plagarism_results)

        return similarity_results