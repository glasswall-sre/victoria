"""plugin

Contains functions for loading Victoria plugins at runtime.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import importlib
import logging
from os.path import basename, splitext
import pkgutil
from typing import List

import click
from marshmallow import Schema


class Plugin:
    """Plugin is the API for creating a Victoria plugin. It defines plugin name,
    CLI entry point, and optionally a schema for custom plugin config.

    Attributes:
        name (str): The name of the plugin. This will be the subcommand name.
        cli (click.Command): The click entrypoint of the plugin command.
        config_schema (marshmallow.Schema): The schema to use to validate config (OPTIONAL).
    """
    def __init__(self,
                 name: str,
                 cli: click.Command,
                 config_schema: Schema = None) -> None:
        self.name = name
        self.cli = cli
        self.config_schema = config_schema


def load(plugin_name: str) -> Plugin:
    """Load a plugin by name.

    Plugins are installed python modules with a name starting with 'victoria_'.
    For example: 'victoria_config'. Plugin packages should define a plugin
    object in their __init__.py and use it to wire up plugin functionality.

    A plugin can optionally define a marshmallow schema that can be used for
    validating its config. Plugin configs will be located in the
    'plugins_config' object of the Victoria config, under an object with the
    same name as the plugin.

    Args:
        plugin_name (str): The name of the plugin package to load. Plugin packages
            must be in the format "victoria_{plugin_name}".

    Returns:
        Plugin: the plugin object as loaded from the module, or None if there was
            some error whilst loading.
    """
    try:
        spec = importlib.util.find_spec(f"victoria_{plugin_name}")
        if spec is None:
            logging.error(
                f"Error loading plugin 'victoria_{plugin_name}': module spec not found"
            )
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        plugin_obj = getattr(module, "plugin")
        if type(plugin_obj) is not Plugin:
            # check that the plugin object is of the right type
            logging.error(
                f"Error loading plugin 'victoria_{plugin_name}': 'plugin' "
                "must be of type 'Plugin'")
            return None
    except (ValueError, ModuleNotFoundError, AttributeError) as err:
        # if there was some error finding the module spec or getting
        # the plugin object from the loaded module
        logging.error(f"Error loading plugin 'victoria_{plugin_name}': {err}")
        return None
    return plugin_obj


def load_all() -> List[Plugin]:
    """Load all plugins that can be found.

    Returns:
        List[Plugin]: The list of plugins successfully loaded.
    """
    plugins = []
    already_loaded_names = []
    for plgn in ls():
        loaded_plugin = load(plgn)

        if loaded_plugin.name in already_loaded_names:
            logging.error(
                f"Error loading plugin 'victoria_{loaded_plugin.name}"
                ": a plugin with the same name is already loaded")
            continue

        if loaded_plugin is not None:
            already_loaded_names.append(loaded_plugin.name)
            plugins.append(loaded_plugin)
    return plugins


def ls() -> List[str]:
    """Get a list of plugins installed on the system.

    Returns:
        List[str]: The list of plugin package names installed. Each plugin name
            will be in the list without the "victoria_" prefix.
    """
    return [
        name[len("victoria_"):] for _, name, _ in pkgutil.iter_modules()
        if name.startswith("victoria_")
    ]