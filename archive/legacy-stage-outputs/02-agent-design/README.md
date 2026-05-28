# Simple Statistics Calculator

A command-line application that calculates basic statistics (mean, median, mode) from a list of numbers.

## Features

- Calculates mean, median, and mode
- Handles both integers and decimal numbers
- Graceful error handling
- Clear, formatted output

## Usage

```bash
python main.py 1 2 3 4 5
```

## Example Output

```
Numbers: [1.0, 2.0, 3.0, 4.0, 5.0]
Mean: 3.0
Median: 3.0
Mode: [1.0, 2.0, 3.0, 4.0, 5.0]
```

## Requirements

- Python 3.6+

## Installation

No installation required - just run the script directly.

## Testing

Run tests with:

```bash
python -m unittest tests/test_calculator.py
```