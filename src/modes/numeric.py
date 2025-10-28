"""
Numeric test mode implementation.
"""

from src.modes.base import BaseMode
from src.generators.numeric import NumericQuestionFactory


class NumericTestMode(BaseMode):
    """Numeric test mode"""

    def get_mode_name(self) -> str:
        return "Numeric Test"

    def get_timer_seconds(self) -> int:
        return 360

    def get_question_count(self) -> int:
        return 50

    def create_question_factory(self):
        return NumericQuestionFactory(self.seed)