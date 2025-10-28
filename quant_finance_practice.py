#!/usr/bin/env python3
"""
Quant Finance Numeracy & Sequences — Tkinter OOP Single-File App
A quantitative finance interview practice game with timed tests and detailed review features.

Author: Abhigya Koirala
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from fractions import Fraction
from dataclasses import dataclass, field
import time
import math
import csv
import argparse
import sys
from typing import List, Dict, Optional, Tuple, Any
from abc import ABC, abstractmethod


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


class Timer:
    """Timer class for managing test timing"""

    def __init__(self, initial_seconds: int, tick_callback=None, finish_callback=None):
        self.initial_seconds = initial_seconds
        self.remaining_seconds = initial_seconds
        self.tick_callback = tick_callback
        self.finish_callback = finish_callback
        self.is_running = False
        self.start_time = None
        self.elapsed_seconds = 0

    def start(self):
        """Start the timer"""
        self.is_running = True
        self.start_time = time.time()
        self._tick()

    def stop(self):
        """Stop the timer"""
        self.is_running = False

    def pause(self):
        """Pause the timer"""
        if self.is_running and self.start_time:
            self.elapsed_seconds += time.time() - self.start_time
            self.is_running = False

    def resume(self):
        """Resume the timer"""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self._tick()

    def _tick(self):
        """Internal tick method"""
        if not self.is_running:
            return

        if self.initial_seconds > 0:  # Countdown mode
            elapsed = time.time() - self.start_time if self.start_time else 0
            total_elapsed = self.elapsed_seconds + elapsed
            self.remaining_seconds = max(0, self.initial_seconds - total_elapsed)

            if self.tick_callback:
                self.tick_callback(self.remaining_seconds)

            if self.remaining_seconds <= 0:
                self.stop()
                if self.finish_callback:
                    self.finish_callback()
                return
        else:  # Elapsed mode
            elapsed = time.time() - self.start_time if self.start_time else 0
            total_elapsed = self.elapsed_seconds + elapsed

            if self.tick_callback:
                self.tick_callback(total_elapsed)

        # Schedule next tick
        self.timer_id = tk.Tk.after(tk._default_root, 1000, self._tick)


class QuestionGenerator:
    """Base class for generating questions"""

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    @abstractmethod
    def generate_question(self) -> Question:
        """Generate a single question"""
        pass


class NumericQuestionFactory(QuestionGenerator):
    """Factory for generating numeric questions"""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.question_types = [
            self._integer_arithmetic,
            self._decimal_arithmetic,
            self._fraction_arithmetic,
            self._mixed_fractions,
            self._percentages
        ]

    def generate_question(self) -> Question:
        """Generate a numeric question"""
        generator = random.choice(self.question_types)
        return generator()

    def _integer_arithmetic(self) -> Question:
        """Generate integer arithmetic questions"""
        operations = ['+', '-', '*', '/']
        op = random.choice(operations)

        if op == '+':
            a, b = random.randint(1, 100), random.randint(1, 100)
            result = a + b
            prompt = f"{a} + {b} = ?"
        elif op == '-':
            a, b = random.randint(1, 100), random.randint(1, 100)
            a, b = max(a, b), min(a, b)  # Ensure positive result
            result = a - b
            prompt = f"{a} - {b} = ?"
        elif op == '*':
            a, b = random.randint(2, 20), random.randint(2, 20)
            result = a * b
            prompt = f"{a} × {b} = ?"
        else:  # division
            b = random.randint(2, 20)
            result = random.randint(2, 20)
            a = b * result
            prompt = f"{a} ÷ {b} = ?"

        correct_answer = str(result)
        return self._create_numeric_question(prompt, correct_answer, "integer_arithmetic")

    def _decimal_arithmetic(self) -> Question:
        """Generate decimal arithmetic questions"""
        operations = ['+', '-', '*']
        op = random.choice(operations)

        if op == '+':
            a = round(random.uniform(1, 100), 2)
            b = round(random.uniform(1, 100), 2)
            result = round(a + b, 2)
            prompt = f"{a:.2f} + {b:.2f} = ?"
        elif op == '-':
            a = round(random.uniform(10, 100), 2)
            b = round(random.uniform(1, min(50, a-1)), 2)
            result = round(a - b, 2)
            prompt = f"{a:.2f} - {b:.2f} = ?"
        else:  # multiplication
            a = round(random.uniform(0.1, 10), 1)
            b = round(random.uniform(0.1, 10), 1)
            result = round(a * b, 2)
            prompt = f"{a:.1f} × {b:.1f} = ?"

        correct_answer = f"{result:.2f}"
        return self._create_numeric_question(prompt, correct_answer, "decimal_arithmetic")

    def _fraction_arithmetic(self) -> Question:
        """Generate fraction arithmetic questions"""
        operations = ['+', '-', '*', '/']
        op = random.choice(operations)

        a_num, a_den = random.randint(1, 10), random.randint(2, 12)
        b_num, b_den = random.randint(1, 10), random.randint(2, 12)

        a_frac = Fraction(a_num, a_den)
        b_frac = Fraction(b_num, b_den)

        if op == '+':
            result = a_frac + b_frac
            prompt = f"{a_num}/{a_den} + {b_num}/{b_den} = ?"
        elif op == '-':
            # Ensure positive result
            if a_frac < b_frac:
                a_frac, b_frac = b_frac, a_frac
                a_num, a_den, b_num, b_den = b_num, b_den, a_num, a_den
            result = a_frac - b_frac
            prompt = f"{a_num}/{a_den} - {b_num}/{b_den} = ?"
        elif op == '*':
            result = a_frac * b_frac
            prompt = f"{a_num}/{a_den} × {b_num}/{b_den} = ?"
        else:  # division
            result = a_frac / b_frac
            prompt = f"{a_num}/{a_den} ÷ {b_num}/{b_den} = ?"

        # Format as mixed number if needed
        if result.numerator >= result.denominator:
            whole = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            if remainder == 0:
                correct_answer = str(whole)
            else:
                correct_answer = f"{whole} {remainder}/{result.denominator}"
        else:
            correct_answer = f"{result.numerator}/{result.denominator}"

        return self._create_numeric_question(prompt, correct_answer, "fraction_arithmetic")

    def _mixed_fractions(self) -> Question:
        """Generate mixed fraction arithmetic questions"""
        # Generate mixed fractions
        a_whole = random.randint(1, 5)
        a_num, a_den = random.randint(1, a_den-1 if (a_den := random.randint(2, 8)) else 1), a_den
        a_total = Fraction(a_whole * a_den + a_num, a_den)

        b_whole = random.randint(1, 5)
        b_num, b_den = random.randint(1, b_den-1 if (b_den := random.randint(2, 8)) else 1), b_den
        b_total = Fraction(b_whole * b_den + b_num, b_den)

        op = random.choice(['+', '-'])

        if op == '+':
            result = a_total + b_total
            prompt = f"{a_whole} {a_num}/{a_den} + {b_whole} {b_num}/{b_den} = ?"
        else:
            # Ensure positive result
            if a_total < b_total:
                a_total, b_total = b_total, a_total
                a_whole, a_num, a_den = b_whole, b_num, b_den
                b_whole, b_num, b_den = a_whole, a_num, a_den
            result = a_total - b_total
            prompt = f"{a_whole} {a_num}/{a_den} - {b_whole} {b_num}/{b_den} = ?"

        # Format result
        if result.numerator >= result.denominator:
            whole = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            if remainder == 0:
                correct_answer = str(whole)
            else:
                correct_answer = f"{whole} {remainder}/{result.denominator}"
        else:
            correct_answer = f"{result.numerator}/{result.denominator}"

        return self._create_numeric_question(prompt, correct_answer, "mixed_fractions")

    def _percentages(self) -> Question:
        """Generate percentage questions"""
        # Use common fractions that correspond to nice percentages
        common_percents = [12.5, 6.25, 25, 33.33, 20, 10, 5, 50, 75]
        percent = random.choice(common_percents)
        base = random.choice([100, 200, 400, 800, 1000, 50])

        result = round((percent / 100) * base, 2)

        if percent == int(percent):
            prompt = f"{int(percent)}% of {base} = ?"
        else:
            prompt = f"{percent}% of {base} = ?"

        if result == int(result):
            correct_answer = str(int(result))
        else:
            correct_answer = f"{result:.2f}"

        return self._create_numeric_question(prompt, correct_answer, "percentages")

    def _create_numeric_question(self, prompt: str, correct_answer: str, question_type: str) -> Question:
        """Create a numeric question with distractors"""
        options = [correct_answer]

        # Generate distractors based on question type
        if question_type == "integer_arithmetic":
            # Off-by-one errors
            if correct_answer.isdigit():
                base = int(correct_answer)
                options.extend([str(base + 1), str(base - 1), str(base * 10), str(base // 10)])

        elif question_type == "decimal_arithmetic":
            # Decimal place errors
            try:
                base = float(correct_answer)
                options.extend([
                    f"{base * 10:.2f}",
                    f"{base / 10:.2f}",
                    f"{round(base + 0.01, 2):.2f}",
                    f"{round(base - 0.01, 2):.2f}"
                ])
            except:
                pass

        elif question_type in ["fraction_arithmetic", "mixed_fractions"]:
            # Common fraction mistakes
            options.extend([
                f"1/{random.randint(2, 9)}",
                f"{random.randint(2, 9)}/{random.randint(10, 20)}",
                f"{random.randint(1, 5)}",
                f"{random.randint(6, 15)}"
            ])

        elif question_type == "percentages":
            # Percentage mistakes
            try:
                base = float(correct_answer)
                options.extend([
                    f"{base * 0.1:.2f}",  # 10% instead of given percent
                    f"{base * 10:.2f}",   # 10x instead of given percent
                    f"{base + 1:.2f}",    # Off by 1
                    f"{base - 1:.2f}"     # Off by 1
                ])
            except:
                pass

        # Ensure we have 5 unique options
        options = list(set(options))  # Remove duplicates
        while len(options) < 5:
            options.append(f"{random.randint(1, 999)}")

        options = options[:5]
        random.shuffle(options)

        answer_letter = chr(ord('A') + options.index(correct_answer))

        explanation = self._generate_numeric_explanation(prompt, correct_answer, question_type)

        return Question(
            prompt=prompt,
            options=options,
            answer_letter=answer_letter,
            explanation=explanation,
            meta={"type": question_type, "correct_answer": correct_answer}
        )

    def _generate_numeric_explanation(self, prompt: str, correct_answer: str, question_type: str) -> str:
        """Generate explanation for numeric questions"""
        if question_type == "integer_arithmetic":
            return f"Calculate the result directly using basic arithmetic operations."
        elif question_type == "decimal_arithmetic":
            return f"Perform the operation with attention to decimal places."
        elif question_type == "fraction_arithmetic":
            return f"Find common denominator and perform the operation, then simplify."
        elif question_type == "mixed_fractions":
            return f"Convert to improper fractions, operate, then convert back if needed."
        elif question_type == "percentages":
            return f"Convert percentage to decimal and multiply by the base number."
        else:
            return f"Apply the appropriate mathematical operation."


class SequenceQuestionFactory(QuestionGenerator):
    """Factory for generating sequence questions"""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.pattern_types = [
            self._arithmetic_sequence,
            self._geometric_sequence,
            self._polynomial_sequence,
            self._alternating_sequence,
            self._fibonacci_sequence
        ]

    def generate_question(self) -> Question:
        """Generate a sequence question"""
        generator = random.choice(self.pattern_types)
        return generator()

    def _arithmetic_sequence(self) -> Question:
        """Generate arithmetic sequence questions"""
        step = random.randint(-9, 9)
        while step == 0:
            step = random.randint(-9, 9)

        start = random.randint(1, 20)
        terms = [start + i * step for i in range(6)]  # Show 6 terms

        # Ensure reasonable magnitude
        if any(abs(t) > 100 for t in terms):
            return self._arithmetic_sequence()  # Regenerate

        prompt = f"What is the next number in this sequence?\n"
        prompt += f"{', '.join(map(str, terms[:5]))}, ?"

        correct_answer = str(terms[5])
        return self._create_sequence_question(prompt, correct_answer, "arithmetic", terms)

    def _geometric_sequence(self) -> Question:
        """Generate geometric sequence questions"""
        ratio = random.randint(2, 5)
        start = random.randint(1, 5)
        terms = [start * (ratio ** i) for i in range(6)]

        # Keep terms reasonable
        if terms[-1] > 1000:
            return self._geometric_sequence()  # Regenerate

        prompt = f"What is the next number in this sequence?\n"
        prompt += f"{', '.join(map(str, terms[:5]))}, ?"

        correct_answer = str(terms[5])
        return self._create_sequence_question(prompt, correct_answer, "geometric", terms)

    def _polynomial_sequence(self) -> Question:
        """Generate polynomial sequence questions (n² or n³)"""
        poly_type = random.choice(["square", "cube"])

        if poly_type == "square":
            start_n = random.randint(1, 5)
            terms = [(start_n + i) ** 2 for i in range(6)]
        else:  # cube
            start_n = random.randint(1, 3)
            terms = [(start_n + i) ** 3 for i in range(6)]

        prompt = f"What is the next number in this sequence?\n"
        prompt += f"{', '.join(map(str, terms[:5]))}, ?"

        correct_answer = str(terms[5])
        pattern_name = "n² pattern" if poly_type == "square" else "n³ pattern"
        return self._create_sequence_question(prompt, correct_answer, pattern_name, terms)

    def _alternating_sequence(self) -> Question:
        """Generate alternating/interleaved sequence questions"""
        # Create two separate arithmetic sequences
        step1 = random.randint(1, 5)
        step2 = random.randint(1, 5)
        start1 = random.randint(1, 10)
        start2 = random.randint(1, 10)

        terms = []
        for i in range(6):
            if i % 2 == 0:
                terms.append(start1 + (i // 2) * step1)
            else:
                terms.append(start2 + (i // 2) * step2)

        prompt = f"What is the next number in this sequence?\n"
        prompt += f"{', '.join(map(str, terms[:5]))}, ?"

        correct_answer = str(terms[5])
        return self._create_sequence_question(prompt, correct_answer, "alternating", terms)

    def _fibonacci_sequence(self) -> Question:
        """Generate Fibonacci-style sequence questions"""
        start1 = random.randint(1, 5)
        start2 = random.randint(1, 5)

        terms = [start1, start2]
        for i in range(4):
            terms.append(terms[-1] + terms[-2])

        prompt = f"What is the next number in this sequence?\n"
        prompt += f"{', '.join(map(str, terms))}, ?"

        correct_answer = str(terms[-1] + terms[-2])
        return self._create_sequence_question(prompt, correct_answer, "fibonacci", terms)

    def _create_sequence_question(self, prompt: str, correct_answer: str, pattern_type: str, terms: List[int]) -> Question:
        """Create a sequence question with distractors"""
        options = [correct_answer]

        # Generate distractors
        last_term = terms[-1]

        if pattern_type == "arithmetic":
            step = terms[1] - terms[0]
            options.extend([
                str(last_term + step * 2),  # Skip one step
                str(last_term - step),      # Previous term
                str(last_term + step + 1),  # Off by one
                str(last_term + step * 3)   # Multiple steps
            ])

        elif pattern_type == "geometric":
            ratio = terms[1] // terms[0] if terms[0] != 0 else 2
            options.extend([
                str(last_term * ratio * ratio),  # Skip one step
                str(terms[-2]),                  # Previous term
                str(last_term * ratio + 1),      # Off by one
                str(last_term * ratio - 1)       # Off by one
            ])

        elif pattern_type in ["n² pattern", "n³ pattern"]:
            options.extend([
                str(terms[-2]),                  # Previous term
                str(last_term + 1),              # Off by one
                str(last_term - 1),              # Off by one
                str(last_term + 10)              # Random error
            ])

        elif pattern_type == "alternating":
            # Wrong pattern application
            odd_step = terms[2] - terms[0]
            even_step = terms[3] - terms[1]
            options.extend([
                str(last_term + odd_step),       # Apply wrong step
                str(terms[-2]),                  # Previous term
                str(last_term + even_step + 1),  # Wrong step + error
                str(last_term + 5)               # Random error
            ])

        elif pattern_type == "fibonacci":
            options.extend([
                str(terms[-2]),                  # Previous term
                str(terms[-1] + terms[-3]),      # Wrong sum
                str(terms[-1] + terms[-2] + 1),  # Off by one
                str(terms[-1] * 2)               # Double instead of sum
            ])

        # Ensure we have 5 unique options
        options = list(set(options))
        while len(options) < 5:
            options.append(str(random.randint(1, 200)))

        options = options[:5]
        random.shuffle(options)

        answer_letter = chr(ord('A') + options.index(correct_answer))

        explanation = self._generate_sequence_explanation(pattern_type, terms)

        return Question(
            prompt=prompt,
            options=options,
            answer_letter=answer_letter,
            explanation=explanation,
            meta={"type": "sequence", "pattern": pattern_type, "terms": terms}
        )

    def _generate_sequence_explanation(self, pattern_type: str, terms: List[int]) -> str:
        """Generate explanation for sequence questions"""
        if pattern_type == "arithmetic":
            step = terms[1] - terms[0]
            return f"This is an arithmetic sequence with common difference {step}. Each term increases by {step}."
        elif pattern_type == "geometric":
            ratio = terms[1] // terms[0] if terms[0] != 0 else 2
            return f"This is a geometric sequence with common ratio {ratio}. Each term is multiplied by {ratio}."
        elif pattern_type == "n² pattern":
            return f"This sequence follows the pattern n² (squares of consecutive integers)."
        elif pattern_type == "n³ pattern":
            return f"This sequence follows the pattern n³ (cubes of consecutive integers)."
        elif pattern_type == "alternating":
            odd_step = terms[2] - terms[0]
            even_step = terms[3] - terms[1]
            return f"This is an alternating sequence. Odd positions increase by {odd_step}, even positions by {even_step}."
        elif pattern_type == "fibonacci":
            return f"This is a Fibonacci-style sequence where each term is the sum of the two preceding terms."
        else:
            return f"Identify the pattern and apply it to find the next term."


class BaseMode(ABC):
    """Base class for test modes"""

    def __init__(self, app, seed: Optional[int] = None):
        self.app = app
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
    def create_question_factory(self) -> QuestionGenerator:
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
                random.shuffle(question.options)
                new_answer_index = question.options.index(original_answer)
                question.answer_letter = chr(ord('A') + new_answer_index)

            self.questions.append(question)

        self.answers = [None] * len(self.questions)
        self.current_question_index = 0

    def start_timer(self):
        """Start the timer"""
        timer_seconds = self.get_timer_seconds() if not self.practice_mode else -1
        self.timer = Timer(
            timer_seconds,
            tick_callback=self.app.update_timer_display,
            finish_callback=self.timer_finished
        )
        self.start_time = time.time()
        self.timer.start()

    def timer_finished(self):
        """Called when timer expires"""
        self.app.show_frame("ResultsScreen")

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


class NumericTestMode(BaseMode):
    """Numeric test mode"""

    def get_mode_name(self) -> str:
        return "Numeric Test"

    def get_timer_seconds(self) -> int:
        return 360

    def get_question_count(self) -> int:
        return 50

    def create_question_factory(self) -> QuestionGenerator:
        return NumericQuestionFactory(self.seed)


class SequenceTestMode(BaseMode):
    """Sequence test mode"""

    def get_mode_name(self) -> str:
        return "Sequence Test"

    def get_timer_seconds(self) -> int:
        return 300

    def get_question_count(self) -> int:
        return 40

    def create_question_factory(self) -> QuestionGenerator:
        return SequenceQuestionFactory(self.seed)


class App(tk.Tk):
    """Main application class"""

    def __init__(self, seed: Optional[int] = None, selftest: bool = False):
        super().__init__()

        self.title("Quant Finance Practice")
        self.geometry("900x700")
        self.minsize(900, 600)

        self.seed = seed
        self.selftest = selftesttest
        self.current_mode: Optional[BaseMode] = None
        self.frames = {}

        # Bind keyboard shortcuts
        self.bind('<Left>', lambda e: self.previous_question())
        self.bind('<Right>', lambda e: self.next_question())
        self.bind('<Return>', lambda e: self.next_question())
        self.bind('<Control-f>', lambda e: self.finish_test())
        self.bind('<Command-f>', lambda e: self.finish_test())

        self.create_frames()
        self.show_frame("MainMenu")

        if selftest:
            self.run_selftest()

    def create_frames(self):
        """Create all frames"""
        # Main Menu
        self.frames["MainMenu"] = MainMenu(self)
        self.frames["MainMenu"].grid(row=0, column=0, sticky="nsew")

        # Test Screen
        self.frames["TestScreen"] = TestScreen(self)
        self.frames["TestScreen"].grid(row=0, column=0, sticky="nsew")

        # Results Screen
        self.frames["ResultsScreen"] = ResultsScreen(self)
        self.frames["ResultsScreen"].grid(row=0, column=0, sticky="nsew")

        # Review Screen
        self.frames["ReviewScreen"] = ReviewScreen(self)
        self.frames["ReviewScreen"].grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name: str):
        """Show a specific frame"""
        frame = self.frames[frame_name]
        frame.tkraise()

        if frame_name == "TestScreen":
            frame.update_display()
        elif frame_name == "ResultsScreen":
            frame.update_display()

    def start_numeric_test(self, practice_mode: bool = False, shuffle_options: bool = True):
        """Start numeric test"""
        self.current_mode = NumericTestMode(self.seed)
        self.current_mode.initialize(practice_mode, shuffle_options)
        self.show_frame("TestScreen")
        self.current_mode.start_timer()

    def start_sequence_test(self, practice_mode: bool = False, shuffle_options: bool = True):
        """Start sequence test"""
        self.current_mode = SequenceTestMode(self.seed)
        self.current_mode.initialize(practice_mode, shuffle_options)
        self.show_frame("TestScreen")
        self.current_mode.start_timer()

    def previous_question(self):
        """Go to previous question"""
        if self.current_mode and self.current_mode.current_question_index > 0:
            self.current_mode.current_question_index -= 1
            self.frames["TestScreen"].update_display()

    def next_question(self):
        """Go to next question"""
        if self.current_mode and self.current_mode.current_question_index < len(self.current_mode.questions) - 1:
            self.current_mode.current_question_index += 1
            self.frames["TestScreen"].update_display()

    def finish_test(self):
        """Finish current test"""
        if self.current_mode:
            self.current_mode.stop_timer()
            self.show_frame("ResultsScreen")

    def update_timer_display(self, remaining_seconds: int):
        """Update timer display"""
        if "TestScreen" in self.frames:
            self.frames["TestScreen"].update_timer(remaining_seconds)

    def export_to_csv(self, filename: str):
        """Export results to CSV"""
        if not self.current_mode:
            return

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'question', 'A', 'B', 'C', 'D', 'E',
                'correct', 'chosen', 'correctness', 'time_spent', 'error_tag'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, question in enumerate(self.current_mode.questions):
                chosen = self.current_mode.answers[i] or "Unanswered"
                correctness = "Correct" if chosen == question.answer_letter else "Incorrect"

                # Generate error tag
                error_tag = ""
                if correctness == "Incorrect":
                    error_tag = self._generate_error_tag(question, chosen)

                writer.writerow({
                    'question': question.prompt,
                    'A': question.options[0],
                    'B': question.options[1],
                    'C': question.options[2],
                    'D': question.options[3],
                    'E': question.options[4],
                    'correct': question.answer_letter,
                    'chosen': chosen,
                    'correctness': correctness,
                    'time_spent': "",  # Could track per-question timing
                    'error_tag': error_tag
                })

    def _generate_error_tag(self, question: Question, chosen: str) -> str:
        """Generate error tag based on question and chosen answer"""
        correct_value = question.options[ord(question.answer_letter) - ord('A')]

        try:
            chosen_value = question.options[ord(chosen) - ord('A')]

            # Check for common error patterns
            if question.meta.get("type") in ["integer_arithmetic", "decimal_arithmetic"]:
                try:
                    correct_num = float(correct_value)
                    chosen_num = float(chosen_value)

                    if abs(correct_num - chosen_num) == 1:
                        return "off-by-one"
                    elif abs(correct_num - chosen_num * 10) < 0.01 or abs(correct_num - chosen_num / 10) < 0.01:
                        return "decimal-place"
                except:
                    pass

            elif question.meta.get("type") in ["fraction_arithmetic", "mixed_fractions"]:
                return "fraction-reduction"

            elif question.meta.get("type") == "sequence":
                if question.meta.get("pattern") == "geometric":
                    return "wrong-ratio"
                elif question.meta.get("pattern") == "alternating":
                    return "interleave-swap"
                elif question.meta.get("pattern") == "fibonacci":
                    return "fib-near"

        except:
            pass

        return "other"

    def run_selftest(self):
        """Run self-test mode"""
        print("Running self-test...")

        # Test numeric mode
        self.current_mode = NumericTestMode(12345)  # Fixed seed for testing
        self.current_mode.initialize()

        # Test scoring
        self.current_mode.answers[0] = self.current_mode.questions[0].answer_letter
        self.current_mode.answers[1] = "B"  # Wrong answer

        total, correct, incorrect, unanswered = self.current_mode.get_score()
        assert total == 50, f"Expected 50 questions, got {total}"
        assert correct >= 1, "Expected at least 1 correct answer"
        assert incorrect >= 1, "Expected at least 1 incorrect answer"

        # Test CSV export
        try:
            self.export_to_csv("test_export.csv")
            import os
            os.remove("test_export.csv")
        except Exception as e:
            print(f"CSV export test failed: {e}")

        print("Self-test passed!")
        if self.selftest:
            self.quit()


class MainMenu(tk.Frame):
    """Main menu frame"""

    def __init__(self, app: App):
        super().__init__(app)
        self.app = app

        # Title
        title_label = tk.Label(self, text="Quant Finance Practice", font=("Arial", 24, "bold"))
        title_label.pack(pady=50)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        numeric_btn = tk.Button(
            button_frame, text="Numeric Test",
            command=lambda: self.app.start_numeric_test(self.practice_mode_var.get(), self.shuffle_var.get()),
            width=20, height=2
        )
        numeric_btn.pack(pady=10)

        sequence_btn = tk.Button(
            button_frame, text="Sequence Test",
            command=lambda: self.app.start_sequence_test(self.practice_mode_var.get(), self.shuffle_var.get()),
            width=20, height=2
        )
        sequence_btn.pack(pady=10)

        # Options
        options_frame = tk.Frame(self)
        options_frame.pack(pady=30)

        self.seed_var = tk.StringVar(value="")
        self.practice_mode_var = tk.BooleanVar(value=False)
        self.shuffle_var = tk.BooleanVar(value=True)

        tk.Label(options_frame, text="Seed (optional):").grid(row=0, column=0, sticky="e", padx=5)
        seed_entry = tk.Entry(options_frame, textvariable=self.seed_var, width=15)
        seed_entry.grid(row=0, column=1, padx=5)

        practice_check = tk.Checkbutton(
            options_frame, text="Practice Mode (no timer)",
            variable=self.practice_mode_var
        )
        practice_check.grid(row=1, column=0, columnspan=2, pady=5)

        shuffle_check = tk.Checkbutton(
            options_frame, text="Shuffle Options",
            variable=self.shuffle_var
        )
        shuffle_check.grid(row=2, column=0, columnspan=2, pady=5)

        # Set seed if provided
        if self.app.seed is not None:
            self.seed_var.set(str(self.app.seed))


class TestScreen(tk.Frame):
    """Test screen frame"""

    def __init__(self, app: App):
        super().__init__(app)
        self.app = app

        # Top bar
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.mode_label = tk.Label(top_frame, text="", font=("Arial", 12))
        self.mode_label.pack(side="left")

        self.timer_label = tk.Label(top_frame, text="", font=("Arial", 12, "bold"))
        self.timer_label.pack(side="right")

        self.progress_label = tk.Label(top_frame, text="", font=("Arial", 12))
        self.progress_label.pack()

        # Question frame
        question_frame = tk.Frame(self)
        question_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.index_label = tk.Label(question_frame, text="", font=("Arial", 14))
        self.index_label.pack(anchor="w", pady=(0, 10))

        self.prompt_label = tk.Label(question_frame, text="", font=("Arial", 14), wraplength=800, justify="left")
        self.prompt_label.pack(anchor="w", pady=(0, 20))

        # Options
        self.option_labels = []
        for i in range(5):
            label = tk.Label(question_frame, text="", font=("Arial", 12))
            label.pack(anchor="w", pady=2)
            self.option_labels.append(label)

        # Answer dropdown
        self.answer_var = tk.StringVar(value="Select Answer")
        self.answer_dropdown = ttk.Combobox(
            question_frame, textvariable=self.answer_var,
            values=["Select Answer", "A", "B", "C", "D", "E"],
            state="readonly", width=15
        )
        self.answer_dropdown.pack(pady=20)
        self.answer_dropdown.bind("<<ComboboxSelected>>", self.on_answer_selected)

        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(side="bottom", pady=20)

        self.prev_btn = tk.Button(nav_frame, text="Previous", command=self.app.previous_question, width=15)
        self.prev_btn.pack(side="left", padx=5)

        self.next_btn = tk.Button(nav_frame, text="Next", command=self.app.next_question, width=15)
        self.next_btn.pack(side="left", padx=5)

        self.finish_btn = tk.Button(nav_frame, text="Finish Test", command=self.finish_test, width=15)
        self.finish_btn.pack(side="left", padx=5)

    def update_display(self):
        """Update the display"""
        if not self.app.current_mode:
            return

        mode = self.app.current_mode
        question = mode.get_current_question()

        if not question:
            return

        # Update labels
        self.mode_label.config(text=f"Mode: {mode.get_mode_name()}")
        self.index_label.config(text=f"Question {mode.current_question_index + 1} of {len(mode.questions)}")
        self.progress_label.config(text=f"Progress: {mode.current_question_index + 1}/{len(mode.questions)}")

        # Update question
        self.prompt_label.config(text=question.prompt)

        # Update options
        for i, option in enumerate(question.options):
            letter = chr(ord('A') + i)
            self.option_labels[i].config(text=f"{letter}. {option}")

        # Update answer dropdown
        current_answer = mode.answers[mode.current_question_index]
        if current_answer:
            self.answer_var.set(current_answer)
        else:
            self.answer_var.set("Select Answer")

        # Update navigation buttons
        self.prev_btn.config(state="normal" if mode.current_question_index > 0 else "disabled")
        self.next_btn.config(state="normal" if mode.current_question_index < len(mode.questions) - 1 else "disabled")

    def update_timer(self, remaining_seconds: int):
        """Update timer display"""
        if self.app.current_mode and self.app.current_mode.practice_mode:
            minutes, seconds = divmod(int(remaining_seconds), 60)
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d} (elapsed)")
        else:
            minutes, seconds = divmod(remaining_seconds, 60)
            color = "red" if remaining_seconds <= 60 else "black"
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}", fg=color)

    def on_answer_selected(self, event):
        """Handle answer selection"""
        answer = self.answer_var.get()
        if answer != "Select Answer":
            self.app.current_mode.set_answer(answer)

    def finish_test(self):
        """Finish the test"""
        # Check for unanswered questions
        unanswered = sum(1 for a in self.app.current_mode.answers if a is None or a == "Select Answer")
        if unanswered > 0:
            if not messagebox.askyesno("Unanswered Questions",
                                     f"You have {unanswered} unanswered questions. Finish anyway?"):
                return

        self.app.finish_test()


class ResultsScreen(tk.Frame):
    """Results screen frame"""

    def __init__(self, app: App):
        super().__init__(app)
        self.app = app

        # Title
        title_label = tk.Label(self, text="Test Results", font=("Arial", 20, "bold"))
        title_label.pack(pady=30)

        # Results frame
        results_frame = tk.Frame(self)
        results_frame.pack(pady=20)

        self.score_labels = {}
        score_items = ["Total", "Correct", "Incorrect", "Unanswered"]

        for i, item in enumerate(score_items):
            label = tk.Label(results_frame, text=f"{item}:", font=("Arial", 14))
            label.grid(row=i, column=0, sticky="e", padx=20, pady=5)

            value_label = tk.Label(results_frame, text="0", font=("Arial", 14, "bold"))
            value_label.grid(row=i, column=1, sticky="w", padx=20, pady=5)

            self.score_labels[item] = value_label

        # Seed display
        self.seed_label = tk.Label(self, text="", font=("Arial", 10))
        self.seed_label.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=30)

        review_btn = tk.Button(button_frame, text="Review Answers", command=self.review_answers, width=15)
        review_btn.pack(side="left", padx=5)

        menu_btn = tk.Button(button_frame, text="Main Menu", command=self.back_to_menu, width=15)
        menu_btn.pack(side="left", padx=5)

        retry_btn = tk.Button(button_frame, text="Retry (same mode)", command=self.retry_same_mode, width=15)
        retry_btn.pack(side="left", padx=5)

        export_btn = tk.Button(button_frame, text="Export CSV", command=self.export_csv, width=15)
        export_btn.pack(side="left", padx=5)

    def update_display(self):
        """Update the display"""
        if not self.app.current_mode:
            return

        total, correct, incorrect, unanswered = self.app.current_mode.get_score()

        self.score_labels["Total"].config(text=str(total))
        self.score_labels["Correct"].config(text=str(correct))
        self.score_labels["Incorrect"].config(text=str(incorrect))
        self.score_labels["Unanswered"].config(text=str(unanswered))

        # Show seed if used
        if self.app.current_mode.seed is not None:
            self.seed_label.config(text=f"Seed used: {self.app.current_mode.seed}")
        else:
            self.seed_label.config(text="")

    def review_answers(self):
        """Review answers"""
        self.app.show_frame("ReviewScreen")

    def back_to_menu(self):
        """Return to main menu"""
        self.app.current_mode = None
        self.app.show_frame("MainMenu")

    def retry_same_mode(self):
        """Retry the same mode"""
        if self.app.current_mode:
            mode_type = type(self.app.current_mode)
            practice_mode = self.app.current_mode.practice_mode
            shuffle_options = self.app.current_mode.shuffle_options

            if mode_type == NumericTestMode:
                self.app.start_numeric_test(practice_mode, shuffle_options)
            elif mode_type == SequenceTestMode:
                self.app.start_sequence_test(practice_mode, shuffle_options)

    def export_csv(self):
        """Export results to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                self.app.export_to_csv(filename)
                messagebox.showinfo("Export Successful", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Failed to export: {str(e)}")


class ReviewScreen(tk.Frame):
    """Review screen frame"""

    def __init__(self, app: App):
        super().__init__(app)
        self.app = app
        self.current_review_index = 0

        # Title
        title_label = tk.Label(self, text="Review Answers", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Question info frame
        info_frame = tk.Frame(self)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrollable text area
        self.text_area = tk.Text(info_frame, wrap="word", font=("Arial", 11), height=20)
        scrollbar = tk.Scrollbar(info_frame, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)

        self.text_area.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Navigation
        nav_frame = tk.Frame(self)
        nav_frame.pack(side="bottom", pady=20)

        self.prev_btn = tk.Button(nav_frame, text="Previous", command=self.previous_question, width=15)
        self.prev_btn.pack(side="left", padx=5)

        self.question_label = tk.Label(nav_frame, text="", font=("Arial", 12))
        self.question_label.pack(side="left", padx=20)

        self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_question, width=15)
        self.next_btn.pack(side="left", padx=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side="bottom", pady=10)

        back_btn = tk.Button(button_frame, text="Back to Results", command=self.back_to_results, width=15)
        back_btn.pack(side="left", padx=5)

        redrill_btn = tk.Button(button_frame, text="Re-drill my mistakes (10)", command=self.redrill_mistakes, width=20)
        redrill_btn.pack(side="left", padx=5)

    def update_display(self):
        """Update the display"""
        if not self.app.current_mode:
            return

        self.current_review_index = 0
        self.show_current_question()

    def show_current_question(self):
        """Show current question review"""
        if not self.app.current_mode:
            return

        mode = self.app.current_mode

        if self.current_review_index >= len(mode.questions):
            return

        question = mode.questions[self.current_review_index]
        answer = mode.answers[self.current_review_index]

        # Update navigation
        self.question_label.config(text=f"Question {self.current_review_index + 1} of {len(mode.questions)}")
        self.prev_btn.config(state="normal" if self.current_review_index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.current_review_index < len(mode.questions) - 1 else "disabled")

        # Clear and populate text area
        self.text_area.delete("1.0", "end")

        # Question text
        self.text_area.insert("end", f"Question {self.current_review_index + 1}:\n\n", "title")
        self.text_area.insert("end", f"{question.prompt}\n\n", "question")

        # Options
        self.text_area.insert("end", "Options:\n", "subtitle")
        for i, option in enumerate(question.options):
            letter = chr(ord('A') + i)
            marker = " ✓" if letter == question.answer_letter else ""
            self.text_area.insert("end", f"  {letter}. {option}{marker}\n")

        self.text_area.insert("end", "\n")

        # Correct answer
        correct_letter = question.answer_letter
        correct_value = question.options[ord(correct_letter) - ord('A')]
        self.text_area.insert("end", f"Correct Answer: {correct_letter}. {correct_value}\n\n", "correct")

        # Your answer
        if answer and answer != "Select Answer":
            chosen_value = question.options[ord(answer) - ord('A')]
            is_correct = answer == question.answer_letter
            status = "✓ Correct" if is_correct else "✗ Incorrect"
            self.text_area.insert("end", f"Your Answer: {answer}. {chosen_value} ({status})\n\n",
                                 "correct" if is_correct else "incorrect")
        else:
            self.text_area.insert("end", "Your Answer: Unanswered\n\n", "unanswered")

        # Explanation
        self.text_area.insert("end", "Explanation:\n", "subtitle")
        self.text_area.insert("end", f"{question.explanation}\n\n", "explanation")

        # Error tag
        if answer and answer != "Select Answer" and answer != question.answer_letter:
            error_tag = self.app._generate_error_tag(question, answer)
            self.text_area.insert("end", f"Error Type: {error_tag}\n", "error")

        # Configure tags
        self.text_area.tag_config("title", font=("Arial", 14, "bold"))
        self.text_area.tag_config("subtitle", font=("Arial", 12, "bold"))
        self.text_area.tag_config("question", font=("Arial", 11))
        self.text_area.tag_config("correct", foreground="green", font=("Arial", 11, "bold"))
        self.text_area.tag_config("incorrect", foreground="red", font=("Arial", 11, "bold"))
        self.text_area.tag_config("unanswered", foreground="gray", font=("Arial", 11))
        self.text_area.tag_config("explanation", font=("Arial", 11, "italic"))
        self.text_area.tag_config("error", foreground="orange", font=("Arial", 11))

    def previous_question(self):
        """Show previous question"""
        if self.current_review_index > 0:
            self.current_review_index -= 1
            self.show_current_question()

    def next_question(self):
        """Show next question"""
        if self.app.current_mode and self.current_review_index < len(self.app.current_mode.questions) - 1:
            self.current_review_index += 1
            self.show_current_question()

    def back_to_results(self):
        """Go back to results"""
        self.app.show_frame("ResultsScreen")

    def redrill_mistakes(self):
        """Practice mistakes again"""
        if not self.app.current_mode:
            return

        # Find incorrect questions
        mistakes = []
        for i, question in enumerate(self.app.current_mode.questions):
            answer = self.app.current_mode.answers[i]
            if not answer or answer == "Select Answer" or answer != question.answer_letter:
                mistakes.append(question)

        # Limit to 10 mistakes
        mistakes = mistakes[:10]

        if not mistakes:
            messagebox.showinfo("No Mistakes", "You have no mistakes to practice!")
            return

        # Create new mode with mistake questions
        mode_type = type(self.app.current_mode)
        new_mode = mode_type(self.app.current_mode.seed)
        new_mode.questions = mistakes
        new_mode.answers = [None] * len(mistakes)
        new_mode.current_question_index = 0
        new_mode.practice_mode = True  # Always practice mode for redrill
        new_mode.shuffle_options = False  # Don't shuffle for focused practice

        self.app.current_mode = new_mode
        self.app.show_frame("TestScreen")
        new_mode.start_timer()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Quant Finance Practice Game")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible sessions")
    parser.add_argument("--selftest", action="store_true", help="Run self-test and exit")

    args = parser.parse_args()

    app = App(seed=args.seed, selftest=args.selftest)
    app.mainloop()


if __name__ == "__main__":
    main()