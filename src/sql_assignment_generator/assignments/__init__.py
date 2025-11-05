from .assignment import Assignment
import random

def random_domain() -> str:
    """
    Select and return a random domain from predefined list.
    """
    domains = [
        "sport",
        "university",
        "travels",
        "airport",
        "hobby",
        "factory",
        "hospital",
        "restaurant"
    ]
    selected_domain = random.choice(domains)
    return selected_domain