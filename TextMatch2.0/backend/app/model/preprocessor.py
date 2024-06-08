import os
import re
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Preprocessor:
    """
    A class for preprocessing text data including cleaning text, removing stopwords,
    lemmatizing tokens, and loading and preprocessing files from a directory.
    """
    def __init__(self):
        """
        Initializes the Preprocessor class by downloading necessary NLTK data and loading the Spacy model.
        It also sets the directory from which text files will be loaded and preprocessed.
        """
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.nlp = spacy.load('en_core_web_sm')
        self.stop_words = set(stopwords.words('english'))
        self.directory = "dataset/files"

    def clean_text(self, text):
        """
        Cleans the input text by converting to lowercase, removing digits, and substituting non-word characters with a space.

        Parameters:
        - text (str): The text to be cleaned.

        Returns:
        - str: The cleaned text.
        """
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\W+', ' ', text)
        return text

    def remove_stopwords(self, tokens):
        """
        Removes stopwords from a list of tokens.

        Parameters:
        - tokens (list of str): The tokens from which stopwords are to be removed.

        Returns:
        - list of str: The tokens with stopwords removed.
        """
        return [word for word in tokens if word not in self.stop_words]

    def lemmatize_tokens(self, tokens):
        """
        Lemmatizes a list of tokens using Spacy.

        Parameters:
        - tokens (list of str): The tokens to be lemmatized.

        Returns:
        - list of str: The lemmatized tokens.
        """
        doc = self.nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]

    def preprocess_text(self, text):
        """
        Preprocesses the input text by cleaning, tokenizing, removing stopwords, and lemmatizing.

        Parameters:
        - text (str): The text to be preprocessed.

        Returns:
        - tuple: A tuple containing the preprocessed text as a string and a list of lemmatized tokens.
        """
        text = self.clean_text(text)
        tokens = word_tokenize(text)
        tokens = self.remove_stopwords(tokens)
        lemmatized_tokens = self.lemmatize_tokens(tokens)
        return " ".join(lemmatized_tokens), lemmatized_tokens

    def split_into_sentences(self, text):
        """
        Splits the input text into sentences using Spacy.

        Parameters:
        - text (str): The text to be split into sentences.

        Returns:
        - list of str: The sentences extracted from the text.
        """
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    def load_and_preprocess_files(self):
        """
        Loads and preprocesses text files from the specified directory.

        Returns:
        - tuple: A tuple containing lists of original texts, filenames, preprocessed texts, and lists of tokens.
        """
        original_texts = []
        filenames = []
        preprocessed_texts = []
        token_lists = []

        for filename in os.listdir(self.directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    original_texts.append(text)
                    filenames.append(filename)
                    preprocessed_text, tokens = self.preprocess_text(text)
                    preprocessed_texts.append(preprocessed_text)
                    token_lists.append(tokens)

        return original_texts, filenames, preprocessed_texts, token_lists