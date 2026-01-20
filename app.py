from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from models import MockDataRequest
from llm_rules import get_generation_rules
from generator import generate_users_stream
from cache import get_cached_rules, set_cached_rules
import logging
import json
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mock Data Generator API")

def json_streamer(count: int, rules: dict, seed: Optional[int]):
    # Yield the opening JSON
    yield '{"count": ' + str(count) + ', "data": ['
    
    generator = generate_users_stream(count, rules, seed)
    
    for i, user in enumerate(generator):
        # Yield the user object as JSON string
        yield json.dumps(user)
        
        # Add a comma if it's not the last item
        if i < count - 1:
            yield ","
    
    # Yield the closing JSON
    yield "]}"

@app.post("/api/mock-data")
def generate_mock_data(request: MockDataRequest):
    try:
        # Default to en_GB if not specified
        locale = request.locale or "en_GB"
        cache_key = f"{locale}:{request.email_domain}"

        rules = get_cached_rules(cache_key)

        if not rules:
            logger.info(f"Cache miss for {cache_key}. Fetching rules from Gemini...")
            rules = get_generation_rules(
                locale=locale,
                email_domain=request.email_domain
            )
            set_cached_rules(cache_key, rules)
        else:
            logger.info(f"Cache hit for {cache_key}.")

        return StreamingResponse(
            json_streamer(request.count, rules, request.seed),
            media_type="application/json"
        )
        
    except Exception as e:
        logger.error(f"Error generating mock data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
