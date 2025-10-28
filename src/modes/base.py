"""
Base mode classes for different test modes.
"""

import time
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from src.models.question import Question
from src.models.timer import Timer


class BaseMode(ABC):
    """Base class for test modes"""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.questions: List[Question] = []
        self.answers: List[Optional[str]] = []
        self.current_question_index = 0
        self.timer = None
        self.start_time = None
        self.practice_mode = False
        self.shuffle_options = True

    @abstractmethod
    def get_mode_name(self) -> str:
        """Get the mode name"""
        pass

    @abstractmethod
    def get_timer_seconds(self) -> int:
        """Get timer duration in seconds"""
        pass

    @abstractmethod
    def get_question_count(self) -> int:
        """Get number of questions"""
        pass

    @abstractmethod
    def create_question_factory(self):
        """Create question factory for this mode"""
        pass

    def initialize(self, practice_mode: bool = False, shuffle_options: bool = True):
        """Initialize the mode"""
        self.practice_mode = practice_mode
        self.shuffle_options = shuffle_options

        # Generate questions
        factory = self.create_question_factory()
        self.questions = []
        for _ in range(self.get_question_count()):
            question = factory.generate_question()

            # Shuffle options if requested
            if self.shuffle_options:
                original_answer = question.options[ord(question.answer_letter) - ord('A')]
                import random
                random.shuffle(question.options)
                new_answer_index = question.options.index(original_answer)
                question.answer_letter = chr(ord('A') + new_answer_index)

            self.questions.append(question)

        self.answers = [None] * len(self.questions)
        self.current_question_index = 0

    def start_timer(self, tick_callback=None, finish_callback=None):
        """Start the timer"""
        timer_seconds = self.get_timer_seconds() if not self.practice_mode else -1
        self.timer = Timer(
            timer_seconds,
            tick_callback=tick_callback,
            finish_callback=finish_callback
        )
        self.start_time = time.time()
        self.timer.start()

    def timer_finished(self):
        """Called when timer expires"""
        pass  # Override in subclasses if needed

    def stop_timer(self):
        """Stop the timer"""
        if self.timer:
            self.timer.stop()

    def get_current_question(self) -> Optional[Question]:
        """Get current question"""
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def set_answer(self, answer: Optional[str]):
        """Set answer for current question"""
        if 0 <= self.current_question_index < len(self.questions):
            self.answers[self.current_question_index] = answer

    def get_score(self) -> Tuple[int, int, int, int]:
        """Calculate score: (total, correct, incorrect, unanswered)"""
        correct = 0
        incorrect = 0
        unanswered = 0

        for i, question in enumerate(self.questions):
            answer = self.answers[i]
            if answer is None or answer == "Select Answer":
                unanswered += 1
            elif answer == question.answer_letter:
                correct += 1
            else:
                incorrect += 1

        return len(self.questions), correct, incorrect, unanswered

    def get_time_spent(self) -> float:
        """Get time spent in seconds"""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0

    def cleanup(self):
        """Clean up resources"""
        if self.timer:
            self.timer.stop()
        if hasattr(self, 'create_question_factory'):
            factory = self.create_question_factory()
            if hasattr(factory, 'cleanup'):
                factory.cleanup()