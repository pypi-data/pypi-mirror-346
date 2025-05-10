# TextInsights

[![Python Tests](https://github.com/ksg-dev/textinsights/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ksg-dev/textinsights/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/textinsights.svg)](https://pypi.org/project/textinsights/)

A Python package for text analysis and visualization. TextInsights provides simple yet powerful tools for analyzing text data, calculating statistics, and understanding content insights.

## Installation

```bash
pip install textinsights
```

## Quick Start

```python
from textinsights import TextAnalyzer

# Create an analyzer with your text
text = "TextInsights makes text analysis easy and efficient!"
analyzer = TextAnalyzer(text)

# Get basic statistics
print(f"Word count: {analyzer.word_count()}")
# Output: Word count: 7

print(f"Unique words: {len(analyzer.unique_words())}")
# Output: Unique words: 7

print(f"Average word length: {analyzer.avg_word_length():.2f}")
# Output: Average word length: 6.71
```

## Features

- **Text Analysis**: Word counts, unique words, average word length
- **Statistical Analysis**: Word frequency, distribution metrics
- **Sentiment Analysis**: Basic sentiment scoring
- **Easy API**: Simple, intuitive interface for text processing
- **Extensible**: Build your own analyzers on top of the framework

## Usage Examples

### Basic Text Analysis

```python
from textinsights import TextAnalyzer

text = """Python is a programming language that lets you work quickly and
integrate systems more effectively. Python is easy to learn, yet powerful
and versatile. Many developers love Python for its simplicity and readability."""

analyzer = TextAnalyzer(text)

# Basic statistics
print(f"Word count: {analyzer.word_count()}")
print(f"Unique words: {len(analyzer.unique_words())}")
print(f"Average word length: {analyzer.avg_word_length():.2f}")

# Output:
# Word count: 30
# Unique words: 26
# Average word length: 4.77
```

### Word Frequency Analysis

```python
from textinsights import word_frequency

text = "Python is amazing. Python is versatile. Python is Python."
frequencies = word_frequency(text)

# Get the most common words
print(frequencies.most_common(3))
# Output: [('python', 3), ('is', 3), ('amazing', 1)]

# Check frequency of a specific word
print(f"Frequency of 'python': {frequencies['python']}")
# Output: Frequency of 'python': 3
```

### Sentiment Analysis

```python
from textinsights import sentiment_score

# Using default positive/negative word lists
text1 = "I love this product. It's excellent and amazing!"
score1 = sentiment_score(text1)
print(f"Sentiment score 1: {score1:.2f}")
# Output: Sentiment score 1: 1.00

text2 = "This is terrible and disappointing. I hate it."
score2 = sentiment_score(text2)
print(f"Sentiment score 2: {score2:.2f}")
# Output: Sentiment score 2: -1.00

text3 = "The product has good features but also some bad aspects."
score3 = sentiment_score(text3)
print(f"Sentiment score 3: {score3:.2f}")
# Output: Sentiment score 3: 0.00

# Using custom word lists
positive_words = ['efficient', 'fast', 'innovative']
negative_words = ['slow', 'complicated', 'buggy']

text4 = "The system is efficient and fast, but slightly complicated."
score4 = sentiment_score(text4, positive_words, negative_words)
print(f"Custom sentiment score: {score4:.2f}")
# Output: Custom sentiment score: 0.33
```

## Project Structure

```
textinsights/
├── textinsights/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── stats.py
│   └── visualizer.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   └── test_stats.py
├── setup.py
├── README.md
├── LICENSE
└── .gitignore
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/ksg-dev/textinsights.git
cd textinsights

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=textinsights
```

## Contributing

Contributions are welcome! Please check out our [contributing guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

## Roadmap

- Add advanced NLP features (tokenization, lemmatization)
- Implement text classification capabilities
- Add more visualization options
- Support for multiple languages
- Integration with popular NLP libraries

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use TextInsights in your research, please cite:

```
@software{textinsights2025,
  author = {ksg-dev},
  title = {TextInsights: A Python package for text analysis and visualization},
  year = {2025},
  url = {https://github.com/ksg-dev/textinsights}
}
```

## Contact

ksg-dev - ksg.dev.data@gmail.com

Project Link: [https://github.com/ksg-dev/textinsights](https://github.com/ksg-dev/textinsights)