RULE_CACHE = {
    "en_GB:testcorp.co.uk": {
        "firstNamePool": ["Oliver", "George", "Arthur", "Noah", "Jack", "Leo", "Oscar", "Harry", "Archie", "Alfie"],
        "lastNamePool": ["Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson", "Davies", "Robinson", "Wright"],
        "emailPattern": "{firstName}.{lastName}.{index}@testcorp.co.uk",
        "phonePattern": "07### ######",
        "allowedStates": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Sheffield", "Liverpool", "Bristol"],
        "country": "UK"
    }
}


def get_cached_rules(key):
    return RULE_CACHE.get(key)

def set_cached_rules(key, rules):
    RULE_CACHE[key] = rules

