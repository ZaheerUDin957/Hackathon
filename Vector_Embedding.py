# Vector_Embedding.py
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class TextEmbedder:
    def __init__(self):
        # Define the available models
        self.models = {
            "BAAI/bge-small-en-v1.5": SentenceTransformer("BAAI/bge-small-en-v1.5"),
            "intfloat/e5-large-v2": SentenceTransformer("intfloat/e5-large-v2"),
        }

    def embed_text(self, text_parts, model_name):
        model = self.models[model_name]
        
        # Ensure text_parts is a list of strings
        if not isinstance(text_parts, list):
            text_parts = [text_parts]
        
        embeddings = model.encode(text_parts)
        return embeddings

    def calculate_cosine_similarity(self, embedding1, embedding2):
        return cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))[0, 0]
