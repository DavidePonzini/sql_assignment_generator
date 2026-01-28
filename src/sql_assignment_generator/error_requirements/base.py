from ..difficulty_level import DifficultyLevel
from ..constraints import SchemaConstraint, QueryConstraint
from typing import Callable
from abc import ABC, abstractmethod

class SqlErrorRequirements(ABC):
    '''Requirements for generating an assignment likely to trigger a specific error'''

    @abstractmethod
    def dataset_constraints(self, difficulty: DifficultyLevel) -> list[SchemaConstraint]:
        '''Constraints the dataset must satisfy to likely trigger the error.'''
        return []

    @abstractmethod
    def exercise_constraints(self, difficulty: DifficultyLevel) -> list[QueryConstraint]:
        '''Constraints the exercise must satisfy to likely trigger the error.'''
        return []

    @abstractmethod
    def exercise_extra_details(self) -> str:
        '''Additional details or instructions for the exercise.'''
        return ''

    @abstractmethod
    def dataset_extra_details(self) -> str:
        '''Additional details or instructions for the dataset.'''
        return ''