from typing import Optional
import random

def generate_users_stream(count: int, pools: dict, seed: Optional[int]):
    """
    Generate user records using LLM-provided pools.
    
    Uses combinatorics to create unique records:
    - Names: Random selection from pools with index for uniqueness
    - Addresses: Deterministic selection based on index for maximum variety
    """
    if seed is not None:
        random.seed(seed)

    # Pre-fetch pools
    first_names = pools.get("firstNames", ["User"])
    last_names = pools.get("lastNames", ["Test"])
    street_names = pools.get("streetNames", ["High Street"])
    cities = pools.get("cities", ["London"])
    counties = pools.get("counties", ["Greater London"])
    postcode_areas = pools.get("postcodeAreas", ["SW"])
    
    email_pattern = pools.get("emailPattern", "{firstName}.{lastName}.{index}@domain.co.uk")
    phone_pattern = pools.get("phonePattern", "07### ######")

    for i in range(count):
        # Names: Random selection for variety
        first = random.choice(first_names)
        last = random.choice(last_names)

        # Email: Index ensures uniqueness
        email = email_pattern \
            .replace("{firstName}", first.lower()) \
            .replace("{lastName}", last.lower()) \
            .replace("{index}", str(i))

        # Address: Combinatorial selection for maximum variety
        street_idx = i % len(street_names)
        city_idx = (i // len(street_names)) % len(cities)
        county_idx = (i // (len(street_names) * len(cities))) % len(counties)
        postcode_idx = (i // 1000) % len(postcode_areas)
        
        # House number from index
        house_number = (i % 10000) + 1
        
        # Address Line 2: Flat number (every 5th address)
        address_line2 = f"Flat {(i % 100) + 1}" if i % 5 == 0 else ""
        
        # Generate UK postcode (e.g., "SW1A 2AA")
        postcode_area = postcode_areas[postcode_idx]
        postcode_district = (i % 9) + 1
        postcode_sector = chr(65 + (i % 26))
        postcode_unit = f"{(i % 9) + 1}{chr(65 + ((i // 26) % 26))}{chr(65 + ((i //676) % 26))}"
        postcode = f"{postcode_area}{postcode_district}{postcode_sector} {postcode_unit}"

        # Generate phone number
        phone = ""
        for char in phone_pattern:
            if char == '#':
                phone += str(random.randint(0, 9))
            else:
                phone += char

        # Yield a single user dict
        yield {
            "firstName": first,
            "lastName": last,
            "email": email,
            "phone": phone,
            "address": {
                "addressLine1": f"{house_number} {street_names[street_idx]}",
                "addressLine2": address_line2,
                "city": cities[city_idx],
                "county": counties[county_idx],
                "postcode": postcode,
                "country": "United Kingdom"
            }
        }
