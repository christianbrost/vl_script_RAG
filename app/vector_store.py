import chromadb
from app.chunking import Chunk

_COLLECTION_NAME = "documents"

# Verbindet sich mit dem Chroma-Service aus docker-compose.yml (Service-Name "chroma").
_client = chromadb.HttpClient(host="chroma", port=8000)
_collection = _client.get_or_create_collection(_COLLECTION_NAME)


def add_chunks(chunks: list[Chunk]) -> None:
    """Speichert Chunks inkl. Metadaten im Vector Store.

    Chroma übernimmt das Embedding automatisch (Default Embedding-Funktion),
    du musst hier keine Embeddings selbst berechnen.
    """
    _collection.add(
        ids=[f"{c.source}-{c.page}-{c.chunk_index}" for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "page": c.page} for c in chunks],
    )


def query_similar(question: str, n_results: int = 4) -> dict:
    """Gibt die ähnlichsten Chunks zu einer Frage zurück (roh von Chroma)."""
    return _collection.query(query_texts=[question], n_results=n_results)
