import chromadb

client = chromadb.PersistentClient(path="/app/chroma_db")

collection = client.get_or_create_collection(name="documents")