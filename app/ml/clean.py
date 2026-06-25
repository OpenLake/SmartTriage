from app.ml.embedder import Embedder

embedder = Embedder()

def clean_issue(issue):
    text = ""

    if issue["title"]:
        text += issue["title"]

    if issue["body"]:
        text += "\n" + issue["body"]

    vector = embedder.generate_embedding(text)
    
    return {
        "id": issue["id"],
        "text": text.strip(),
        "url": issue["url"],
        "state": issue["state"],
        "vector": vector
    }