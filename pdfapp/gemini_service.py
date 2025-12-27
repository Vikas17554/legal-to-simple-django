import google.generativeai as genai
import time
import random
import os

# 1. Configure API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


def explain_page(text: str, page_number: int) -> str:
    print(f"🔥 Processing Page {page_number}...")

    if not text or not text.strip():
        return "Is page par koi text nahi hai."

    prompt = f"""
    You are a helpful Indian legal assistant.
    TASK: Read this legal text and explain it in simple Hinglish (Hindi + English mix).
    Keep it short and simple.
    
    LEGAL TEXT:
    {text[:4000]} 
    """

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            print(f"   ✅ Page {page_number} Done!")
            return response.text

        except Exception as e:
            if "429" in str(e):
                wait_time = 5 * (attempt + 1)
                print(f"   ⚠️ Speed limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            return f"Error: {str(e)}"

    return "❌ Error: Could not process page."
