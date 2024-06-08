import numpy as np
from app.model.preprocessor import Preprocessor

class Vectorizer:
    """
    A class to vectorize text data.
    
    Attributes:
        preprocessor (Preprocessor): An instance of the Preprocessor class for text preprocessing.
    """
    
    def __init__(self):
        """Initializes the Vectorizer with a Preprocessor instance."""
        self.preprocessor = Preprocessor()

    def get_sentence_vector(self, text, model):
        """
        Converts a sentence into a vector using a given word embedding model.
        
        Args:
            text (str): The text to be vectorized.
            model: The word embedding model to use for vectorization.
            
        Returns:
            numpy.ndarray: The vector representation of the input text. If the text
            cannot be vectorized (e.g., no known words), returns a zero vector of
            the same size as the model's vector size.
        """
        tokens = self.preprocessor.preprocess_text(text)[1]
        word_vectors = [model.wv[word] for word in tokens if word in model.wv]
        if not word_vectors:  
            return np.zeros(model.vector_size)
        return np.mean(word_vectors, axis=0)