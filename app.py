from fastapi import FastAPI, HTTPException
from models import MockDataRequest, MockDataResponse
from llm_rules import get_generation_rules
from generator import generate_users
from cache import get_cached_rules, set_cached_rules
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mock Data Generator API")

@app.post("/api/mock-data", response_model=MockDataResponse)
def generate_mock_data(request: MockDataRequest):
    try:
        cache_key = f"{request.locale}:{request.email_domain}"

        rules = get_cached_rules(cache_key)

        if not rules:
            logger.info(f"Cache miss for {cache_key}. Fetching rules from Gemini...")
            rules = get_generation_rules(
                locale=request.locale,
                email_domain=request.email_domain
            )
            set_cached_rules(cache_key, rules)
        else:
            logger.info(f"Cache hit for {cache_key}.")

        data = generate_users(
            count=request.count,
            rules=rules,
            seed=request.seed
        )

        return {
            "count": request.count,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error generating mock data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
