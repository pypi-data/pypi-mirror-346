# Copyright (c) 2025 ksg-dev. Licensed under the MIT License.
# See LICENSE for details.

"""Statistical utilities for text analysis."""

from collections import Counter


def word_frequency(text):
    """Calculate frequency distribution of words.

    Args:
        text (str): The text to analyze

    Returns:
        Counter: Word frequency counts

    Example:
        >>> word_frequency("banana banana banana coconut coconut orange")
        Counter({'banana': 3, 'coconut': 2, 'orange': 1})

    """
    words = text.lower().split()
    return Counter(words)


def sentiment_score(text, positive_words=None, negative_words=None):
    """Calculate a sentiment score for the given text.

    The sentiment score is a value between -1.0 (completely negative)
    and 1.0 (completely positive), with 0.0 representing neutral sentiment.

    Args:
        text (str): The text to analyze
        positive_words (list, optional): List of positive words to use.
            Defaults to a basic set of positive words.
        negative_words (list, optional): List of negative words to use.
            Defaults to a basic set of negative words.

    Returns:
        float: A sentiment score between -1.0 and 1.0

    Example:
        >>> sentiment_score("I love this product!")
        1.0
        >>> sentiment_score("I hate this product!")
        -1.0
    """

    if positive_words is None:
        positive_words = [
            'good', 'great', 'excellent', 'happy', 'like', 'love'
            ]

    if negative_words is None:
        negative_words = ['bad', 'terrible', 'awful', 'sad', 'hate', 'dislike']

    words = text.lower().split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)

    total = positive_count + negative_count
    if total == 0:
        return 0

    return (positive_count - negative_count) / total
