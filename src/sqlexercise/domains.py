import random
from .translatable_text import TranslatableText

domains = [
    TranslatableText('sports',      it='sport'      ),
    TranslatableText('university',  it='università' ),
    TranslatableText('travels',     it='viaggi'     ),
    TranslatableText('airport',     it='aeroporto'  ),
    TranslatableText('hobby',       it='passatempo' ),
    TranslatableText('factory',     it='fabbrica'   ),
    TranslatableText('hospital',    it='ospedale'   ),
    TranslatableText('restaurant',  it='ristorante' ),
    TranslatableText('banking',     it='banca'      ),
    TranslatableText('school',      it='scuola'     ),
]

def random_domain(language: str) -> str:
    '''Select and return a random domain from predefined list.'''
    
    selected_domain = random.choice(domains)
    return selected_domain.get(language)