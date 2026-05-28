#!/usr/bin/env python3

"""
Simple Statistics Calculator

This script calculates basic statistics (mean, median, mode) from a list of numbers.
"""

import argparse
import sys
from calculator import calculate_mean, calculate_median, calculate_mode, validate_input


def main():
    parser = argparse.ArgumentParser(description='Calculate basic statistics from a list of numbers')
    parser.add_argument('numbers', nargs='+', type=float, help='Numbers to calculate statistics for')
    
    try:
        args = parser.parse_args()
        numbers = args.numbers
        
        # Validate input
        validate_input(numbers)
        
        # Calculate statistics
        mean = calculate_mean(numbers)
        median = calculate_median(numbers)
        mode = calculate_mode(numbers)
        
        # Display results
        print(f"Numbers: {numbers}")
        print(f"Mean: {mean}")
        print(f"Median: {median}")
        print(f"Mode: {mode}")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()