from pypdf import PdfReader
from typing import List
import io


# This function extracts text from a PDF file. It reads the PDF file using PdfReader and concatenates the text from all pages into a single string.
def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text
