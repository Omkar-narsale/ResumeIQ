"""
Resume Parser Module
Handles PDF parsing and text extraction
"""

from PyPDF2 import PdfReader
from io import BytesIO


def extract_text(file) -> str:
    """
    Extract all text from uploaded PDF file

    Args:
        file: Uploaded file object from Streamlit

    Returns:
        Extracted text from PDF

    Raises:
        ValueError: If file is not a valid PDF
    """
    try:
        # Read PDF from uploaded file
        pdf_reader = PdfReader(file)

        # Extract text from all pages
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text

        if not text.strip():
            raise ValueError("No text could be extracted from the PDF")

        return text.strip()

    except Exception as e:
        raise ValueError(f"Error parsing PDF: {str(e)}")
