"""setup.py

Used for installing victoria_config via pip.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

from setuptools import setup, find_packages

setup(
    dependency_links=[],
    install_requires=[
        "click==7.0", "pyyaml==5.1.2", "marshmallow==3.2.1", "victoria"
    ],
    name="victoria_config",
    version="0.1",
    description="Victoria plugin to print config",
    author="Sam Gibson",
    author_email="sgibson@glasswallsolutions.com",
    packages=find_packages(),
)
