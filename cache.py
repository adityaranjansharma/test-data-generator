from pool_calculator import calculate_pool_sizes

# Pool cache structure: stores all pools for each locale/domain/count tier
POOL_CACHE = {}

def get_cache_key(locale: str, domain: str, count: int) -> str:
    """Generate cache key based on locale, domain, and count tier."""
    # Tier the count to cache levels (1k, 10k, 100k, 1M, 10M)
    if count <= 1000:
        tier = "1k"
    elif count <= 10000:
        tier = "10k"
    elif count <= 100000:
        tier = "100k"
    elif count <= 1000000:
        tier = "1M"
    else:
        tier = "10M"
    
    return f"{locale}:{domain}:{tier}"

def get_cached_pools(locale: str, domain: str, count: int):
    """Get cached pools if available."""
    key = get_cache_key(locale, domain, count)
    return POOL_CACHE.get(key)

def set_cached_pools(locale: str, domain: str, count: int, pools: dict):
    """Cache pools for future use."""
    key = get_cache_key(locale, domain, count)
    POOL_CACHE[key] = pools

def has_sufficient_pools(cached_pools: dict, required_count: int) -> bool:
    """Check if cached pools are sufficient for the required count."""
    if not cached_pools:
        return False
    
    required_sizes = calculate_pool_sizes(required_count)
    
    return (
        len(cached_pools.get("firstNames", [])) >= required_sizes["firstNames"] and
        len(cached_pools.get("lastNames", [])) >= required_sizes["lastNames"] and
        len(cached_pools.get("streetNames", [])) >= required_sizes["streets"] and
        len(cached_pools.get("cities", [])) >= required_sizes["cities"] and
        len(cached_pools.get("counties", [])) >= required_sizes["counties"] and
        len(cached_pools.get("postcodeAreas", [])) >= required_sizes["postcodeAreas"]
    )
