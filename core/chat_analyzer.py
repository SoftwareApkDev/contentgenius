import os
import json

from llm.prompt_builder import generate_response


def load_chat_text(chat_path: str):
    """
    Load chat log from a .txt or .json file.
    """
    if not os.path.exists(chat_path):
        raise FileNotFoundError(f"❌ File not found: {chat_path}")

    if chat_path.endswith(".json"):
        with open(chat_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    # WhatsApp-like JSON structure
                    return "\n".join(f"{msg['sender']}: {msg['text']}" for msg in data if 'sender' in msg and 'text' in msg)
                elif isinstance(data, dict) and "messages" in data:
                    return "\n".join(f"{m['from']}: {m['text']}" for m in data["messages"] if 'from' in m and 'text' in m)
                else:
                    return json.dumps(data, indent=2)  # Fallback
            except Exception as e:
                raise RuntimeError(f"❌ Failed to parse JSON: {e}")
    elif chat_path.endswith(".txt"):
        with open(chat_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("❌ Unsupported file format. Use .txt or .json")


def build_prompt(chat_text: str, question: str):
    """
    Constructs an LLM-friendly prompt from chat content.
    """
    return f"{question}\n\nChat log:\n\n{chat_text}"


def analyze(chat_path: str, question: str):
    """
    Main function for chat analysis.
    """
    print(f"💬 Reading chat log: {chat_path}")
    chat_text = load_chat_text(chat_path)

    if not chat_text.strip():
        return "❌ No readable chat content found."

    prompt = build_prompt(chat_text[:5000], question)
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
