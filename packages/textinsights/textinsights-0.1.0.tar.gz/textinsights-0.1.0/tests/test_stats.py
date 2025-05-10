# Copyright (c) 2025 ksg-dev. Licensed under the MIT License.
# See LICENSE for details.

import pytest
from collections import Counter
from textinsights.stats import word_frequency, sentiment_score


class TestWordFrequency:
    """Test suite for the word_frequency function."""

    @pytest.fixture
    def sample_text(self):
        """Fixture providing sample text for word frequency testing."""
        return "apple banana apple orange banana apple"

    @pytest.fixture
    def complex_text(self):
        """Fixture providing more complex text with puntuation and cases."""
        return """The quick brown fox jumps over the lazy dog.
        The quick brown fox is quick indeed! Fox fox FOX."""

    @pytest.fixture(params=["apple", "apple apple", "apple banana apple", ""])
    def various_texts(self, request):
        """Parametrized fixture providing different text examples."""
        return request.param

    def test_basic_frequency(self, sample_text):
        """Test basic word frequency counting using fixture."""

        freq = word_frequency(sample_text)
        assert isinstance(freq, Counter)
        assert freq["apple"] == 3
        assert freq["banana"] == 2
        assert freq["orange"] == 1

    @pytest.mark.parametrize("text,expected_counts", [
        ("apple banana apple", {"apple": 2, "banana": 1}),
        ("test test test", {"test": 3}),
        ("ONE one One", {"one": 3}),  # Case insensitive
        ("", {}),
        ("single", {"single": 1}),  # Single word
        ("with   spaces", {"with": 1, "spaces": 1})  # Multiple spaces
    ])
    def test_frequency_with_parameters(self, text, expected_counts):
        """Test word frequency with various inputs."""

        freq = word_frequency(text)

        # Check all expected counts
        for word, count in expected_counts.items():
            assert freq[word] == count

        # Ensure no extra words are counted
        assert sum(freq.values()) == sum(expected_counts.values())

    def test_case_insensitivity(self):
        """Test that word frequency is case-insensitive."""

        text = "Apple apple APPLE aPpLe"
        freq = word_frequency(text)
        assert freq["apple"] == 4
        assert len(freq) == 1  # Only one unique word (case-insensitive)

    def test_empty_text(self):
        """Test that empty text returns empty Counter."""

        freq = word_frequency("")
        assert isinstance(freq, Counter)
        assert len(freq) == 0

    def test_various_texts_fixture(self, various_texts):
        """Test using parametrized fixture."""

        freq = word_frequency(various_texts)

        if various_texts == "":
            assert len(freq) == 0
        else:
            # Word count should match expected patterns
            words = various_texts.lower().split()
            assert sum(freq.values()) == len(words)

    @pytest.mark.parametrize("text", [
        "word1 word2 word3",
        "repeated repeated repeated",
        "MiXeD cAsE tExT"
    ])
    @pytest.mark.parametrize("transformation", ["upper", "lower", "title"])
    def test_case_transformations(self, text, transformation):
        """Test word frequency with different case transformations."""

        if transformation == "upper":
            transformed_text = text.upper()
        elif transformation == "lower":
            transformed_text = text.lower()
        else:  # Title
            transformed_text = text.title()

        # Original and transformed text should have some frequency patterns
        freq_original = word_frequency(text)
        freq_transformed = word_frequency(transformed_text)

        assert sum(freq_original.values()) == sum(freq_transformed.values())

    def test_most_common_words(self, sample_text):
        """Test finding most common words."""

        freq = word_frequency(sample_text)
        most_common = freq.most_common(2)

        assert most_common[0] == ("apple", 3)
        assert most_common[1] == ("banana", 2)

    @pytest.mark.skipif(True, reason="Punctuation handling not implemented")
    def test_punctuation_handling(self):
        """Test how punctuation is handled in word frequency."""

        text = "Hello, world! Hello again."
        freq = word_frequency(text)
        # This test might fail if punctuation isn't stripped
        assert freq["hello"] == 2
        assert freq["world"] == 1


