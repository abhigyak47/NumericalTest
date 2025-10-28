"""
GUI components for the Quant Finance Practice application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from typing import Optional

from src.models.question import Question, TestResult
from src.models.timer import Timer
from src.utils.latex_renderer import LaTeXRenderer


class MathLabel(tk.Label):
    """Custom label that renders LaTeX math expressions"""

    def __init__(self, parent, text: str, use_latex: bool = True, **kwargs):
        super().__init__(parent, text="", **kwargs)
        self.use_latex = use_latex
        self.latex_renderer = LaTeXRenderer()
        self.set_text(text)

    def set_text(self, text: str):
        """Set the text, rendering as LaTeX if needed"""
        if self.use_latex and self._contains_math(text):
            try:
                # Convert to LaTeX format
                latex_text = self.latex_renderer.format_question_latex(text)
                photo_image = self.latex_renderer.render_math_expression(latex_text)
                self.config(image=photo_image)
                self.image = photo_image  # Keep a reference
                self.config(text="")
            except:
                # Fallback to plain text
                self.config(image="")
                self.config(text=text)
        else:
            self.config(image="")
            self.config(text=text)

    def _contains_math(self, text: str) -> bool:
        """Check if text contains mathematical expressions"""
        math_indicators = ['+', '-', '×', '÷', '=', '/', '\\', '%', 'fraction']
        return any(indicator in text for indicator in math_indicators)

    def cleanup(self):
        """Clean up resources"""
        if self.latex_renderer:
            self.latex_renderer.cleanup()


class MainMenu(tk.Frame):
    """Main menu frame"""

    def __init__(self, app):
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
    """Test screen frame with centered LaTeX questions"""

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.latex_renderer = LaTeXRenderer()
        self.question_label = None

        # Top bar
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.mode_label = tk.Label(top_frame, text="", font=("Arial", 12))
        self.mode_label.pack(side="left")

        self.timer_label = tk.Label(top_frame, text="", font=("Arial", 12, "bold"))
        self.timer_label.pack(side="right")

        self.progress_label = tk.Label(top_frame, text="", font=("Arial", 12))
        self.progress_label.pack()

        # Main content frame with centering
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Question container (centered)
        question_container = tk.Frame(main_frame)
        question_container.pack(expand=True)

        self.index_label = tk.Label(question_container, text="", font=("Arial", 14))
        self.index_label.pack(pady=(0, 20))

        # Math question label (centered)
        self.question_label = MathLabel(
            question_container,
            text="",
            use_latex=True,
            font=("Arial", 16),
            wraplength=600,
            justify="center"
        )
        self.question_label.pack(pady=20)

        # Options frame (centered)
        options_container = tk.Frame(question_container)
        options_container.pack(pady=20)

        self.option_labels = []
        for i in range(5):
            label = tk.Label(options_container, text="", font=("Arial", 12))
            label.pack(pady=2)
            self.option_labels.append(label)

        # Answer dropdown
        self.answer_var = tk.StringVar(value="Select Answer")
        self.answer_dropdown = ttk.Combobox(
            question_container, textvariable=self.answer_var,
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

        # Update question with LaTeX rendering
        if question.meta.get("latex", False):
            self.question_label.set_text(question.prompt)
        else:
            self.question_label.config(text=question.prompt)

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

    def cleanup(self):
        """Clean up resources"""
        if self.question_label:
            self.question_label.cleanup()
        if self.latex_renderer:
            self.latex_renderer.cleanup()


class ResultsScreen(tk.Frame):
    """Results screen frame"""

    def __init__(self, app):
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
            from src.modes.base import BaseMode
            from src.modes.numeric import NumericTestMode
            from src.modes.sequence import SequenceTestMode

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
    """Review screen frame with LaTeX rendering"""

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.current_review_index = 0
        self.latex_renderer = LaTeXRenderer()

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

        # Add LaTeX rendering for question if needed
        if question.meta.get("latex", False):
            try:
                latex_text = self.latex_renderer.format_question_latex(question.prompt)
                self.text_area.insert("end", f"LaTeX: {latex_text}\n\n", "latex")
            except:
                pass

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
        self.text_area.tag_config("latex", font=("Courier", 10, "italic"), foreground="blue")
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
        from src.modes.base import BaseMode

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

    def cleanup(self):
        """Clean up resources"""
        if self.latex_renderer:
            self.latex_renderer.cleanup()