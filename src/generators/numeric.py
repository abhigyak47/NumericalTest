"""
Numeric question generator for arithmetic problems.
"""

import random
from fractions import Fraction
from typing import List

from src.generators.base import QuestionGenerator
from src.models.question import Question
from src.utils.latex_renderer import LaTeXRenderer


class NumericQuestionFactory(QuestionGenerator):
    """Factory for generating numeric questions with LaTeX rendering"""

    def __init__(self, seed: int = None):
        super().__init__(seed)
        self.latex_renderer = LaTeXRenderer()
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
            prompt = f"\\frac{{{a_num}}}{{{a_den}}} + \\frac{{{b_num}}}{{{b_den}}} = ?"
        elif op == '-':
            # Ensure positive result
            if a_frac < b_frac:
                a_frac, b_frac = b_frac, a_frac
                a_num, a_den, b_num, b_den = b_num, b_den, a_num, a_den
            result = a_frac - b_frac
            prompt = f"\\frac{{{a_num}}}{{{a_den}}} - \\frac{{{b_num}}}{{{b_den}}} = ?"
        elif op == '*':
            result = a_frac * b_frac
            prompt = f"\\frac{{{a_num}}}{{{a_den}}} × \\frac{{{b_num}}}{{{b_den}}} = ?"
        else:  # division
            result = a_frac / b_frac
            prompt = f"\\frac{{{a_num}}}{{{a_den}}} ÷ \\frac{{{b_num}}}{{{b_den}}} = ?"

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
            prompt = f"{a_whole}\\frac{{{a_num}}}{{{a_den}}} + {b_whole}\\frac{{{b_num}}}{{{b_den}}} = ?"
        else:
            # Ensure positive result
            if a_total < b_total:
                a_total, b_total = b_total, a_total
                a_whole, a_num, a_den = b_whole, b_num, b_den
                b_whole, b_num, b_den = a_whole, a_num, a_den
            result = a_total - b_total
            prompt = f"{a_whole}\\frac{{{a_num}}}{{{a_den}}} - {b_whole}\\frac{{{b_num}}}{{{b_den}}} = ?"

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
            prompt = f"{int(percent)}\\% \\text{{ of }} {base} = ?"
        else:
            prompt = f"{percent}\\% \\text{{ of }} {base} = ?"

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
            meta={"type": question_type, "correct_answer": correct_answer, "latex": True}
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

    def cleanup(self):
        """Clean up LaTeX renderer resources"""
        if self.latex_renderer:
            self.latex_renderer.cleanup()