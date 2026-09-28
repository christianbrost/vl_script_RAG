class Chunk:
    """Ein Textabschnitt mit Metadaten, bereit für den Vector Store."""

    def __init__(self, text: str, source: str, page: int, chunk_index: int):
        self.text = text
        self.source = source
        self.page = page
        self.chunk_index = chunk_index


_CHUNK_SIZE = 800
_CHUNK_OVERLAP = 150
_MIN_CHUNK_LENGTH = 50


def chunk_document(pages: list[str], source: str) -> list[Chunk]:
    """Zerlegt die Seiten eines Dokuments in durchsuchbare Chunks.

    Chunkt jede Seite einzeln in Stücke von _CHUNK_SIZE Zeichen mit
    _CHUNK_OVERLAP Überlappung, damit an Chunk-Grenzen kein Kontext
    verloren geht. Zu kurze/leere Fragmente werden verworfen.
    """
    chunks: list[Chunk] = []

    for page_number, page_text in enumerate(pages, start=1):
        text = page_text.strip()
        if not text:
            continue

        start = 0
        while start < len(text):
            end = start + _CHUNK_SIZE
            piece = text[start:end].strip()

            if len(piece) >= _MIN_CHUNK_LENGTH:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=source,
                        page=page_number,
                        chunk_index=len(chunks),
                    )
                )

            if end >= len(text):
                break
            start = end - _CHUNK_OVERLAP

    return chunks
