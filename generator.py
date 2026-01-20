from typing import Optional
from faker import Faker
import random

def generate_users_stream(count: int, rules: dict, seed: Optional[int]):

    fake = Faker("en_GB")
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    # Pre-fetch pools to avoid dictionary lookups in the loop
    first_names = rules.get("firstNamePool", ["User"])
    last_names = rules.get("lastNamePool", ["Test"])
    email_pattern = rules.get("emailPattern", "{firstName}.{lastName}.{index}@{domain}")
    phone_pattern = rules.get("phonePattern", "07### ######")
    allowed_states = rules.get("allowedStates", ["NA"])
    country = rules.get("country", "United Kingdom")

    for i in range(count):
        # To ensure uniqueness at 10M scale, we use the index 'i' in the email
        # and rely on Faker's entropy for other fields.
        
        first = random.choice(first_names)
        last = random.choice(last_names)

        # The {index} in the pattern is key for 10M unique emails
        email = email_pattern \
            .replace("{firstName}", first.lower()) \
            .replace("{lastName}", last.lower()) \
            .replace("{index}", str(i))

        # Yield a single user dict
        yield {
            "firstName": first,
            "lastName": last,
            "email": email,
            "phone": fake.numerify(phone_pattern),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": random.choice(allowed_states),
                "country": country
            }
        }

