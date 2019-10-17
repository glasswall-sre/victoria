"""setup.py

Used for installing Victoria via pip.
"""

from setuptools import setup, find_packages

setup(
    dependency_links=[],
    install_requires=["click==7.0", "marshmallow==3.2.1", "pyyaml==5.1.2"],
    name="victoria",
    version="0.1",
    description="SRE automation toolbelt",
    author="Sam Gibson",
    author_email="sgibson@glasswallsolutions.com",
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        victoria=victoria.script.victoria:main
    ''',
)
