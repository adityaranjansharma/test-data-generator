from typing import Optional
from faker import Faker
import random

def generate_users(count: int, rules: dict, seed: Optional[int]):
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    users = []

    for i in range(count):
        # Fallback names if pools are missing or empty
        first_names = rules.get("firstNamePool", ["User"])
        last_names = rules.get("lastNamePool", ["Test"])
        
        first = random.choice(first_names)
        last = random.choice(last_names)

        email_pattern = rules.get("emailPattern", "{firstName}.{lastName}_{index}@{domain}")
        # Assuming emailPattern uses {firstName}, {lastName}, {index}
        email = email_pattern \
            .replace("{firstName}", first.lower()) \
            .replace("{lastName}", last.lower()) \
            .replace("{index}", str(i))

        user = {
            "firstName": first,
            "lastName": last,
            "email": email,
            "phone": fake.numerify(rules.get("phonePattern", "##########")),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": random.choice(rules.get("allowedStates", ["NA"])),
                "country": rules.get("country", "USA")
            }
        }

        users.append(user)

    return users
