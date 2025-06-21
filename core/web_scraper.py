import requests
from bs4 import BeautifulSoup
from llm.prompt_builder import generate_response


def fetch_webpage(url: str):
    """
    Downloads and extracts the main content from a webpage.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; contentgenius-bot/1.0)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"❌ Failed to fetch webpage: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Get clean text
    body = soup.get_text(separator="\n", strip=True)
    lines = [line for line in body.splitlines() if line.strip()]
    return "\n".join(lines)


def build_prompt(web_text: str, question: str):
    """
    Constructs an LLM-friendly prompt.
    """
    return f"{question}\n\nWebpage content:\n\n{web_text}"


def analyze(url: str, question: str):
    """
    Scrapes and analyzes a webpage with LLM assistance.
    """
    print(f"🌐 Scraping URL: {url}")
    text = fetch_webpage(url)

    if not text.strip():
        return "❌ No readable text found on the page."

    prompt = build_prompt(text[:5000], question)  # Limit input size
    print("🧠 Sending to LLM...")
    response = generate_response(prompt)
    return response
