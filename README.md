# Quant Finance Practice Game

A comprehensive quantitative finance interview practice application built with Python and Tkinter. This single-file, object-oriented application helps you sharpen your mental math skills and pattern recognition abilities through timed tests with detailed review features.

## Features

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

## Installation

### Prerequisites
- Python 3.10 or higher
- Tkinter (included with most Python installations)

### Setup
1. Clone or download the repository
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. The application uses only Python standard library modules, so no additional packages need to be installed!

## Usage

### Basic Usage
```bash
python quant_finance_practice.py
```

### Command Line Options
```bash
# Use a specific seed for reproducible sessions
python quant_finance_practice.py --seed 12345

# Run self-test and exit
python quant_finance_practice.py --selftest
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

## Question Types

### Numeric Questions

#### Integer Arithmetic
Basic operations with integers:
- Addition: `23 + 45 = ?`
- Subtraction: `87 - 34 = ?`
- Multiplication: `12 × 8 = ?`
- Division: `144 ÷ 12 = ?`

#### Decimal Arithmetic
Operations with decimal numbers (1-3 decimal places):
- `12.34 + 45.67 = ?`
- `89.50 - 23.75 = ?`
- `3.14 × 2.5 = ?`

#### Fraction Arithmetic
Operations with proper and improper fractions:
- `3/4 + 2/3 = ?`
- `7/8 - 1/4 = ?`
- `2/3 × 3/4 = ?`
- `3/4 ÷ 1/2 = ?`

#### Mixed Fractions
Operations with mixed numbers:
- `2 1/4 + 1 1/2 = ?`
- `3 3/4 - 1 1/4 = ?`

#### Percentages
Common percentage calculations:
- `25% of 200 = ?`
- `12.5% of 800 = ?`
- `6.25% of 1600 = ?`

### Sequence Questions

#### Arithmetic Sequences
Constant difference between terms:
- `3, 7, 11, 15, 19, ?` (Answer: 23, difference = 4)

#### Geometric Sequences
Constant ratio between terms:
- `2, 6, 18, 54, 162, ?` (Answer: 486, ratio = 3)

#### Polynomial Patterns
Square or cube patterns:
- `4, 9, 16, 25, 36, ?` (Answer: 49, n² pattern starting from 2²)
- `1, 8, 27, 64, 125, ?` (Answer: 216, n³ pattern starting from 1³)

#### Alternating Sequences
Two interleaved patterns:
- `2, 8, 4, 10, 6, 12, ?` (Answer: 8, odd positions +2, even positions +2)

#### Fibonacci-style
Each term is sum of two preceding terms:
- `3, 5, 8, 13, 21, ?` (Answer: 34)

## Scoring System

- **Correct Answer**: +1 point
- **Incorrect Answer**: -1 point
- **Unanswered**: 0 points

Score is only shown at the end to prevent test-taking anxiety.

## Error Classification

The application automatically categorizes common mistakes:

| Error Type | Description | Example |
|------------|-------------|---------|
| off-by-one | Answer is one unit away from correct | `23` instead of `24` |
| decimal-place | Decimal point is misplaced | `12.3` instead of `1.23` |
| fraction-reduction | Errors in fraction operations | `5/8` instead of `3/4` |
| wrong-ratio | Incorrect ratio in geometric sequences | `486` instead of `162` |
| interleave-swap | Confusing patterns in alternating sequences | Applying wrong rule |
| fib-near | Near-correct Fibonacci calculations | `33` instead of `34` |

## CSV Export Format

Export your results for detailed analysis:

```csv
question,A,B,C,D,E,correct,chosen,correctness,time_spent,error_tag
"23 + 45 = ?","68","69","70","71","72","A","A","Correct","",""
```

Fields:
- `question`: The question prompt
- `A,B,C,D,E`: All answer options
- `correct`: Correct answer letter
- `chosen`: Your selected answer
- `correctness`: Correct/Incorrect/Unanswered
- `time_spent`: Time per question (future feature)
- `error_tag`: Automatic error classification

## Study Plan Recommendations

### Daily Practice
- Complete one short run of each mode (numeric and sequence)
- Track your score, time remaining, and most frequent error types

### Weekly Focus
- Identify your top error type from the review screen
- Complete 3 re-drill sessions focusing on mistakes (~10 minutes each)

### Micro-techniques
- **Decimals**: Multiply as integers, then place decimal point based on total places
- **Fractions**: Remember `a/b ÷ c/d = a/b × d/c` and reduce early using GCD
- **Percentages**: Memorize common fraction equivalents (12.5% = 1/8, 6.25% = 1/16)
- **Sequences**: State the pattern before answering; if uncertain, skip and return

## Advanced Features

### Deterministic Sessions
Use seeds to create reproducible test sessions:
```bash
python quant_finance_practice.py --seed 12345
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

## Technical Architecture

### Class Structure
- **App**: Main application controller
- **BaseMode**: Abstract base class for test modes
- **NumericTestMode**: Numeric questions implementation
- **SequenceTestMode**: Sequence questions implementation
- **Timer**: Flexible countdown/elapsed timer
- **Question**: Dataclass for question structure
- **QuestionGenerator**: Abstract base for question factories
- **NumericQuestionFactory**: Generates numeric questions
- **SequenceQuestionFactory**: Generates sequence questions

### UI Components
- **MainMenu**: Test selection and options
- **TestScreen**: Question display and answering
- **ResultsScreen**: Performance summary
- **ReviewScreen**: Detailed question analysis

### Design Principles
- **Single File**: Entire application in one Python file
- **Object-Oriented**: Clean separation of concerns
- **Standard Library Only**: No external dependencies
- **Deterministic**: Seed-based reproducibility
- **Accessible**: Clear fonts, consistent sizing, keyboard navigation

## Troubleshooting

### Common Issues

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
- The application is optimized for standard test sizes
- Larger question counts may show slight delays during generation
- Timer precision is 1-second intervals, suitable for test timing

### Getting Help
- Check the console for error messages
- Ensure Python 3.10+ is being used
- Verify all files are in the same directory

## Contributing

This project follows the POML (Prompt Object Markup Language) specification. When making changes:

1. Maintain the single-file structure
2. Use only Python standard library modules
3. Follow the existing class hierarchy
4. Preserve deterministic behavior with seeds
5. Test with the `--selftest` flag

## License

This project is provided as-is for educational and practice purposes.

## Acknowledgments

Designed following quantitative finance interview preparation best practices. The question generation algorithms create realistic distractors based on common mathematical mistakes observed in interview settings.