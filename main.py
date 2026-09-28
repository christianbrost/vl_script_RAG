from fastapi import FastAPI, UploadFile

from app.schemas import QueryRequest, QueryResponse, UploadResponse
from app.parsing import extract_text_per_page
from app.chunking import chunk_document
from app.vector_store import add_chunks
from app.rag_pipeline import retrieve_and_answer

app = FastAPI(title="RAG Service")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile) -> UploadResponse:
    pdf_bytes = await file.read()
    pages = extract_text_per_page(pdf_bytes)
    chunks = chunk_document(pages, source=file.filename)
    add_chunks(chunks)
    return UploadResponse(filename=file.filename, chunks_created=len(chunks))


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    answer, sources = retrieve_and_answer(request.question)
    return QueryResponse(answer=answer, sources=sources)
