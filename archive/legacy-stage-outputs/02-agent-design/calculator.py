"""
Calculator module for statistics operations.

This module provides functions to calculate basic statistics from a list of numbers.
"""

from collections import Counter


def calculate_mean(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.
    
    Args:
        numbers (list): List of numbers
    
    Returns:
        float: The mean value
    """
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """
    Calculate the median of a list of numbers.
    
    Args:
        numbers (list): List of numbers
    
    Returns:
        float: The median value
    """
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 0:
        # Even number of elements - average of two middle values
        return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        # Odd number of elements - middle value
        return sorted_numbers[n//2]


def calculate_mode(numbers):
    """
    Calculate the mode (most frequent value) of a list of numbers.
    
    Args:
        numbers (list): List of numbers
    
    Returns:
        list: List of mode values (can be multiple if tied)
    """
    counter = Counter(numbers)
    max_count = max(counter.values())
    modes = [num for num, count in counter.items() if count == max_count]
    
    # Return sorted list of modes
    return sorted(modes)


def validate_input(numbers):
    """
    Validate that input contains valid numbers.
    
    Args:
        numbers (list): List of numbers to validate
    
    Raises:
        ValueError: If input is invalid
    """
    if not numbers:
        raise ValueError("No numbers provided")
    
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise ValueError(f"Invalid number: {num}")