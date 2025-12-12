import random

def random_domain() -> str:
    '''Select and return a random domain from predefined list.'''
    
    domains = [
        'sports',
        'university',
        'travels',
        'airport',
        'hobby',
        'factory',
        'hospital',
        'restaurant',
        'banking',
        'school',
    ]
    
    selected_domain = random.choice(domains)
    return selected_domain