# Quant Finance Practice Game (Version 2.0)

A comprehensive quantitative finance interview practice application with **LaTeX math rendering** and **centered question display**. This modular application helps you sharpen your mental math skills and pattern recognition abilities through timed tests with detailed review features.

## 🎯 Features

### 🧮 **Two Test Modes**
- **Numeric Test**: 50 questions in 6 minutes covering:
  - Integer arithmetic (+, -, ×, ÷)
  - Decimal arithmetic (1-3 decimal places)
  - Fraction operations (including mixed fractions)
  - Percentage calculations
- **Sequence Test**: 40 questions in 5 minutes covering:
  - Arithmetic sequences
  - Geometric sequences
  - Polynomial patterns (n², n³)
  - Alternating/interleaved sequences
  - Fibonacci-style sequences

### ✨ **LaTeX Math Rendering** (NEW)
- **Beautiful mathematical expressions** rendered using matplotlib
- Professional fraction notation: $\frac{3}{4} + \frac{2}{3} = ?$
- Mixed fractions: $1\frac{3}{4} \times 2\frac{1}{2} = ?$
- Percentage calculations: $25\% \text{ of } 200 = ?$
- Clean, readable mathematical formatting

### 🎯 **Centered Question Display** (NEW)
- **Professional layout** with questions centered in the interface
- Enhanced readability with proper spacing and alignment
- Modern, clean visual design
- Improved focus on the mathematical content

### ⏱️ **Timer Options**
- **Timed Mode**: Automatic submission when time expires
- **Practice Mode**: No time limit, shows elapsed time
- Visual countdown with color coding (red when under 1 minute)

### 📊 **Comprehensive Review**
- Detailed results showing total score, correct, incorrect, and unanswered questions
- Question-by-question review with explanations
- Error classification (off-by-one, decimal-place, fraction-reduction, etc.)
- CSV export for detailed analysis

### 🎯 **Smart Features**
- Deterministic sessions with optional seed for reproducible practice
- Intelligent distractor generation based on common mistakes
- Question shuffling to prevent memorization
- "Re-drill my mistakes" mode for focused practice
- Keyboard shortcuts for efficient navigation

## 📁 Project Structure

```
Quant_OA/
├── main.py                 # Main entry point
├── run.sh                  # Launcher script
├── requirements.txt        # Dependencies
├── README.md              # This file
├── src/
│   ├── app.py             # Main application class
│   ├── models/            # Data models
│   │   ├── question.py    # Question and TestResult classes
│   │   └── timer.py       # Timer functionality
│   ├── generators/        # Question generators
│   │   ├── base.py        # Base generator class
│   │   ├── numeric.py     # Numeric question generator
│   │   └── sequence.py    # Sequence question generator
│   ├── gui/               # GUI components
│   │   └── components.py  # All GUI frames and widgets
│   ├── modes/             # Test modes
│   │   ├── base.py        # Base mode class
│   │   ├── numeric.py     # Numeric test mode
│   │   └── sequence.py    # Sequence test mode
│   └── utils/             # Utilities
│       └── latex_renderer.py  # LaTeX rendering functionality
└── quant_finance_practice.py  # Original single-file version (legacy)
```

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Tkinter (included with most Python installations)

### Setup
1. Clone or download the repository
2. Create and activate a virtual environment:
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip3.11 install -r requirements.txt
```

4. Make the launcher executable:
```bash
chmod +x run.sh
```

## 🎮 Usage

### Basic Usage
```bash
# Run with the launcher script
./run.sh

# Or directly with Python
python3.11 main.py

# Run with a specific seed for reproducible sessions
python3.11 main.py --seed 12345

# Run self-test
python3.11 main.py --selftest
```

### Command Line Options
```bash
# Use a specific seed for reproducible sessions
python3.11 main.py --seed 12345

