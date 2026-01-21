import json
import os
from google import genai
from dotenv import load_dotenv
from pool_calculator import calculate_pool_sizes

load_dotenv()

# Initialize Gemini client (automatically picks up GEMINI_API_KEY from environment)
client = genai.Client()

def get_data_pools(locale: str, email_domain: str, count: int) -> dict:
    """
    Fetch all required data pools from Gemini in ONE call using the official SDK.
    
    Pools include:
    - First names and last names (for unique name combinations)
    - Street names, cities, counties, postcode areas (for unique addresses)
    """
    # Calculate optimal pool sizes
    sizes = calculate_pool_sizes(count)
    
    prompt = f"""
You are a test data architect specializing in UK (en_GB) mock data.

Generate mock data pools as JSON for generating {count} unique UK records.

Required pools (return as JSON object):
{{
  "firstNames": [array of {sizes['firstNames']} diverse British first names],
  "lastNames": [array of {sizes['lastNames']} diverse British surnames],
  "streetNames": [array of {sizes['streets']} UK street names WITHOUT house numbers, e.g. "High Street", "Church Road"],
  "cities": [array of {sizes['cities']} UK cities],
  "counties": [array of {sizes['counties']} UK counties],
  "postcodeAreas": [array of {sizes['postcodeAreas']} UK postcode area codes like "SW", "M", "B", "NW"],
  "emailPattern": "{'{'}firstName{'}'}.{'{'}lastName{'}'}.{'{'}index{'}'}@{email_domain}",
  "phonePattern": "07### ######"
}}

Critical requirements:
- All arrays must contain UNIQUE values only
- Street names should be realistic UK street types
- Postcode areas should be real UK area codes
- Return ONLY valid JSON, no markdown blocks
- No explanations or additional text
"""

    try:
        # Use the new SDK with gemini-2.0-flash-lite model
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        
        # Extract text from response (response.text is a property, not a method)
        text_content = str(response.text).strip()
        
        # Clean markdown if present
        if text_content.startswith("```json"):
            text_content = text_content[len("```json"):].rsplit("```", 1)[0].strip()
        elif text_content.startswith("```"):
            text_content = text_content[len("```"):].rsplit("```", 1)[0].strip()

        pools = json.loads(text_content)
       
        # Validate we got all required pools
        required_keys = ["firstNames", "lastNames", "streetNames", "cities", "counties", "postcodeAreas"]
        for key in required_keys:
            if key not in pools or not isinstance(pools[key], list):
                raise ValueError(f"Missing or invalid pool: {key}")
        
        return pools
        
    except Exception as e:
        raise Exception(f"Failed to fetch pools from Gemini: {str(e)}")

