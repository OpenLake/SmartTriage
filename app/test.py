from app.ml.embedder import Embedder
from app.db.vector import search_similar


embedder = Embedder()


text = "Cannot login into application"


embedding = embedder.generate_embedding(text)


result = search_similar(
    embedding
)


print(result)