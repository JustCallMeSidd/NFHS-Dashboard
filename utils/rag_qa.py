import requests
import json
import os

# Get the API key from an environment variable
GEMINI_API_KEY = "AIzaSyC7vLGBt7Sv3rHAyZdl3QgZFiOheVFXjJQ"

def generate_answer(question, context_text, few_shot_path="prompts/nfhs_few_shot_prompt.txt"):
    """
    RAG-powered answer using Gemini API
    """
    if not GEMINI_API_KEY:
        return "Error: Need payment for Chat or API key not set."

    # Load few-shot prompt examples
    try:
        with open(few_shot_path, "r") as f:
            few_shot_prompt = f.read()
    except FileNotFoundError:
        few_shot_prompt = ""  # fallback if the file is missing

    prompt = f"""
You are an expert on Indian health survey data (NFHS).
Few-shot examples: {few_shot_prompt}
Context: {context_text}
Question: {question}
Answer in a clear, concise, factual way.
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {"contents":[{"parts":[{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['parts'][0]['text']
        elif response.status_code == 403:
            return "Error: Need payment for Chat or API key is invalid."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

