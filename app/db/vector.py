import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./data/chroma")


collection = client.get_or_create_collection(
    name="github_issues",
    metadata={"hnsw:space": "cosine"}
)


def add_issue(issue_id, text, vector, metadata):
    collection.upsert(
        ids=[str(issue_id)],
        documents=[text],
        embeddings=[vector],
        metadatas=[metadata]
    )


def search_similar_issue(embedding, limit=1):
    results = collection.query(
        query_embeddings=[embedding],
        n_results=limit
    )
    return results