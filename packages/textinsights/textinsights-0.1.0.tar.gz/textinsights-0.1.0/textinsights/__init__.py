# Copyright (c) 2025 ksg-dev. Licensed under MIT License.
# See LICENSE for details

"""TextInsights: A package for text analysis and visualization"""

from .analyzer import TextAnalyzer
from .stats import word_frequency, sentiment_score

__version__ = "0.1.0"

# Define what should be available through 'from textinsights import *'
__all__ = ["TextAnalyzer", "word_frequency", "sentiment_score"]
