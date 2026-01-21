import math

def calculate_pool_sizes(count: int) -> dict:
    """
    Calculate optimal pool sizes for generating 'count' unique records.
    
    Strategy:
    - Names: Use sqrt(count) for both first and last names to get count combinations
    - Addresses: Use combinatorics for efficiency (smaller pools, high variety)
    """
    # Names need sqrt(count) each for count unique combinations
    name_pool_size = math.ceil(math.sqrt(count))
    
    # Address pools use combinatorics
    # With 100 streets × 100 cities × 20 counties × 50 postcodes × 10k house numbers
    # = 100,000,000+ unique addresses
    
    # For small counts, scale down proportionally
    if count <= 1000:
        street_pool = 10
        city_pool = 10
        county_pool = 5
        postcode_pool = 5
    elif count <= 10000:
        street_pool = 20
        city_pool = 20
        county_pool = 10
        postcode_pool = 10
    elif count <= 100000:
        street_pool = 50
        city_pool = 50
        county_pool = 15
        postcode_pool = 15
    elif count <= 1000000:
        street_pool = 100
        city_pool = 100
        county_pool = 20
        postcode_pool = 20
    else:  # 10M+
        street_pool = 100
        city_pool = 100
        county_pool = 20
        postcode_pool = 50
    
    return {
        "firstNames": name_pool_size,
        "lastNames": name_pool_size,
        "streets": street_pool,
        "cities": city_pool,
        "counties": county_pool,
        "postcodeAreas": postcode_pool
    }
