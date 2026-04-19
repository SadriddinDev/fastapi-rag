from fastapi import APIRouter, UploadFile, File, Depends
import shutil
from app.rag.retrieval import retrieve
from app.rag.llm import ask_llm
from app.rag.ingestion import ingest_pdf
from app.core.deps import get_current_user

router = APIRouter(tags=["RAG"], dependencies=[Depends(get_current_user)])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_pdf(file_path)

    return {"status": "uploaded and indexed"}


@router.post("/ask")
async def ask(question: str):
    chunks = retrieve(question)
    context = "\n".join(chunks)

    answer = ask_llm(context, question)

    return {"answer": answer}