"""empty doc"""

# datasets.py
from importlib import resources


def get_gatsby():
    """Get path to example "The Great Gatsby" [1]_ text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] F. Scott Fitzgerald "The Great Gatsby"
    """
    resource = resources.files("countpy.data") / "gatsby.txt"
    with resources.as_file(resource) as f:
        data_file_path = f
    # with resources.path("countpy.data", "gatsby.txt") as f:
    # data_file_path = f
    return data_file_path
