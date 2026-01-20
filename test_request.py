import requests
import json

url = "http://127.0.0.1:8000/api/mock-data"
payload = {
    "count": 500,
    "locale": "en_US",
    "seed": 123,
    "email_domain": "testcorp.com"
}


try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully generated {data['count']} records.")
        print("\nFirst 3 records:")
        print(json.dumps(data["data"][:3], indent=2))
        
        # Verify domain
        all_domains_correct = all("@testcorp.com" in user["email"] for user in data["data"])
        print(f"\nAll email domains correct: {all_domains_correct}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Connection failed: {e}")
