"""functionality.py

This is where the main functionality of the config plugin is implemented.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import click
import yaml
import victoria.config
from victoria.config import Config

from . import schema


@click.group()
@click.pass_obj
def config(cfg: schema.ConfigConfig):
    pass


@config.command()
@click.pass_obj
def path(cfg: schema.ConfigConfig):
    """Print the path to the config file Victoria uses."""
    print(victoria.config.get_config_loc())


@click.command()
@click.pass_obj
def view(cfg: schema.ConfigConfig):
    """Print the current loaded config and exit."""
    # as the plugin config is the current context, the app config will be in
    # the parent context
    main_config = click.get_current_context().parent.obj
    print(yaml.safe_dump(main_config.__dict__, indent=cfg.indent))