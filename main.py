#!/usr/bin/env python3
"""
Quant Finance Numeracy & Sequences Practice Game
A quantitative finance interview practice game with LaTeX rendering and centered questions.

Author: Abhigya Koirala
Version: 2.0
"""

import argparse
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import App


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Quant Finance Practice Game")
    parser.add_argument("--seed", type=int, help="Random seed for reproducible sessions")
    parser.add_argument("--selftest", action="store_true", help="Run self-test and exit")

    args = parser.parse_args()

    app = App(seed=args.seed, selftest=args.selftest)

    try:
        app.mainloop()
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()