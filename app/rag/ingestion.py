from pypdf import PdfReader
from app.rag.vectorstore import collection
from app.rag.embeddings import embed_text
import uuid


def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def chunk_text(text: str, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def ingest_pdf(file_path: str):
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = embed_text(chunk)

        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk]
        )