class TestSentimentScore:
    """Test suite for the sentiment_score function."""

    @pytest.fixture
    def default_positive_words(self):
        """Fixture providing default positive words list."""
        return ['good', 'great', 'excellent', 'happy', 'like', 'love']

    @pytest.fixture
    def default_negative_words(self):
        """Fixture providing default negative words list."""
        return ['bad', 'terrible', 'awful', 'sad', 'hate', 'dislike']

    @pytest.fixture
    def custom_words_lists(self):
        """Fixture providing custom positive and negative word lists."""
        return {
            'positive': ['amazing', 'brilliant', 'wonderful'],
            'negative': ['horrible', 'dreadful', 'poor']
        }

    @pytest.fixture(params=[
        ("good excellent happy love", 1.0),
        ("bad terrible awful sad", -1.0),
        ("good bad good bad", 0.0),
        ("neutral text here", 0.0),
        ("", 0.0)
    ])
    def sentiment_test_cases(self, request):
        """Parametrized fixture with sentiment test cases."""
        return request.param

    def test_positive_sentiment(self):
        """Test text with positive sentiment."""

        text = "good excellent happy love"
        score = sentiment_score(text)
        assert score == 1.0

    def test_negative_sentiment(self):
        """Test text with negative sentiment."""

        text = "bad terrible awful sad hate"
        score = sentiment_score(text)
        assert score == -1.0

    @pytest.mark.parametrize("text,expected_score", [
        ("good excellent happy love", 1.0),
        ("bad terrible awful sad", -1.0),
        ("good bad good bad", 0.0),
        ("good good bad", 0.33),
        ("good bad bad", -0.33),
        ("neutral words only", 0.0),
        ("", 0.0),
        ("GOOD BAD", 0.0),
        ("    good     bad  ", 0.0)
    ])
    def test_sentiment_scores_parametrized(self, text, expected_score):
        """Test sentiment_score with various inputs."""
        score = sentiment_score(text)
        assert pytest.approx(score, 0.01) == expected_score

    def test_custom_words_list(self, custom_words_lists):
        """Test with custom positive and negative word lists."""

        text = "amazing horrible wonderful poor"

        # Test with custom lists
        score = sentiment_score(
            text,
            positive_words=custom_words_lists['positive'],
            negative_words=custom_words_lists['negative']
            )
        # 2 positive 2 negative = 0.0
        assert score == 0.0

    def test_partial_custom_lists(self):
        """Test with only one custom word list."""
        text = "good bad terrible wonderful"

        # Only custom positive words
        score_custom_pos = sentiment_score(
            text,
            positive_words=['wonderful'],
            negative_words=None  # Use defaults
        )

        # Only custom negative words
        score_custom_neg = sentiment_score(
            text,
            positive_words=None,  # Use defaults
            negative_words=['terrible']
        )

        # Results should differ
        assert score_custom_pos != score_custom_neg

    def test_sentiment_test_cases_fixture(self, sentiment_test_cases):
        """Test using parametrized fixture with test cases."""
        text, expected_score = sentiment_test_cases
        score = sentiment_score(text)
        assert score == expected_score

    @pytest.mark.parametrize("positive_words", [
        ['good', 'great'],
        ['amazing', 'wonderful', 'fantastic'],
        ['love']
    ])
    @pytest.mark.parametrize("negative_words", [
        ['bad', 'terrible'],
        ['awful', 'horrible', 'dreadful'],
        ['hate']
    ])
    def test_different_word_lists_combos(self, positive_words, negative_words):
        """Test with different combinations of word lists."""
        # Create text with words from both lists
        pos_word = positive_words[0]
        neg_word = negative_words[0]

        text_positive = f"{pos_word} {pos_word}"
        text_negative = f"{neg_word} {neg_word}"
        text_mixed = f"{pos_word} {neg_word}"

        score_positive = sentiment_score(
            text_positive, positive_words, negative_words
        )
        score_negative = sentiment_score(
            text_negative, positive_words, negative_words
        )
        score_mixed = sentiment_score(
            text_mixed, positive_words, negative_words
        )

        assert score_positive == 1.0
        assert score_negative == -1.0
        assert score_mixed == 0

    def test_case_insensitivity(self):
        """Test that sentiment analysis is case-insensitive."""
        text_lower = "good bad"
        text_upper = "GOOD BAD"
        text_mixed = "GoOd bAd"

        assert sentiment_score(text_lower) == sentiment_score(text_upper)
        assert sentiment_score(text_lower) == sentiment_score(text_mixed)

    @pytest.mark.xfail(reason="Float precision can cause issues")
    def test_precise_float_calculation(self):
        """Test precise float calculations in sentiment scoring."""
        text = "good good good bad bad"
        score = sentiment_score(text)
        # This might fail due to float precision
        assert score == 0.2  # 3 pos, 2 neg = (3-2)/5 = 0.2

    def test_repeated_words(self):
        """Test sentiment with repeated sentiment words."""
        text = "love love love hate"
        score = sentiment_score(text)
        # 3 positive, 1 negative = (3-1)/4 = 0.5
        assert pytest.approx(score, 0.01) == 0.5

    def test_empty_custom_word_lists(self):
        """Test with empty custom word lists."""
        text = "good bad excellent terrible"

        # Empty lists should result in neutral score
        score = sentiment_score(
            text, positive_words=[], negative_words=[]
        )
        assert score == 0.0
