from enum import Enum

class DifficultyLevel(Enum):
    EASY = 1
    '''Minimal cognitive load, the assignments contains only elements related to triggering the error'''

    MEDIUM = 2
    '''Moderate cognitive load, the assignments contains some elements not related to triggering the error'''

    HARD = 3
    '''High cognitive load, the assignments contains elements not related to triggering the error and may require complex reasoning'''