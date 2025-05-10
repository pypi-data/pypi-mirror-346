"""Test the countpy module."""

# test_countpy.py
from collections import Counter
import matplotlib
import pytest
from countpy.countpy import count_words
from countpy.plotting import plot_words
from countpy.datasets import get_gatsby


@pytest.fixture(name="einstein_counts")
def _einstein_counts_fixture():
    """Fixture for the Einstein quote."""
    return Counter(
        {
            "insanity": 1,
            "is": 1,
            "doing": 1,
            "the": 1,
            "same": 1,
            "thing": 1,
            "over": 2,
            "and": 2,
            "expecting": 1,
            "different": 1,
            "results": 1,
        }
    )


def test_count_words(einstein_counts):
    """Test word counting from a file."""
    expected = einstein_counts
    actual = count_words("tests/einstein.txt")
    assert actual == expected, "Einstein quote counted incorrectly!"


def test_plot_words(einstein_counts):
    """Test plotting of word counts."""
    counts = einstein_counts
    fig = plot_words(counts)
    assert isinstance(fig, matplotlib.container.BarContainer), "Wrong plot type"
    assert len(fig.datavalues) == 10, "Incorrect number of bars plotted"


@pytest.mark.parametrize(
    "bad_input",
    [
        3.14,
        "test_string",
        "test_file.txt",
        ["test", "list", "of", "words"],
        {"test_key": "test_value"},
    ],
)
def test_plot_words_error(bad_input):
    """Check TypeError raised when Counter not used."""
    with pytest.raises(TypeError):
        plot_words(bad_input)


def test_integration():
    """Test count_words() and plot_words() workflow."""
    counts = count_words("tests/einstein.txt")
    fig = plot_words(counts)
    assert isinstance(fig, matplotlib.container.BarContainer), "Wrong plot type"
    assert len(fig.datavalues) == 10, "Incorrect number of bars plotted"
    assert max(fig.datavalues) == 2, "Highest word count should be 2"


def test_regression():
    """Regression test for The Great Gatsby dataset."""
    top_word = count_words(get_gatsby()).most_common(1)
    assert top_word[0][0] == "the", "Most common word should be 'the'"
    assert top_word[0][1] == 2545, """
    Most word count for 'the' should be 2545; the count has changed.
    """
