"""
Main application class for the Quant Finance Practice game.
"""

import tkinter as tk
import csv
import sys
import os
from typing import Optional

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.components import MainMenu, TestScreen, ResultsScreen, ReviewScreen
from src.modes.numeric import NumericTestMode
from src.modes.sequence import SequenceTestMode
from src.utils.latex_renderer import LaTeXRenderer


class App(tk.Tk):
    """Main application class"""

    def __init__(self, seed: Optional[int] = None, selftest: bool = False):
        super().__init__()

        self.seed = seed
        self.selftest = selftest
        self.current_mode = None
        self.frames = {}

        if not selftest:
            self.title("Quant Finance Practice")
            self.geometry("900x700")
            self.minsize(900, 600)

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
        elif frame_name == "ReviewScreen":
            frame.update_display()

    def start_numeric_test(self, practice_mode: bool = False, shuffle_options: bool = True):
        """Start numeric test"""
        # Get seed from main menu
        seed_value = self.frames["MainMenu"].seed_var.get()
        seed = int(seed_value) if seed_value.isdigit() else self.seed

        self.current_mode = NumericTestMode(seed)
        self.current_mode.initialize(practice_mode, shuffle_options)
        self.show_frame("TestScreen")
        self.current_mode.start_timer(
            tick_callback=self.update_timer_display,
            finish_callback=self.timer_finished
        )

    def start_sequence_test(self, practice_mode: bool = False, shuffle_options: bool = True):
        """Start sequence test"""
        # Get seed from main menu
        seed_value = self.frames["MainMenu"].seed_var.get()
        seed = int(seed_value) if seed_value.isdigit() else self.seed

        self.current_mode = SequenceTestMode(seed)
        self.current_mode.initialize(practice_mode, shuffle_options)
        self.show_frame("TestScreen")
        self.current_mode.start_timer(
            tick_callback=self.update_timer_display,
            finish_callback=self.timer_finished
        )

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

    def timer_finished(self):
        """Called when timer expires"""
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

    def _generate_error_tag(self, question, chosen: str) -> str:
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

        try:
            # Test numeric mode
            print("Testing numeric mode...")
            self.current_mode = NumericTestMode(12345)  # Fixed seed for testing
            self.current_mode.initialize()
            print(f"Generated {len(self.current_mode.questions)} questions")

            # Test scoring
            print("Testing scoring...")
            self.current_mode.answers[0] = self.current_mode.questions[0].answer_letter
            # Ensure we have a wrong answer by choosing a different letter
            wrong_answer = "A" if self.current_mode.questions[1].answer_letter != "A" else "B"
            self.current_mode.answers[1] = wrong_answer

            total, correct, incorrect, unanswered = self.current_mode.get_score()
            print(f"Score: {total} total, {correct} correct, {incorrect} incorrect, {unanswered} unanswered")
            assert total == 50, f"Expected 50 questions, got {total}"
            assert correct >= 1, "Expected at least 1 correct answer"
            assert incorrect >= 1, "Expected at least 1 incorrect answer"

            # Test CSV export
            print("Testing CSV export...")
            try:
                self.export_to_csv("test_export.csv")
                import os
                os.remove("test_export.csv")
                print("CSV export test passed")
            except Exception as e:
                print(f"CSV export test failed: {e}")

            print("Self-test passed!")
        except Exception as e:
            print(f"Self-test failed: {e}")
            import traceback
            traceback.print_exc()

        if self.selftest:
            self.destroy()

    def cleanup(self):
        """Clean up resources"""
        if self.current_mode:
            self.current_mode.cleanup()

        # Clean up all frames
        for frame in self.frames.values():
            if hasattr(frame, 'cleanup'):
                frame.cleanup()

        # Clean up LaTeX renderer
        latex_renderer = LaTeXRenderer()
        latex_renderer.cleanup()