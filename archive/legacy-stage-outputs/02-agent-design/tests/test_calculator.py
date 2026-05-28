"""
Unit tests for the calculator module.
"""

import unittest
from calculator import calculate_mean, calculate_median, calculate_mode, validate_input


class TestCalculator(unittest.TestCase):
    
    def test_calculate_mean(self):
        self.assertEqual(calculate_mean([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(calculate_mean([10, 20]), 15.0)
        self.assertEqual(calculate_mean([1.5, 2.5]), 2.0)
        
    def test_calculate_median(self):
        self.assertEqual(calculate_median([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(calculate_median([1, 2, 3, 4]), 2.5)
        self.assertEqual(calculate_median([5, 1, 3, 2, 4]), 3.0)
        
    def test_calculate_mode(self):
        self.assertEqual(calculate_mode([1, 2, 2, 3]), [2])
        self.assertEqual(calculate_mode([1, 1, 2, 2]), [1, 2])
        self.assertEqual(calculate_mode([5, 5, 5, 5]), [5])
        
    def test_validate_input(self):
        # Valid inputs
        validate_input([1, 2, 3])
        validate_input([1.5, 2.5])
        
        # Invalid inputs
        with self.assertRaises(ValueError):
            validate_input([])
        
        with self.assertRaises(ValueError):
            validate_input([1, 2, 'three'])


if __name__ == '__main__':
    unittest.main()