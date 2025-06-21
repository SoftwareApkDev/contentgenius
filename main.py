"""
This file is used to run the application "contentgenius".
Author: SoftwareApkDev
"""


import argparse
from core import (
    pdf_analyzer,
    text_analyzer,
    csv_analyzer,
    ppt_analyzer,
    youtube_analyzer,
    web_scraper,
    chat_analyzer,
    code_analyzer,
    package_analyzer,
    mp3_analyzer
)


# Creating main function used to run the application.

def main():
    parser = argparse.ArgumentParser(
        description="📘 contentgenius - AI-powered content analysis tool"
    )
    parser.add_argument("mode", choices=[
        "analyze-pdf", "analyze-text", "analyze-csv", "analyze-ppt",
        "analyze-youtube", "analyze-web", "analyze-chat",
        "analyze-code", "analyze-package", "analyze-mp3"
    ], help="Type of content to analyze")
    parser.add_argument("--input", help="Path to file or URL (depending on mode)")
    parser.add_argument("--prompt", help="Custom prompt/question for LLM")
    args = parser.parse_args()

    # Dispatch to the correct analyzer
    if args.mode == "analyze-pdf":
        result = pdf_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-text":
        result = text_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-csv":
        result = csv_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-ppt":
        result = ppt_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-youtube":
        result = youtube_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-web":
        result = web_scraper.analyze(args.input, args.prompt)
    elif args.mode == "analyze-chat":
        result = chat_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-code":
        result = code_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-package":
        result = package_analyzer.analyze(args.input, args.prompt)
    elif args.mode == "analyze-mp3":
        result = mp3_analyzer.analyze(args.input, args.prompt)
    else:
        raise ValueError("Unsupported mode.")

    print("🧠 Analysis Result:")
    print(result)


if __name__ == "__main__":
    main()
