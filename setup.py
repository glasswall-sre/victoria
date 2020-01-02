"""setup.py

Used for installing Victoria via pip.
"""

from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(dependency_links=[],
      install_requires=[
          "appdirs==1.4.3",
          "click==7.0",
          "marshmallow==3.2.1",
          "pyyaml==5.1.2",
      ],
      name="victoria",
      version="#{TAG_NAME}#",
      description="SRE automation toolbelt",
      long_description=repo_file_as_string("README.md"),
      long_description_content_type="text/markdown",
      author="Sam Gibson",
      author_email="sgibson@glasswallsolutions.com",
      packages=find_packages(".") +
      find_packages("example_plugins/victoria_config"),
      package_dir={
          "victoria_config": "example_plugins/victoria_config/victoria_config"
      },
      entry_points="""
        [console_scripts]
        victoria=victoria.script.victoria:main
    """,
      python_requires=">=3.7",
      include_package_data=True,
      package_data={"victoria": ["victoria_example.yaml"]})
