import os
from llm.prompt_builder import generate_response


def find_common_files(package_path: str):
    """
    Scans for common package metadata and doc files.
    """
    files_of_interest = []
    common_files = [
        "README.md", "README.txt", "README.rst",
        "setup.py", "pyproject.toml", "package.json",
        "requirements.txt", "environment.yml",
        "composer.json", "Cargo.toml", "Makefile"
    ]

    for root, _, files in os.walk(package_path):
        for file in files:
            if file in common_files:
                files_of_interest.append(os.path.join(root, file))

    return files_of_interest


def read_file_contents(file_paths: list, limit_chars=5000) -> str:
    """
    Reads and concatenates content from multiple files up to a limit.
    """
    combined = ""
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                contents = f.read()
                combined += f"\n--- {os.path.basename(path)} ---\n{contents}\n"
                if len(combined) >= limit_chars:
                    break
        except Exception as e:
            print(f"⚠️ Could not read {path}: {e}")

    return combined[:limit_chars]


def build_prompt(package_data: str, question: str):
    """
    Builds the LLM prompt using collected package data.
    """
    return f"{question}\n\n{package_data}"


def analyze(package_path: str, question: str):
    """
    Main analysis function for software packages.
    """
    if not os.path.isdir(package_path):
        raise NotADirectoryError(f"❌ Not a valid directory: {package_path}")

    print(f"📦 Analyzing package at: {package_path}")
    files = find_common_files(package_path)

    if not files:
        return "❌ No recognizable metadata or documentation files found."

    package_data = read_file_contents(files)
    prompt = build_prompt(package_data, question)

    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
