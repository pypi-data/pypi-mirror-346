# Copyright (c) 2025 ksg-dev. Licensed under the MIT License.
# See LICENSE for details.

import pytest
from textinsights.analyzer import TextAnalyzer


class TestTextAnalyzer:
    """Test suite for the TextAnalyzer class."""

    @pytest.fixture
    def sample_analyzer(self):
        """Fixture providing sample TextAnalyzer instance."""

        return TextAnalyzer("This is a test sentence")

    @pytest.fixture
    def complex_analyzer(self):
        """Fixture providing a more complex text analyzer."""

        text = """Python is a programming language that lets you work quickly
        and integrate systems more effectively. Python is easy to learn."""
        return TextAnalyzer(text)

    @pytest.fixture(params=[
        "Hello world",
        "Python programming",
        "Test test test",
        ""
    ])
    def various_analyzers(self, request):
        """Fixture providing analyzers with different test texts."""
        return TextAnalyzer(request.param)

    def test_initialization(self):
        """Test that the analyzer initializes correctly."""

        sample_text = "This is a test sentence"
        analyzer = TextAnalyzer(sample_text)
        assert analyzer.text == sample_text
        assert analyzer.words == ["this", "is", "a", "test", "sentence"]

    def test_word_count_with_fixture(self, sample_analyzer):
        """Test the word_count method using a fixture."""
        assert sample_analyzer.word_count() == 5

    def test_unique_words_with_fixture(self, sample_analyzer):
        """Test unique_words method using a fixture."""
        unique_words = sample_analyzer.unique_words()
        assert len(unique_words) == 5
        assert "test" in unique_words
        assert "sentence" in unique_words

    @pytest.mark.parametrize("text,expected_count", [
        ("Hello world", 2),
        ("One two three four", 4),
        ("", 0),
        ("Single", 1),
        ("Multiple   spaces   here", 3),
        ("Test test test", 3)
    ])
    def test_word_count_parametrized(self, text, expected_count):
        """Test word_count method with various inputs."""

        analyzer = TextAnalyzer(text)
        assert analyzer.word_count() == expected_count

    @pytest.mark.parametrize("text,expected_unique", [
        ("test test test", 1),
        ("unique words only", 3),
        ("Case CASE cAsE", 1),
        ("", 0),
        ("one two three one two", 3)
    ])
    def test_unique_words_parametrized(self, text, expected_unique):
        """Test unique_words method with various inputs."""

        analyzer = TextAnalyzer(text)
        assert len(analyzer.unique_words()) == expected_unique

    @pytest.mark.parametrize("text,expected_avg", [
        ("four nine", 4.0),
        ("a bb ccc", 2.0),
        ("", 0),
        ("equal equal equal", 5.0),
        ("x", 1.0)
    ])
    def test_avg_word_length_parametrized(self, text, expected_avg):
        """Test avg_word method with various inputs."""
        analyzer = TextAnalyzer(text)
        assert analyzer.avg_word_length() == expected_avg

    # Test combining fixture and parametrization
    def test_complex_text(self, complex_analyzer):
        """Test analyzer with more complex text."""

        assert complex_analyzer.word_count() == 20
        assert "python" in complex_analyzer.unique_words()
        assert complex_analyzer.avg_word_length() > 4

    # Parametrized fixture usage
    def test_various_texts(self, various_analyzers):
        """Test with various text analyzers from parametrized fixture."""

        word_count = various_analyzers.word_count()
        unique_count = len(various_analyzers.unique_words())

        # Word count should always be >= unique word count
        assert word_count >= unique_count

        # Average word length should be 0 only for empty text
        if word_count == 0:
            assert various_analyzers.avg_word_length() == 0
        else:
            assert various_analyzers.avg_word_length() > 0

    # Advanced: Using multiple parametrize decorators
    @pytest.mark.parametrize("text", ["Hello", "World", "Testing"])
    @pytest.mark.parametrize("repeat", [1, 2, 3])
    def test_repeated_words(self, text, repeat):
        """Test w repeated words."""

        repeated_text = " ".join([text] * repeat)
        analyzer = TextAnalyzer(repeated_text)

        assert analyzer.word_count() == repeat
        assert len(analyzer.unique_words()) == 1
        assert analyzer.avg_word_length() == len(text.lower())

    # Testing edge cases
    @pytest.mark.parametrize("edge_case_test", [
        "  ",  # Only spaces
        "\n\n",  # Only newlines
        "\t\t",  # Only tabs
        "word\nword",  # Words w newline
        "word\tword"  # Words w tab
    ])
    def test_edge_cases(self, edge_case_test):
        """Test edge cases for text input."""

        analyzer = TextAnalyzer(edge_case_test)
        # Empty strings and whitespace should result in 0 words
        word_count = analyzer.word_count()

        # We expect certain behaviors for edge cases
        if edge_case_test.strip() == "":
            assert word_count == 0
            assert len(analyzer.unique_words()) == 0
        else:
            assert word_count > 0

    # Using fixtures with skip/xfail decorators
    @pytest.mark.skipif(
        True,  # You could replace w condition like sys.version_info < (3, 8)
        reason="Example of skipped test"
    )
    def test_future_feature(self, sample_analyzer):
        """Test for a feature not yet implemented."""

        # This test would be skipped
        pass

    @pytest.mark.xfail(reason="Known issue with punctuation handling")
    def test_punctuation_handling(self):
        """Test that currently fails but is known and expected."""

        analyzer = TextAnalyzer("hello, world! How are you?")
        # This might fail if punctuation isn't handled properly
        assert analyzer.word_count() == 5
        # Should consider if "hello," and "hello" are the same word
        assert "hello" in analyzer.unique_words()
