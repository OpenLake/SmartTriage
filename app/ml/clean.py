from app.ml.embedder import Embedder

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder

def clean_issue(issue):
    text = ""

    if issue["title"]:
        text += issue["title"]

    if issue["body"]:
        text += "\n" + issue["body"]

    embedding = get_embedder().generate_embedding(text)
    
    return {
        "id": issue["id"],
        "text": text.strip(),
        "url": issue["url"],
        "state": issue["state"],
        "embedding": embedding
    }