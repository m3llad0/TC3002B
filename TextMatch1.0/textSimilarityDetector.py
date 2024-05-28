import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textPreprocessor import TextPreprocessor

class TextSimilarityDetector:
    """
    A class to detect text similarity using TF-IDF and cosine similarity.

    Attributes:
        preprocessor (TextPreprocessor): TextPreprocessor instance for text preprocessing.
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
        self.preprocessor = TextPreprocessor()
        self.directory = directory
        self.texts = []
        self.file_names = []
        self._load_and_preprocess_texts()
        self._vectorize_texts()

    def _load_and_preprocess_texts(self):
        """
        Loads and preprocesses all text files in the specified directory.
        """
        for filename in os.listdir(self.directory):
            if filename.endswith('.txt'):
                with open(os.path.join(self.directory, filename), 'r', encoding='utf-8') as file:
                    text = file.read()
                    preprocessed_text = self.preprocessor.preprocess_text(text)
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
        preprocessed_input_text = self.preprocessor.preprocess_text(input_text)
        input_vector = self.tfidf_vectorizer.transform([preprocessed_input_text])
        cosine_similarities = cosine_similarity(input_vector, self.X).flatten()

        similar_texts_found = False
        for i, similarity in enumerate(cosine_similarities):
            if similarity > similarity_threshold:
                print(f"Archivo: {self.file_names[i]}, Similitud: {similarity:.4f}")
                similar_texts_found = True

        if not similar_texts_found:
            print("No se encontraron textos similares")