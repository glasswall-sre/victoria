"""setup.py

Used for installing Victoria via pip.
"""

from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(
    dependency_links=[],
    install_requires=["click==7.0", "marshmallow==3.2.1", "pyyaml==5.1.2"],
    name="victoria",
    version="0.2.1",
    description="SRE automation toolbelt",
    long_description=repo_file_as_string("README.md"),
    long_description_content_type="text/markdown",
    author="Sam Gibson",
    author_email="sgibson@glasswallsolutions.com",
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        victoria=victoria.script.victoria:main
    """,
)
