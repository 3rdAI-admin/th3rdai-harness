# This is the main entry point of the application.
import sys

def calculate_statistics(numbers):
    mean = sum(numbers) / len(numbers)
    median = sorted(numbers)[len(numbers) // 2]
    mode = max(set(numbers), key=numbers.count)
    return {'mean': mean, 'median': median, 'mode': mode}

if __name__ == '__main__':
    try:
        numbers = list(map(float, sys.argv[1:]))
        stats = calculate_statistics(numbers)
        print(stats)
    except ValueError:
        print('Invalid input. Please provide a list of numbers.', file=sys.stderr)