# Run self-test and exit
python3.11 main.py --selftest
```

### Interface Navigation
- **Mouse**: Click buttons and dropdowns to navigate
- **Keyboard Shortcuts**:
  - `←` : Previous question
  - `→` or `Enter` : Next question
  - `Ctrl/Cmd+F` : Finish test

### Test Workflow
1. **Main Menu**: Choose test mode and options
2. **Test Screen**: Answer questions using the dropdown
3. **Results Screen**: View your overall performance
4. **Review Screen**: Analyze each question with explanations

## 📖 Question Types

### Numeric Questions

#### Integer Arithmetic
Basic operations with integers displayed as LaTeX:
- Addition: $23 + 45 = ?$
- Subtraction: $87 - 34 = ?$
- Multiplication: $12 \times 8 = ?$
- Division: $144 \div 12 = ?$

#### Decimal Arithmetic
Operations with decimal numbers (1-3 decimal places):
- $12.34 + 45.67 = ?$
- $89.50 - 23.75 = ?$
- $3.14 \times 2.5 = ?$

#### Fraction Arithmetic
Operations with proper and improper fractions (LaTeX formatted):
- $\frac{3}{4} + \frac{2}{3} = ?$
- $\frac{7}{8} - \frac{1}{4} = ?$
- $\frac{2}{3} \times \frac{3}{4} = ?$
- $\frac{3}{4} \div \frac{1}{2} = ?$

#### Mixed Fractions
Operations with mixed numbers (LaTeX formatted):
- $1\frac{3}{4} + 2\frac{1}{2} = ?$
- $3\frac{3}{4} - 1\frac{1}{4} = ?$

#### Percentages
Common percentage calculations (LaTeX formatted):
- $25\% \text{ of } 200 = ?$
- $12.5\% \text{ of } 800 = ?$
- $6.25\% \text{ of } 1600 = ?$

### Sequence Questions

#### Arithmetic Sequences
Constant difference between terms:
- $3, 7, 11, 15, 19, ?$ (Answer: 23, difference = 4)

#### Geometric Sequences
Constant ratio between terms:
- $2, 6, 18, 54, 162, ?$ (Answer: 486, ratio = 3)

#### Polynomial Patterns
Square or cube patterns:
- $4, 9, 16, 25, 36, ?$ (Answer: 49, n² pattern starting from 2²)
- $1, 8, 27, 64, 125, ?$ (Answer: 216, n³ pattern starting from 1³)

#### Alternating Sequences
Two interleaved patterns:
- $2, 8, 4, 10, 6, 12, ?$ (Answer: 8, odd positions +2, even positions +2)

#### Fibonacci-style
Each term is sum of two preceding terms:
- $3, 5, 8, 13, 21, ?$ (Answer: 34)

## 📊 Scoring System

- **Correct Answer**: +1 point
- **Incorrect Answer**: -1 point
- **Unanswered**: 0 points

Score is only shown at the end to prevent test-taking anxiety.

## 🏷️ Error Classification

The application automatically categorizes common mistakes:

| Error Type | Description | Example |
|------------|-------------|---------|
| off-by-one | Answer is one unit away from correct | $23$ instead of $24$ |
| decimal-place | Decimal point is misplaced | $12.3$ instead of $1.23$ |
| fraction-reduction | Errors in fraction operations | $\frac{5}{8}$ instead of $\frac{3}{4}$ |
| wrong-ratio | Incorrect ratio in geometric sequences | $486$ instead of $162$ |
| interleave-swap | Confusing patterns in alternating sequences | Applying wrong rule |
| fib-near | Near-correct Fibonacci calculations | $33$ instead of $34$ |

## 📈 CSV Export Format

Export your results for detailed analysis:

```csv
question,A,B,C,D,E,correct,chosen,correctness,time_spent,error_tag
"12.34 + 45.67 = ?","58.01","58.02","58.03","58.04","58.05","A","A","Correct","",""
```

Fields:
- `question`: The question prompt (LaTeX formatted)
- `A,B,C,D,E`: All answer options
- `correct`: Correct answer letter
- `chosen`: Your selected answer
- `correctness`: Correct/Incorrect/Unanswered
- `time_spent`: Time per question (future feature)
- `error_tag`: Automatic error classification

## 📚 Study Plan Recommendations

### Daily Practice
- Complete one short run of each mode (numeric and sequence)
- Track your score, time remaining, and most frequent error types

### Weekly Focus
- Identify your top error type from the review screen
- Complete 3 re-drill sessions focusing on mistakes (~10 minutes each)

### Micro-techniques
- **Decimals**: Multiply as integers, then place decimal point based on total places
- **Fractions**: Remember $\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \times \frac{d}{c}$ and reduce early using GCD
- **Percentages**: Memorize common fraction equivalents (12.5% = $\frac{1}{8}$, 6.25% = $\frac{1}{16}$)
- **Sequences**: State the pattern before answering; if uncertain, skip and return

## 🔧 Advanced Features

### Deterministic Sessions
Use seeds to create reproducible test sessions:
```bash
python3.11 main.py --seed 12345
```
This ensures the same questions, order, and options every time - perfect for comparing performance or creating practice tests.

### Practice Mode
Turn on Practice Mode to:
- Remove time pressure
- See elapsed time instead of countdown
- Focus on accuracy and understanding

### Re-drill Mode
After completing a test, use "Re-drill my mistakes" to:
- Practice only questions you got wrong or skipped
- Focus on your weak areas
- Build confidence with targeted practice

## 🏗️ Technical Architecture

### Design Principles
- **Separation of Concerns**: Clear separation between data, logic, and presentation
- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add new question types and modes
- **Maintainability**: Clean, readable code with proper documentation

### Key Components

#### Data Models (`src/models/`)
- `Question`: Represents a single question with metadata
- `TestResult`: Stores test results and statistics
- `Timer`: Handles countdown and elapsed time functionality

#### Question Generators (`src/generators/`)
- `NumericQuestionFactory`: Generates arithmetic problems
- `SequenceQuestionFactory`: Generates pattern recognition problems
- LaTeX integration for mathematical expressions

#### GUI Components (`src/gui/`)
- `MainMenu`: Main menu with options and settings
- `TestScreen`: Test interface with centered LaTeX questions
- `ResultsScreen`: Results display and export options
- `ReviewScreen`: Detailed answer review with explanations
- `MathLabel`: Custom widget for LaTeX rendering

#### Test Modes (`src/modes/`)
- `BaseMode`: Abstract base class for test modes
- `NumericTestMode`: Numeric test configuration
- `SequenceTestMode`: Sequence test configuration

#### Utilities (`src/utils/`)
- `LaTeXRenderer`: Handles mathematical expression rendering
- Integration with matplotlib for high-quality output

## 🐛 Troubleshooting

### Common Issues

#### LaTeX Rendering Issues
- **Ensure dependencies are installed**: `pip3.11 install -r requirements.txt`
- **Check matplotlib availability**: Make sure matplotlib and Pillow are properly installed
- **Font issues**: On some systems, ensure fonts are available for LaTeX rendering

#### Tkinter Not Found
If you get an error about Tkinter not being found:
- **macOS**: Install Python from python.org (includes Tkinter)
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Windows**: Tkinter is included with Python installations

#### Window Not Appearing
- Check that the script is running without errors
- Try running from command line instead of double-clicking
- Ensure virtual environment is activated

#### Performance Issues
- LaTeX rendering may be slower initially but images are cached
- The application is optimized for standard test sizes
- Timer precision is 1-second intervals, suitable for test timing

### Getting Help
- Check the console for error messages
- Ensure Python 3.10+ is being used
- Run the self-test: `python3.11 main.py --selftest`
- Verify all dependencies are installed: `pip3.11 install -r requirements.txt`

## 🤝 Contributing

The application is designed to be easily extensible:

### Adding New Question Types
1. Create a new generator class in `src/generators/`
2. Inherit from `QuestionGenerator`
3. Implement the `generate_question()` method
4. Add to appropriate test mode

### Adding New Test Modes
1. Create a new mode class in `src/modes/`
2. Inherit from `BaseMode`
3. Implement required abstract methods
4. Add to main application menu

### Development Guidelines
1. Maintain the modular architecture
2. Use proper type hints and documentation
3. Follow the existing class hierarchy
4. Preserve deterministic behavior with seeds
5. Test with the `--selftest` flag
6. Ensure LaTeX rendering works for new question types

## 📝 Changelog

### Version 2.0 (Current)
- ✨ **Added LaTeX math rendering** for all questions
- ✨ **Centered question display** for better readability
- 🏗️ **Complete code refactoring** into modular architecture
- 🔧 **Improved error categorization** and analysis
- 📱 **Enhanced GUI** with MathLabel widget
- 🧹 **Clean separation of concerns** across modules
- 📚 **Updated documentation** and project structure

### Version 1.0 (Legacy)
- Basic numeric and sequence questions
- Simple tkinter interface
- CSV export functionality
- Timer and review system

## 📄 License

This project is maintained for educational and interview preparation purposes.

---

**Author**: Abhigya Koirala
**Version**: 2.0
**Last Updated**: 2025

## 🙏 Acknowledgments

Designed following quantitative finance interview preparation best practices. The question generation algorithms create realistic distractors based on common mathematical mistakes observed in interview settings. LaTeX rendering provides professional mathematical notation for enhanced learning experience.