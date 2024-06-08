import spacy
import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TextPreprocessor:
    """
    A class for preprocessing text.

    Attributes:
        nlp (spacy.Language): SpaCy language model for text processing.
        stop_words (set): Set of stop words to be removed from text.
        stemmer (SnowballStemmer): Stemmer for stemming tokens.
    """

    def __init__(self):
        """
        Initializes the TextPreprocessor.
        """
        self.nlp = spacy.load('en_core_web_sm')
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')

    def clean_text(self, text):
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

    def remove_stopwords(self, tokens):
        """
        Removes stop words from the token list.

        Args:
            tokens (list): List of word tokens.

        Returns:
            list: List of tokens with stop words removed.
        """
        return [word for word in tokens if word not in self.stop_words]

    def lemmatize_tokens(self, tokens):
        """
        Lemmatizes the tokens using SpaCy.

        Args:
            tokens (list): List of word tokens.

        Returns:
            list: List of lemmatized tokens.
        """
        doc = self.nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]

    def stem_tokens(self, tokens):
        """
        Stems the tokens using the SnowballStemmer.

        Args:
            tokens (list): List of word tokens.

        Returns:
            list: List of stemmed tokens.
        """
        return [self.stemmer.stem(word) for word in tokens]

    def preprocess_text(self, text):
        """
        Preprocesses the input text by cleaning, tokenizing, removing stop words, and lemmatizing.

        Args:
            text (str): Input text to be preprocessed.

        Returns:
            str: Preprocessed text.
        """
        text = self.clean_text(text)
        tokens = word_tokenize(text)
        tokens = self.remove_stopwords(tokens)
        lemmatized_tokens = self.lemmatize_tokens(tokens)
        return " ".join(lemmatized_tokens)
