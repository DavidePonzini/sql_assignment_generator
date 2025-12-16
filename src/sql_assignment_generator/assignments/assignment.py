from .dataset import Dataset
from .exercise import Exercise

from dataclasses import dataclass

@dataclass
class Assignment:
    dataset: Dataset
    exercises: list[Exercise]