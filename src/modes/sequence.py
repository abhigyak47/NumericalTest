"""
Sequence test mode implementation.
"""

from src.modes.base import BaseMode
from src.generators.sequence import SequenceQuestionFactory


class SequenceTestMode(BaseMode):
    """Sequence test mode"""

    def get_mode_name(self) -> str:
        return "Sequence Test"

    def get_timer_seconds(self) -> int:
        return 300

    def get_question_count(self) -> int:
        return 40

    def create_question_factory(self):
        return SequenceQuestionFactory(self.seed)