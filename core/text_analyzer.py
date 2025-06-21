import os
from typing import TextIO
from llm.prompt_builder import generate_response


def analyze(file_path: str, question: str) -> str:
    text_file: TextIO or None = None
    try:
        with open(file_path):
            text_file = open(file_path)
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"Error reading file: {e}"

    if text_file is None:
        return "Error: Unable to open file."

    text: str = text_file.read()
    full_prompt = f"""
        {question}

        Here is the content of the file '{os.path.basename(file_path)}':
        ---
        {text}
        ---
        """

    print(f"📄 Analyzing '{file_path}'... (this may take a moment)")
    response = generate_response(full_prompt)
    return response
