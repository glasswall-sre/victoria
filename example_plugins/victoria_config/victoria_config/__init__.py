"""victoria_config

A Victoria plugin to print the currently loaded config.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import click
import yaml
from victoria.plugin import Plugin

# you need to use relative imports for your own modules/packages
from . import functionality
from . import schema

# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="config",
                cli=functionality.config,
                config_schema=schema.ConfigSchema())


@click.group()
@click.pass_obj
def config(cfg: schema.ConfigConfig):
    """Print the loaded config, and the path to the default config file."""
    pass