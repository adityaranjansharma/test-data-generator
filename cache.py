RULE_CACHE = {
    "en_US:testcorp.com": {
        "firstNamePool": ["Alice", "Bob", "Charlie", "Diana", "Edward"],
        "lastNamePool": ["Smith", "Jones", "Williams", "Brown", "Taylor"],
        "emailPattern": "{firstName}.{lastName}.{index}@testcorp.com",
        "phonePattern": "555-####",
        "allowedStates": ["NY", "CA", "TX", "FL", "IL"],
        "country": "USA"
    },
    "en_GB:testcorp.com": {
        "firstNamePool": ["Oliver", "George", "Arthur", "Noah", "Jack"],
        "lastNamePool": ["Smith", "Jones", "Taylor", "Brown", "Williams"],
        "emailPattern": "{firstName}.{lastName}.{index}@testcorp.co.uk",
        "phonePattern": "07### ######",
        "allowedStates": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
        "country": "UK"
    }

}

def get_cached_rules(key):
    return RULE_CACHE.get(key)

def set_cached_rules(key, rules):
    RULE_CACHE[key] = rules

