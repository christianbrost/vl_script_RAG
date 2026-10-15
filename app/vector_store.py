import chromadb
from app.chunking import Chunk

_COLLECTION_NAME = "documents"
_client = chromadb.HttpClient(host="chroma", port=8000)
_collection = _client.get_or_create_collection(_COLLECTION_NAME)


def add_chunks(chunks: list[Chunk]) -> None:
    _collection.add(
        ids=[f"{c.source}-{c.page}-{c.chunk_index}" for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "page": c.page} for c in chunks],
    )


def query_similar(question: str, n_results: int = 4) -> dict:
    return _collection.query(query_texts=[question], n_results=n_results)
