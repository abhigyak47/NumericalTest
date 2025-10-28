"""
Sequence question generator for pattern recognition problems.
"""

import random
from typing import List

from src.generators.base import QuestionGenerator
from src.models.question import Question


class SequenceQuestionFactory(QuestionGenerator):
    """Factory for generating sequence questions"""

    def __init__(self, seed: int = None):
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

    # ---------------------------
    # Helper: consistent prompt formatting
    # ---------------------------
    def _format_prompt(self, terms: List[int]) -> str:
        """Format the sequence question prompt consistently"""
        return f"What is the next number in this sequence?\n{', '.join(map(str, terms[:5]))}, ?"

    # ---------------------------
    # Sequence generators
    # ---------------------------

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

        prompt = self._format_prompt(terms)
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

        prompt = self._format_prompt(terms)
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

        prompt = self._format_prompt(terms)
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

        prompt = self._format_prompt(terms)
        correct_answer = str(terms[5])
        return self._create_sequence_question(prompt, correct_answer, "alternating", terms)

    def _fibonacci_sequence(self) -> Question:
        """Generate Fibonacci-style sequence questions"""
        start1 = random.randint(1, 5)
        start2 = random.randint(1, 5)

        terms = [start1, start2]
        for i in range(4):
            terms.append(terms[-1] + terms[-2])

        prompt = self._format_prompt(terms)
        correct_answer = str(terms[-1] + terms[-2])
        return self._create_sequence_question(prompt, correct_answer, "fibonacci", terms)

    # ---------------------------
    # Question creation and explanation
    # ---------------------------

    def _create_sequence_question(self, prompt: str, correct_answer: str, pattern_type: str, terms: List[int]) -> Question:
        """Create a sequence question with distractors"""
        options = [correct_answer]
        last_term = terms[-1]

        if pattern_type == "arithmetic":
            step = terms[1] - terms[0]
            options.extend([
                str(last_term + step * 2),
                str(last_term - step),
                str(last_term + step + 1),
                str(last_term + step * 3)
            ])

        elif pattern_type == "geometric":
            ratio = terms[1] // terms[0] if terms[0] != 0 else 2
            options.extend([
                str(last_term * ratio * ratio),
                str(terms[-2]),
                str(last_term * ratio + 1),
                str(last_term * ratio - 1)
            ])

        elif pattern_type in ["n² pattern", "n³ pattern"]:
            options.extend([
                str(terms[-2]),
                str(last_term + 1),
                str(last_term - 1),
                str(last_term + 10)
            ])

        elif pattern_type == "alternating":
            odd_step = terms[2] - terms[0]
            even_step = terms[3] - terms[1]
            options.extend([
                str(last_term + odd_step),
                str(terms[-2]),
                str(last_term + even_step + 1),
                str(last_term + 5)
            ])

        elif pattern_type == "fibonacci":
            options.extend([
                str(terms[-2]),
                str(terms[-1] + terms[-3]),
                str(terms[-1] + terms[-2] + 1),
                str(terms[-1] * 2)
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
            meta={"type": "sequence", "pattern": pattern_type, "terms": terms, "latex": False}
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
