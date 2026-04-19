from app.rag.vectorstore import collection
from app.rag.embeddings import embed_text


def retrieve(query: str, k=3):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]