import pdfplumber
import io
from typing import Tuple

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file bytes"""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def extract_text_and_filename(file_bytes: bytes, filename: str) -> Tuple[str, str]:
    """Extract text from PDF and return with filename"""
    text = extract_text_from_pdf(file_bytes)
    if not text or len(text.strip()) == 0:
        raise ValueError("PDF appears to be empty or contains no extractable text")
    return text, filename
