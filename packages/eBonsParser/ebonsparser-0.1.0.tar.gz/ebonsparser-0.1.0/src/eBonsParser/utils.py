from typing import Union
from io import BytesIO
import pdfplumber
import logging
import re

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_text_from_pdf(input: Union[str, bytes]) -> str:
    """
    Extracts raw text from a PDF file, whether it's from disk or memory.
    """
    if isinstance(input, str):
        with pdfplumber.open(input) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif isinstance(input, bytes):
        with pdfplumber.open(BytesIO(input)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        raise TypeError("Input must be a file path (str) or raw bytes (bytes)")