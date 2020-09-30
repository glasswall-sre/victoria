"""setup.py

Used for installing victoria_encrypt via pip.

Author:
    Ash Powell <apowell@glasswallsolutions.com>
"""

from setuptools import setup, find_packages

setup(
    dependency_links=[],
    install_requires=["victoria"],
    name="victoria_encrypt",
    version="0.1",
    description="Victoria plugin to make envelope encryption easier",
    author="Ash Powell",
    author_email="apowell@glasswallsolutions.com",
    packages=find_packages(),
)
