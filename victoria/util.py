"""util

Contains various utility functions and classes used in Victoria.

Author:
    Sam Gibson 
"""

from os.path import splitext, basename


def basenamenoext(path: str) -> str:
    """Get the basename of a filepath without a file extension."""
    return splitext(basename(path))[0]