"""config.py

A Victoria plugin to interact with Azure DevOps PBIs.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import click

import yaml


@click.group()
@click.pass_obj
def pbi(cfg):
    """Interact with PBIs on Azure DevOps."""
    pass


@pbi.command()
@click.pass_obj
def ls(cfg):
    """List PBIs."""
    pass