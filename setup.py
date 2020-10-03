"""setup.py

Used for installing Victoria via pip.
"""

from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(
    dependency_links=[],
    install_requires=[
        "appdirs>=1.4.3", "click>=7.0", "marshmallow>=3.2.1", "pyyaml>=5.1.2",
        "azure-storage-blob>=12.3.0", "cryptography>=2.8",
        "azure-keyvault>=4.0.0", "azure-identity>=1.3.0", "dpath>=2.0.1",
        "azure-cli-core>=2.7.0"
    ],
    name="victoria",
    version="0.7.7",
    description=
    "Automation toolbelt -- a single command with multiple pluggable subcommands for automating any number of 'toil' tasks that inhibit productivity.",
    long_description=repo_file_as_string("README.md"),
    long_description_content_type="text/markdown",
    author="Glasswall SRE",
    author_email="sre@glasswallsolutions.com",
    url="https://github.com/glasswall-sre/victoria",
    classifiers=[
        "Development Status :: 4 - Beta", "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", "Topic :: Terminals",
        "Topic :: Utilities"
    ],
    keywords="cli automation sre plugin",
    packages=find_packages(".") +
    find_packages("example_plugins/victoria_config") +
    find_packages("example_plugins/victoria_store") +
    find_packages("example_plugins/victoria_encrypt"),
    package_dir={
        "victoria_config": "example_plugins/victoria_config/victoria_config",
        "victoria_store": "example_plugins/victoria_store/victoria_store",
        "victoria_encrypt": "example_plugins/victoria_encrypt/victoria_encrypt"
    },
    entry_points="""
        [console_scripts]
        victoria=victoria.script.victoria:main
    """,
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"victoria": ["victoria_example.yaml"]})
