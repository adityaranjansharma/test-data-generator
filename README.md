# Mock Data Generator API (Gemini & Faker)

A high-performance mock data generation API that uses **Gemini 1.5 Flash** to intelligently define generation rules and **Faker** for high-volume, deterministic data production.

## Features
- **Intelligent Rules**: Uses Gemini (via REST API) to generate locale-specific data rules (names, patterns, states, etc.).
- **Bulk Generation**: Efficiently produces thousands of records based on the rules.
- **Caching**: In-memory rule caching to minimize LLM API calls and cost.
- **Deterministic**: Supports random seeding for reproducible data sets.
- **Python 3.8+ Compatible**: Uses direct REST calls to bypass SDK version constraints.

## Fast Start

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn faker pydantic python-dotenv requests
   ```

2. **Configure Environment**:
   Create a `.env` file based on the template:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```

3. **Run the API**:
   ```bash
   python app.py
   ```
   Or with reload:
   ```bash
   uvicorn app:app --reload
   ```

4. **API Usage**:
   Send a `POST` request to `/api/mock-data`:
   ```json
   {
     "count": 1000,
     "locale": "en_GB",
     "seed": 42,
     "email_domain": "example.com"
   }
   ```

## Project Structure
- `app.py`: FastAPI controller and routing.
- `llm_rules.py`: Gemini REST API integration.
- `generator.py`: Faker-based data production.
- `models.py`: Pydantic data schemas.
- `cache.py`: Rule caching logic.
