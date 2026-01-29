class ConstraintValidationError(Exception):
    '''Custom exception for constraint validation errors.'''
    pass

class SQLParsingError(Exception):
    '''Custom exception for SQL parsing errors.'''
    
    def __init__(self, message: str, sql: str) -> None:
        super().__init__(message)
        self.sql = sql

    def __str__(self) -> str:
        return f'{super().__str__()}\nSQL:\n{self.sql}'
    
class ConstraintMergeError(Exception):
    '''Custom exception for errors during merging of dataset constraints.'''
    
    def __init__(self, this, other) -> None:
        message = f'Cannot merge constraints of different types: {type(this)} vs {type(other)}'
        super().__init__(message)

class ExerciseGenerationError(Exception):
    '''Custom exception for errors during exercise generation.'''
    pass

class DatasetGenerationError(Exception):
    '''Custom exception for errors during dataset generation.'''
    pass