# Copyright (c) 2025 ksg-dev. Licensed under the MIT License.
# See LICENSE for details.

"""Core analyzer module for text processing"""


class TextAnalyzer:
    """Analyze text documents for various linguistic features."""

    def __init__(self, text):
        """Initialize with text content.

        Args:
            text (str): The text to analyze

        Example:
            >>> analyzer = TextAnalyzer("Wow this bon bon is delicious")

        """
        self.text = text
        self.words = text.lower().split()

    def word_count(self):
        """Count the total number of words.

        Returns:
            int: Total word count

        Example:
            >>> analyzer.word_count()
            6

        """
        return len(self.words)

    def unique_words(self):
        """Find unique words in the text.

        Returns:
            set: Set of unique words

        Example:
            >>> analyzer.unique_words()
            {'this', 'delicious', 'is', 'wow', 'bon'}

        """
        return set(self.words)

    def avg_word_length(self):
        """Calculate average word length.

        Returns:
            float: Average length of words

        Example:
            >>> analyzer.avg_word_length()
            4.0

        """
        if not self.words:
            return 0
        return sum(len(word) for word in self.words) / len(self.words)
