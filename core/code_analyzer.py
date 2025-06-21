import os
from llm.prompt_builder import generate_response


SUPPORTED_EXTENSIONS: dict = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.rb': 'Ruby',
    '.go': 'Go',
    '.php': 'PHP',
    '.rs': 'Rust',
    '.html': 'HTML',
    '.css': 'CSS'
}


def detect_language(file_path: str):
    _, ext = os.path.splitext(file_path)
    return SUPPORTED_EXTENSIONS.get(ext.lower(), "Unknown")


def read_code(file_path: str):
    """
    Reads the code content from a source file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def build_prompt(code: str, language: str, question: str):
    """
    Constructs a prompt for the LLM with the source code.
    """
    return f"{question}\n\nLanguage: {language}\n\nCode:\n\n{code}"


def analyze(file_path: str, question: str):
    """
    Main function for source code analysis.
    """
    print(f"🧑‍💻 Auditing code file: {file_path}")
    language = detect_language(file_path)
    code = read_code(file_path)

    if not code.strip():
        return "❌ File is empty or contains no readable code."

    prompt = build_prompt(code[:5000], language, question)  # limit to 5000 chars
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
