from sentence_transformers import SentenceTransformer

class Embedder:
    _model = None

    def __init__(self):
        if Embedder._model is None:
            Embedder._model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text):
        embedding = Embedder._model.encode(text)
        return embedding.tolist()