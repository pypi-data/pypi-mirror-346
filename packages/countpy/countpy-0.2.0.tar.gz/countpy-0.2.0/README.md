# countpy

A python package to help you count words in a text file

## Installation

```bash
$ pip install countpy
```

## Usage

`countpy` can be used to count words in a text file and plot results
as follows:

```python
from countpy.countpy import count_words
from countpy.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`countpy` was created by Dalia Tavizon-Dykstra. It is licensed under the terms of the MIT license.

## Credits

`countpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
