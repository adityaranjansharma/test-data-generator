# Mock Data Generator API (Scaled & en_GB Focused)

A high-performance mock data generation API optimized for the **UK (en_GB) locale** and massive scale (**10 million unique records**).

## Features
- **Massive Scale**: Capable of generating up to 10M records using **Streaming Responses** to keep memory usage minimal.
- **UK-Centric**: Focused on `en_GB` locale with British names, postcodes, and phone formats.
- **Intelligent Rules**: Uses Gemini (via REST API) to generate British-specific data rules.
- **Deterministic**: Supports random seeding for reproducible large-scale datasets.
- **Fast Performance**: Optimized generation pipeline capable of >1,000 records/second.

## Fast Start

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn faker pydantic python-dotenv requests
   ```

2. **Configure Environment**:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```

3. **Run the API**:
   ```bash
   python app.py
   ```

4. **API Usage**:
   ```json
   POST /api/mock-data
   {
     "count": 10000000,
     "locale": "en_GB",
     "seed": 42
   }
   ```


## Project Structure
- `app.py`: FastAPI controller and routing.
- `llm_rules.py`: Gemini REST API integration.
- `generator.py`: Faker-based data production.
- `models.py`: Pydantic data schemas.
- `cache.py`: Rule caching logic.
