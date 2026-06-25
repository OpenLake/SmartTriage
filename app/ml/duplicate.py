from app.ml.embedder import Embedder
from app.db.vector import search_similar_issue
from app.config import SIMILARITY_THRESHOLD

embedder = Embedder()

def detect_duplicate(issue_text):

    embedding = embedder.generate_embedding(issue_text)

    result = search_similar_issue(embedding)


    if not result["distances"][0]:
        return None

    distance = result["distances"][0][0]
    similarity = max(0, 1 - distance)

    if similarity >= SIMILARITY_THRESHOLD:
        return {
            "duplicate": True,
            "similarity": similarity,
            "issue": result["metadatas"][0][0]
        }

    return {
        "duplicate": False,
        "similarity": similarity
    }