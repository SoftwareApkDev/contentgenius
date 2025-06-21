import os
from PyPDF2 import PdfReader
from llm.prompt_builder import generate_response


def extract_text_from_pdf(pdf_path: str):
    """
    Extracts all text from a PDF file.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    full_text = []

    for page in reader.pages:
        try:
            text = page.extract_text()
            if text:
                full_text.append(text)
        except Exception as e:
            print(f"⚠️ Failed to extract text from page: {e}")

    return "\n".join(full_text)


def build_prompt(content: str, question: str):
    """
    Builds the LLM prompt using user question.
    """
    return f"Given the following PDF content, answer this:\n{question}\n\n---\n\n{content}"


def analyze(pdf_path: str, question: str):
    """
    Main analysis function for PDF files.
    """
    print(f"📄 Reading PDF: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text.strip():
        return "❌ No readable text found in the PDF."

    prompt = build_prompt(raw_text[:5000], question)  # Limit to first 5000 chars
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
