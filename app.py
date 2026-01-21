from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from models import MockDataRequest
from llm_rules import get_data_pools
from generator import generate_users_stream
from cache import get_cached_pools, set_cached_pools, has_sufficient_pools
import logging
import json
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mock Data Generator API - Dynamic LLM Pools")

def json_streamer(count: int, pools: dict, seed: Optional[int]):
    # Yield the opening JSON
    yield '{"count": ' + str(count) + ', "data": ['
    
    generator = generate_users_stream(count, pools, seed)
    
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
        locale = request.locale or "en_GB"
        email_domain = request.email_domain
        count = request.count
        
        logger.info(f"Request: {count} records for {locale}:{email_domain}")
        
        # Check cache
        cached_pools = get_cached_pools(locale, email_domain, count)
        
        if cached_pools and has_sufficient_pools(cached_pools, count):
            logger.info(f"✓ Cache hit - Using existing pools")
            pools = cached_pools
        else:
            logger.info(f"✗ Cache miss - Fetching pools from Gemini for {count} records...")
            pools = get_data_pools(locale, email_domain, count)
            set_cached_pools(locale, email_domain, count, pools)
            
            # Log pool sizes for debugging
            logger.info(f"Fetched pools: {len(pools.get('firstNames', []))} first names, "
                       f"{len(pools.get('lastNames', []))} last names, "
                       f"{len(pools.get('streetNames', []))} streets, "
                       f"{len(pools.get('cities', []))} cities")

        return StreamingResponse(
            json_streamer(count, pools, request.seed),
            media_type="application/json"
        )
        
    except Exception as e:
        logger.error(f"Error generating mock data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
