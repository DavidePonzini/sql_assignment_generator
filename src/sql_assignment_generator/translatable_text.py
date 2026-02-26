
class TranslatableText:
    '''A simple wrapper for a translatable text string.'''

    def __init__(self, en: str = '', **kwargs) -> None:
        self.translations = {
            'en': en,
        }

        self.translations.update(kwargs)
    def get(self, language: str = 'en', **kwargs) -> str:
        '''
            Return the text in the specified language, falling back to English if not available.

            Args:
                language (str): The language code for the desired translation (default: 'en').
                **kwargs: Additional keyword arguments to format the string with.
        '''

        result =  self.translations.get(language, self.translations['en'])
        
        if kwargs:
            return result.format(**kwargs)
        return result
    
    def __add__(self, other):
        if not isinstance(other, TranslatableText):
            return NotImplemented
        
        combined_translations = {
            lang: self.translations.get(lang, '') + other.translations.get(lang, '')
            for lang in set(self.translations) | set(other.translations)
        }
        
        return TranslatableText(**combined_translations)
    
    def strip(self) -> 'TranslatableText':
        '''Return a new TranslatableText with leading and trailing whitespace removed from all translations.'''
        stripped_translations = {
            lang: text.strip()
            for lang, text in self.translations.items()
        }

        return TranslatableText(**stripped_translations)
    