from pathlib import Path
from typing import Union

# we use Union[str, Path] which means
# the function can accept either a string or Path object:


def get_file_content(file_path: Union[str, Path]) -> str:
    """Read and return the content of a file.
    and return the content as a string"""

    # here we use Path object to handle file paths
    # if user enters a string, we convert it to a Path object for easier handling
    path = Path(file_path) if isinstance(file_path, str) else file_path

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
