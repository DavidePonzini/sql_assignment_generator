from .dataset import Dataset
from .exercise import Exercise

from dataclasses import dataclass

@dataclass
class Assignment:
    '''A full SQL assignment consisting of a dataset and exercises.'''
    
    dataset: Dataset
    '''The dataset associated with the assignment.'''
    
    exercises: list[Exercise]
    '''The exercises included in the assignment.'''