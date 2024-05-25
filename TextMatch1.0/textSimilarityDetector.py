import spacy
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TextSimilarityDetector:
    """
    A class to detect text similarity using TF-IDF and cosine similarity.

    Attributes:
        nlp (spacy.Language): SpaCy language model for text processing.
        stop_words (set): Set of stop words to be removed from text.
        stemmer (SnowballStemmer): Stemmer for stemming tokens.
        directory (str): Directory containing text files to be processed.
        texts (list): List of preprocessed text contents from files.
        file_names (list): List of filenames corresponding to the texts.
        tfidf_vectorizer (TfidfVectorizer): TF-IDF vectorizer for text vectorization.
        X (scipy.sparse.csr.csr_matrix): TF-IDF matrix for the preprocessed texts.
    """

    def __init__(self, directory):
        """
        Initializes the TextSimilarityDetector with the directory of text files.

        Args:
            directory (str): Path to the directory containing text files.
        """
        self.nlp = spacy.load('en_core_web_sm')
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')
        self.directory = directory
        self.texts = []
        self.file_names = []
        self._load_and_preprocess_texts()
        self._vectorize_texts()

    def _clean_text(self, text):
        """
        Cleans the input text by lowering the case, removing digits and non-alphanumeric characters.

        Args:
            text (str): Input text to be cleaned.

        Returns:
            str: Cleaned text.
        """
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\W+', ' ', text)
        return text

    def _remove_stopwords(self, tokens):
        """
        Removes stop words from the token list.

        Args:
            tokens (list): List of word tokens.

        Returns:
            list: List of tokens with stop words removed.
        """
        return [word for word in tokens if word not in self.stop_words]

    def _lemmatize_tokens(self, tokens):
        """
        Lemmatizes the tokens using SpaCy.

        Args:
            tokens (list): List of word tokens.

        Returns:
            list: List of lemmatized tokens.
        """
        doc = self.nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]

    def _stem_tokens(self, tokens):
        """
        Stems the tokens using the SnowballStemmer.

        Args:
            tokens (list): List of word tokens.

        Returns:
            list: List of stemmed tokens.
        """
        return [self.stemmer.stem(word) for word in tokens]

    def _preprocess_text(self, text):
        """
        Preprocesses the input text by cleaning, tokenizing, removing stop words, and lemmatizing.

        Args:
            text (str): Input text to be preprocessed.

        Returns:
            str: Preprocessed text.
        """
        text = self._clean_text(text)
        tokens = word_tokenize(text)
        tokens = self._remove_stopwords(tokens)
        lemmatized_tokens = self._lemmatize_tokens(tokens)
        return " ".join(lemmatized_tokens)

    def _load_and_preprocess_texts(self):
        """
        Loads and preprocesses all text files in the specified directory.
        """
        for filename in os.listdir(self.directory):
            if filename.endswith('.txt'):
                with open(os.path.join(self.directory, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    preprocessed_text = self._preprocess_text(text)
                    self.texts.append(preprocessed_text)
                    self.file_names.append(filename)
        print("Número de archivos procesados:", len(self.texts))

    def _vectorize_texts(self):
        """
        Vectorizes the preprocessed texts using TF-IDF.
        """
        self.tfidf_vectorizer = TfidfVectorizer()
        self.X = self.tfidf_vectorizer.fit_transform(self.texts)
        print("Dimensión de la matriz TF-IDF:", self.X.shape)

    def check_similarity(self, input_text, similarity_threshold=0.3):
        """
        Checks the similarity of the input text with the preprocessed texts in the directory.

        Args:
            input_text (str): Input text to be checked for similarity.
            similarity_threshold (float): Threshold above which texts are considered similar.
        """
        preprocessed_input_text = self._preprocess_text(input_text)
        input_vector = self.tfidf_vectorizer.transform([preprocessed_input_text])
        cosine_similarities = cosine_similarity(input_vector, self.X).flatten()

        for i, similarity in enumerate(cosine_similarities):
            if similarity > similarity_threshold:
                print(f"Archivo: {self.file_names[i]}, Similitud: {similarity:.4f}")