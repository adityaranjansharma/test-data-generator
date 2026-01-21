"""
Example test script for the Mock Data Generator API.
This demonstrates how to request data from the API and validate the response.
"""
import requests
import json

# API Configuration
API_URL = "http://127.0.0.1:8003/api/mock-data"

# Request payload
payload = {
    "count": 500,
    "locale": "en_GB",
    "seed": 42,
    "email_domain": "testcorp.co.uk"
}

print(f"Requesting {payload['count']} records from the API...")
print("="*70)

try:
    response = requests.post(API_URL, json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Successfully generated {data['count']} records\n")
        
        # Display first record
        print("Sample Record:")
        print(json.dumps(data["data"][0], indent=2))
        
        # Validate uniqueness
        emails = [user["email"] for user in data["data"]]
        print(f"\n✓ Unique emails: {len(set(emails))}/{len(emails)}")
        
        # Validate UK address format
        addr = data["data"][0]["address"]
        print(f"\n✓ UK Address Fields:")
        print(f"  - Address Line 1: {addr['addressLine1']}")
        print(f"  - City: {addr['city']}")
        print(f"  - County: {addr['county']}")
        print(f"  - Postcode: {addr['postcode']}")
        
        print("\n" + "="*70)
        print("✓ Test Passed!")
        
    else:
        print(f"✗ Error {response.status_code}: {response.text[:500]}")
        
except Exception as e:
    print(f"✗ Exception: {e}")
