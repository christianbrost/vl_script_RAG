from pypdf import PdfReader
from io import BytesIO


def extract_text_per_page(pdf_bytes: bytes) -> list[str]:
    """Liest ein PDF ein und gibt pro Seite den extrahierten Text zurück.

    Rückgabe: Liste mit einem String pro Seite (Index 0 = Seite 1).
    """
    reader = PdfReader(BytesIO(pdf_bytes))
    return [page.extract_text() or "" for page in reader.pages]
