# Connect to Google Gemini AI


import os
import google.generativeai as genai

from dotenv import load_dotenv


def initiate_gemini_model() -> genai.GenerativeModel:
    load_dotenv()
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    gemini_model_name = "gemini-2.5-flash"
    return genai.GenerativeModel(gemini_model_name)


def generate_response(prompt: str) -> str:
    model = initiate_gemini_model()
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return str(convo.last.text)
