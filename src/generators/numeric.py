"""
Numeric question generator for arithmetic problems.
"""

import random
from fractions import Fraction
from typing import List

from src.generators.base import QuestionGenerator
from src.models.question import Question


class NumericQuestionFactory(QuestionGenerator):
    """Factory for generating numeric questions"""

    def __init__(self, seed: int = None):
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

    # -----------------------------------
    # Question type generators
    # -----------------------------------

    def _integer_arithmetic(self) -> Question:
        """Generate integer arithmetic questions"""
        operations = ['+', '-', '*', '/']
        op = random.choice(operations)

        if op == '+':
            a, b = random.randint(1, 100), random.randint(1, 100)
            result = a + b
            prompt = f"What is {a} + {b}?\n"
        elif op == '-':
            a, b = random.randint(1, 100), random.randint(1, 100)
            a, b = max(a, b), min(a, b)
            result = a - b
            prompt = f"What is {a} - {b}?\n"
        elif op == '*':
            a, b = random.randint(2, 20), random.randint(2, 20)
            result = a * b
            prompt = f"What is {a} × {b}?\n"
        else:  # division
            b = random.randint(2, 20)
            result = random.randint(2, 20)
            a = b * result
            prompt = f"What is {a} ÷ {b}?\n"

        correct_answer = str(result)
        return self._create_numeric_question(prompt, correct_answer, "integer_arithmetic")

    def _decimal_arithmetic(self) -> Question:
        """Generate decimal arithmetic questions"""
        operations = ['+', '-', '*']
        op = random.choice(operations)

        if op == '+':
            a, b = round(random.uniform(1, 100), 2), round(random.uniform(1, 100), 2)
            result = round(a + b, 2)
            prompt = f"What is {a:.2f} + {b:.2f}?\n"
        elif op == '-':
            a = round(random.uniform(10, 100), 2)
            b = round(random.uniform(1, a - 1), 2)
            result = round(a - b, 2)
            prompt = f"What is {a:.2f} - {b:.2f}?\n"
        else:
            a, b = round(random.uniform(0.1, 10), 1), round(random.uniform(0.1, 10), 1)
            result = round(a * b, 2)
            prompt = f"What is {a:.1f} × {b:.1f}?\n"

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

        # Perform operation
        if op == '+':
            result = a_frac + b_frac
            prompt = f"What is {a_num}/{a_den} + {b_num}/{b_den}?\n"
        elif op == '-':
            if a_frac < b_frac:
                a_frac, b_frac = b_frac, a_frac
                a_num, a_den, b_num, b_den = b_num, b_den, a_num, a_den
            result = a_frac - b_frac
            prompt = f"What is {a_num}/{a_den} - {b_num}/{b_den}?\n"
        elif op == '*':
            result = a_frac * b_frac
            prompt = f"What is {a_num}/{a_den} × {b_num}/{b_den}?\n"
        else:
            result = a_frac / b_frac
            prompt = f"What is {a_num}/{a_den} ÷ {b_num}/{b_den}?\n"

        # Format result
        if result.numerator >= result.denominator:
            whole = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            correct_answer = str(whole) if remainder == 0 else f"{whole} {remainder}/{result.denominator}"
        else:
            correct_answer = f"{result.numerator}/{result.denominator}"

        return self._create_numeric_question(prompt, correct_answer, "fraction_arithmetic")

    def _mixed_fractions(self) -> Question:
        """Generate mixed fraction arithmetic questions"""
        a_whole = random.randint(1, 5)
        a_den = random.randint(2, 8)
        a_num = random.randint(1, a_den - 1)
        a_total = Fraction(a_whole * a_den + a_num, a_den)

        b_whole = random.randint(1, 5)
        b_den = random.randint(2, 8)
        b_num = random.randint(1, b_den - 1)
        b_total = Fraction(b_whole * b_den + b_num, b_den)

        op = random.choice(['+', '-'])

        if op == '+':
            result = a_total + b_total
            prompt = f"What is {a_whole} {a_num}/{a_den} + {b_whole} {b_num}/{b_den}?\n"
        else:
            if a_total < b_total:
                a_total, b_total = b_total, a_total
                a_whole, a_num, a_den, b_whole, b_num, b_den = b_whole, b_num, b_den, a_whole, a_num, a_den
            result = a_total - b_total
            prompt = f"What is {a_whole} {a_num}/{a_den} - {b_whole} {b_num}/{b_den}?\n"

        if result.numerator >= result.denominator:
            whole = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            correct_answer = str(whole) if remainder == 0 else f"{whole} {remainder}/{result.denominator}"
        else:
            correct_answer = f"{result.numerator}/{result.denominator}"

        return self._create_numeric_question(prompt, correct_answer, "mixed_fractions")

    def _percentages(self) -> Question:
        """Generate percentage questions"""
        common_percents = [12.5, 6.25, 25, 33.33, 20, 10, 5, 50, 75]
        percent = random.choice(common_percents)
        base = random.choice([100, 200, 400, 800, 1000, 50])

        result = round((percent / 100) * base, 2)
        prompt = f"What is {percent}% of {base}?\n"
        correct_answer = str(int(result)) if result.is_integer() else f"{result:.2f}"

        return self._create_numeric_question(prompt, correct_answer, "percentages")

    # -----------------------------------
    # Core creation and explanation
    # -----------------------------------

    def _create_numeric_question(self, prompt: str, correct_answer: str, question_type: str) -> Question:
        """Create a numeric question with distractors"""
        options = [correct_answer]

        # Generate distractors
        if question_type == "integer_arithmetic":
            base = int(correct_answer)
            options.extend([str(base + 1), str(base - 1), str(base * 2), str(base // 2)])

        elif question_type == "decimal_arithmetic":
            base = float(correct_answer)
            options.extend([
                f"{base * 10:.2f}",
                f"{base / 10:.2f}",
                f"{round(base + 0.01, 2):.2f}",
                f"{round(base - 0.01, 2):.2f}"
            ])

        elif question_type in ["fraction_arithmetic", "mixed_fractions"]:
            options.extend([
                f"1/{random.randint(2, 9)}",
                f"{random.randint(2, 9)}/{random.randint(10, 20)}",
                f"{random.randint(1, 5)}",
                f"{random.randint(6, 15)}"
            ])

        elif question_type == "percentages":
            base = float(correct_answer)
            options.extend([
                f"{base * 0.1:.2f}",
                f"{base * 10:.2f}",
                f"{base + 1:.2f}",
                f"{base - 1:.2f}"
            ])

        # Ensure 5 unique options
        options = list(set(options))
        while len(options) < 5:
            options.append(str(random.randint(1, 999)))

        options = options[:5]
        random.shuffle(options)
        answer_letter = chr(ord('A') + options.index(correct_answer))

        explanation = self._generate_numeric_explanation(question_type)

        return Question(
            prompt=prompt,
            options=options,
            answer_letter=answer_letter,
            explanation=explanation,
            meta={"type": question_type, "correct_answer": correct_answer, "latex": False}
        )

    def _generate_numeric_explanation(self, question_type: str) -> str:
        """Generate explanation for numeric questions"""
        explanations = {
            "integer_arithmetic": "Calculate using basic arithmetic operations.",
            "decimal_arithmetic": "Perform the operation carefully, keeping two decimal places.",
            "fraction_arithmetic": "Find a common denominator, compute, then simplify.",
            "mixed_fractions": "Convert mixed numbers to improper fractions, compute, then simplify.",
            "percentages": "Convert percentage to decimal and multiply by the base number."
        }
        return explanations.get(question_type, "Apply the correct mathematical rule.")
