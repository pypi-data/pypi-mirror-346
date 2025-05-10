# read version from installed package
from importlib.metadata import version

__version__ = version("countpy")

# populate package namespace
from countpy.countpy import count_words
from countpy.plotting import plot_words
from countpy.datasets import get_gatsby
