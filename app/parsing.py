from pypdf import PdfReader
from io import BytesIO


def extract_text_per_page(pdf_bytes: bytes) -> list[str]:
    """input: pdf - output; extracted text"""
    reader = PdfReader(BytesIO(pdf_bytes))
    return [page.extract_text() or "" for page in reader.pages]
