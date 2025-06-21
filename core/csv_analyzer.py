import pandas as pd
from llm.prompt_builder import generate_response


def load_csv(csv_path: str, max_rows=30):
    """
    Loads a CSV file and returns a truncated DataFrame and its string representation.
    """
    try:
        df = pd.read_csv(csv_path)
        display_df = df.head(max_rows)  # Show only the first N rows
        return df, display_df.to_markdown(index=False)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to read CSV file: {e}")


def build_prompt(csv_markdown: str, question: str):
    """
    Builds the LLM prompt using user question.
    """
    return f"{question}\n\nCSV preview:\n\n{csv_markdown}"


def analyze(csv_path: str, question: str):
    """
    Main analysis function for CSV files.
    """
    print(f"📊 Reading CSV: {csv_path}")
    _, csv_text = load_csv(csv_path)

    prompt = build_prompt(csv_text, question)
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
