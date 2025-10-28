"""
LaTeX math rendering utilities for the Quant Finance Practice application.
"""

import matplotlib.pyplot as plt
import matplotlib
import io
from PIL import Image, ImageTk
import tkinter as tk
import re
import tempfile
import os

# Set matplotlib to use a non-interactive backend
matplotlib.use('Agg')
plt.rcParams.update({
    'font.size': 14,
    'mathtext.fontset': 'cm',
    'mathtext.default': 'regular'
})


class LaTeXRenderer:
    """Handles LaTeX math rendering for questions"""

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def render_math_expression(self, expression: str, dpi: int = 150) -> ImageTk.PhotoImage:
        """
        Render a mathematical expression as a LaTeX image.

        Args:
            expression: The mathematical expression to render
            dpi: Resolution for the rendered image

        Returns:
            PhotoImage object that can be used in tkinter
        """
        try:
            # Create figure with transparent background
            fig, ax = plt.subplots(figsize=(8, 2), facecolor='none')
            ax.axis('off')

            # Render the LaTeX expression
            ax.text(0.5, 0.5, f'${expression}$',
                   fontsize=16, ha='center', va='center',
                   transform=ax.transAxes)

            # Save to memory buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                       facecolor='none', edgecolor='none', pad_inches=0.1, transparent=True)
            plt.close(fig)
            buf.seek(0)

            # Convert to PIL Image and then to PhotoImage
            pil_image = Image.open(buf)
            photo_image = ImageTk.PhotoImage(pil_image)

            buf.close()
            return photo_image

        except Exception as e:
            # Fallback to plain text if LaTeX rendering fails
            return self._render_text_fallback(expression)

    def render_text_fallback(self, text: str) -> ImageTk.PhotoImage:
        """
        Fallback text rendering when LaTeX fails.
        """
        try:
            fig, ax = plt.subplots(figsize=(8, 1.5), facecolor='none')
            ax.axis('off')

            ax.text(0.5, 0.5, text, fontsize=16, ha='center', va='center',
                   transform=ax.transAxes, family='monospace')

            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                       facecolor='none', edgecolor='none', pad_inches=0.1, transparent=True)
            plt.close(fig)
            buf.seek(0)

            pil_image = Image.open(buf)
            photo_image = ImageTk.PhotoImage(pil_image)

            buf.close()
            return photo_image

        except Exception:
            # Create a simple text image as last resort
            from PIL import ImageDraw, ImageFont

            img = Image.new('RGBA', (400, 60), color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                font = ImageFont.load_default()

            draw.text((200, 30), text, font=font, fill='black', anchor='mm')
            return ImageTk.PhotoImage(img)

    def format_question_latex(self, prompt: str) -> str:
        """
        Convert a plain text question to LaTeX format.
        """
        # Replace multiplication symbol
        latex_prompt = prompt.replace('×', r'\times')
        latex_prompt = latex_prompt.replace('÷', r'\div')

        # Replace common math patterns with LaTeX
        latex_prompt = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', latex_prompt)

        # Handle mixed numbers like "2 3/4"
        latex_prompt = re.sub(r'(\d+)\s+(\d+)/(\d+)', r'\\frac{\1\\times\3 + \2}{\3}', latex_prompt)

        # Replace percentage symbols
        latex_prompt = latex_prompt.replace('%', r'\%')

        # Add LaTeX math mode markers around expressions
        latex_prompt = re.sub(r'(\d+\s*[+\-×÷]\s*\d+[^=\n]*=)', r'$\1$', latex_prompt)
        latex_prompt = re.sub(r'(\d+% of \d+ =)', r'$\1$', latex_prompt)

        return latex_prompt

    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass