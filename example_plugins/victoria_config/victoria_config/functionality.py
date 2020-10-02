"""functionality.py

This is where the main functionality of the config plugin is implemented.

Author:
    Sam Gibson 
"""

import click
import yaml
import victoria.config
from victoria.config import Config

from . import schema


@click.group()
@click.pass_obj
def config(cfg: schema.ConfigConfig):
    """Print the loaded config, and the path to the default config file."""
    pass


@config.command()
@click.pass_obj
def path(cfg: schema.ConfigConfig):
    """Print the path to the config file Victoria uses."""
    print(victoria.config.get_config_loc())


@config.command()
@click.pass_obj
def view(cfg: schema.ConfigConfig):
    """Print the current loaded config and exit."""
    core_config = cfg.victoria_config
    print(yaml.safe_dump(core_config.as_dict(), indent=cfg.indent))