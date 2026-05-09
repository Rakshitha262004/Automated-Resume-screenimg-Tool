"""
extractor.py
Handles text extraction from PDF and DOCX files.
"""

import os
import PyPDF2
import pdfplumber
from docx import Document


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfplumber.
    Falls back to PyPDF2 if pdfplumber fails.
    """
    text = ""
    try:
        # Primary method: pdfplumber (better for complex PDFs)
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        # Fallback method: PyPDF2
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"  [ERROR] Could not read PDF {pdf_path}: {e}")
    return text


def extract_text_from_docx(docx_path):
    """
    Extract text from a DOCX file.
    """
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"  [ERROR] Could not read DOCX {docx_path}: {e}")
    return text


def extract_text_from_txt(txt_path):
    """
    Extract text from a plain .txt file.
    """
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"  [ERROR] Could not read TXT {txt_path}: {e}")
        return ""


def extract_all_resumes(resume_folder):
    """
    Loop through the resumes/ folder and extract text from all files.
    Returns a dict: { filename: extracted_text }
    """
    resume_texts = {}
    supported_formats = (".pdf", ".docx", ".txt")

    if not os.path.exists(resume_folder):
        print(f"  [ERROR] Resume folder not found: {resume_folder}")
        return resume_texts

    files = [f for f in os.listdir(resume_folder)
             if f.lower().endswith(supported_formats)]

    if not files:
        print(f"  [WARNING] No supported resume files found in {resume_folder}")
        return resume_texts

    print(f"\n  Found {len(files)} resume(s) in '{resume_folder}'")

    for filename in files:
        filepath = os.path.join(resume_folder, filename)
        print(f"  Extracting: {filename}")

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(filepath)
        elif filename.lower().endswith(".docx"):
            text = extract_text_from_docx(filepath)
        elif filename.lower().endswith(".txt"):
            text = extract_text_from_txt(filepath)
        else:
            text = ""

        if text.strip():
            resume_texts[filename] = text
        else:
            print(f"  [WARNING] Empty text extracted from {filename}")

    return resume_texts