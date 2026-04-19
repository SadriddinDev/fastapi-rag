import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(persist_directory="/app/chroma_db")
)

collection = client.get_or_create_collection(name="documents")