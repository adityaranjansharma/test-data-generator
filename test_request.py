import requests
import json
import time

url = "http://127.0.0.1:8001/api/mock-data"

# Request 10,000 for a quick but substantial test
target_count = 10000
payload = {
    "count": target_count,
    "locale": "en_GB",
    "seed": 42,
    "email_domain": "testcorp.co.uk"
}

print(f"Requesting {target_count} records from {url}...")
start_time = time.time()

try:
    # Use stream=True to handle the StreamingResponse
    with requests.post(url, json=payload, stream=True) as response:
        if response.status_code == 200:
            print("Connected. Receiving stream...")
            
            # Simple validation: just read a few chunks to see the start
            chunk_count = 0
            bytes_received = 0
            for chunk in response.iter_content(chunk_size=1024):
                if chunk_count == 0:
                    print(f"First chunk: {chunk[:100].decode(errors='ignore')}...")
                bytes_received += len(chunk)
                chunk_count += 1
            
            duration = time.time() - start_time
            print(f"\nStream complete.")
            print(f"Total bytes received: {bytes_received}")
            print(f"Time taken: {duration:.2f} seconds")
            print(f"Approx speed: {target_count/duration:.2f} records/sec")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
except Exception as e:
    print(f"Connection failed: {e}")
