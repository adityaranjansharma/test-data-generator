# Mock Data Generator API

A high-performance, scalable mock data generation API capable of generating **10 million+ unique records** with authentic UK (en_GB) data. It leverages **Gemini 2.0 Flash-Lite** to dynamically generate culturally accurate name and address pools, ensuring diversity and realism.

---

## Key Features

- **Massive Scale**: Generate up to 10 million unique records efficiently using streaming responses.
- **Authentic UK Data**: Full support for `en_GB` locale, including:
  - Realistic UK names (First & Last).
  - Complete UK addresses (Street, City, County, Postcode).
  - Valid UK mobile numbers (`07xxx`).
- **Dynamic LLM Integration**: Uses **Gemini 2.0 Flash-Lite** via the official `google-genai` SDK to fetch optimzed data pools.
- **Smart Caching**: Implements tiered caching to minimize LLM calls. One call populates pools for millions of records.
- **Memory Efficient**: Uses Python generators and streaming to maintain low memory footprint (~10MB) regardless of request size.
- **Deterministic**: Supports seeding for reproducible datasets.

---

## Prerequisites

- **Python 3.9+** (Required for `google-genai` SDK)
- **Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd TestDataGenerator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

## Usage

### Start the Server
```bash
uvicorn app:app --port 8000
```
*(Note: If testing locally with multiple Python versions, ensure you use the python executable where dependencies are installed, e.g., `py -m uvicorn app:app --port 8000`)*

### Generate Data

**Endpoint**: `POST /api/mock-data`

**Payload**:
```json
{
  "count": 1000,
  "locale": "en_GB",
  "seed": 42,
  "email_domain": "testcorp.co.uk"
}
```

**Example Curl**:
```bash
curl -X POST "http://127.0.0.1:8000/api/mock-data" \
  -H "Content-Type: application/json" \
  -d '{"count": 1000, "locale": "en_GB", "seed": 42}'
```

---

## Architecture

### 1. Intelligent Pool Sizing
The system calculates the exact number of unique components needed based on the requested count to ensure uniqueness without over-fetching.

| Records Requested | Component Strategy | LLM Calls |
|-------------------|--------------------|-----------|
| **1,000** | ~32 First × 32 Last names | 1 |
| **10,000** | ~100 First × 100 Last names | 1 |
| **10,000,000** | ~3,162 First × 3,162 Last names | 1 |

### 2. Data Uniqueness & Variety
- **Names**: Combinatorial generation from LLM-fetched name pools (e.g., 3,162 × 3,162 = 10M unique names).
- **Emails**: Guaranteed unique via index injection (`firstname.lastname.123@domain`).
- **Addresses**: Combinatorial generation using LLM-fetched Streets, Cities, Counties, and Postcode Areas to produce over 100M unique valid addresses.

### 3. Caching
Pools are cached by locale, domain, and size tier. Subsequent requests for the same or smaller size use cached data, requiring **zero LLM calls**.

---

## Project Structure

- `app.py`: FastAPI entry point and streaming logic.
- `llm_rules.py`: Handles interaction with Gemini 2.0 Flash-Lite using `google-genai` SDK.
- `pool_calculator.py`: Logic for determining optimal pool sizes.
- `generator.py`: Core logic for combining pools into unique user records.
- `cache.py`: In-memory caching system.
- `models.py`: Pydantic data models.

## Deployment on Render

This application is ready to be deployed on Render.

1.  Create a new **Web Service** on Render connected to this repository.
2.  Render should automatically detect the configuration from `render.yaml`.
3.  **Important**: You must provide the `GEMINI_API_KEY` environment variable in the Render dashboard for the application to function correctly.
    -   Key: `GEMINI_API_KEY`
    -   Value: Your Gemini API key from Google AI Studio.
