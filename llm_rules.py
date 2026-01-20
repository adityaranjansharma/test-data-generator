import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Gemini REST API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model_name = "gemini-1.5-flash"
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"

def get_generation_rules(locale: str, email_domain: str) -> dict:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not set. Please provide a valid API key in the .env file.")

    prompt = f"""
You are a test data architect.

Generate mock data generation rules as JSON only for the locale: {locale}.

Rules must include:
- firstNamePool (10–20 common names for locale {locale})
- lastNamePool
- emailPattern (must use domain {email_domain})
- phonePattern
- allowedStates (if applicable)
- country

Constraints:
- Output valid JSON only
- No markdown
- No explanation
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 800,
            "responseMimeType": "application/json"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Gemini API Error ({response.status_code}): {response.text}")

    try:
        data = response.json()
        # Navigate the response structure: candidates[0].content.parts[0].text
        text_content = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Some versions might return markdown code blocks even with responseMimeType
        if text_content.startswith("```json"):
            text_content = text_content[len("```json"):].rsplit("```", 1)[0].strip()
        elif text_content.startswith("```"):
            text_content = text_content[len("```"):].rsplit("```", 1)[0].strip()

        return json.loads(text_content)
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise Exception(f"Failed to parse Gemini response: {str(e)}\nRaw text: {text_content if 'text_content' in locals() else 'N/A'}")

