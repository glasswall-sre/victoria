"""config.py

A Victoria plugin to print the currently loaded config.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import click

import yaml


@click.command()
@click.pass_obj
def config(cfg):
    """Print the current loaded config and exit."""
    print(yaml.safe_dump(cfg.__dict__, indent=2))