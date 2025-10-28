"""
Base classes for question generators.
"""

from abc import ABC, abstractmethod
from typing import Optional
import random

from src.models.question import Question


class QuestionGenerator(ABC):
    """Base class for generating questions"""

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    @abstractmethod
    def generate_question(self) -> Question:
        """Generate a single question"""
        pass