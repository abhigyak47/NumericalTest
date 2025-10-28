"""
Data models for the Quant Finance Practice application.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Question:
    """Data class representing a single question"""
    prompt: str
    options: List[str]  # len=5
    answer_letter: str  # {A|B|C|D|E}
    explanation: str
    meta: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if len(self.options) != 5:
            raise ValueError("Question must have exactly 5 options")
        if self.answer_letter not in ['A', 'B', 'C', 'D', 'E']:
            raise ValueError("Answer must be one of A, B, C, D, E")
        if self.options[ord(self.answer_letter) - ord('A')] not in self.options:
            raise ValueError("Answer letter must correspond to a valid option")


@dataclass
class TestResult:
    """Data class for test results"""
    total_questions: int
    correct: int
    incorrect: int
    unanswered: int
    time_spent: float
    seed: Optional[int] = None
    mode_name: str = ""
    questions: List[Question] = field(default_factory=list)
    answers: List[Optional[str]] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct / self.total_questions) * 100

    @property
    def answered(self) -> int:
        """Number of answered questions"""
        return self.correct + self.incorrect