"""setup.py

Used for installing victoria_store via pip.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

from setuptools import setup, find_packages

setup(
    dependency_links=[],
    install_requires=["victoria"],
    name="victoria_store",
    version="0.1",
    description="Victoria plugin to store things in cloud storage",
    author="Sam Gibson",
    author_email="sgibson@glasswallsolutions.com",
    packages=find_packages(),
)
