"""config

Contains various classes and methods for loading the config of Victoria.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import logging.config
from typing import List

import click
from marshmallow import Schema, fields, post_load, ValidationError
import yaml

from .plugin import Plugin


class ConfigSchema(Schema):
    """Marshmallow schema for the Config object."""
    logging_config = fields.Dict()
    plugins_config = fields.Dict(required=False)

    @post_load
    def make_config_obj(self, data, **kwargs):
        return Config(**data)


CONFIG_SCHEMA = ConfigSchema()
"""Instance of ConfigSchema used for validating loaded configs."""


class Config:
    """Config is used for storing deserialized values from Config files.

    Attributes:
        logging_config (dict): The config to use for logging.
        plugins_config (dict): The config to use for plugins.
    """
    def __init__(self, logging_config: dict, plugins_config: dict = None):
        self.logging_config = logging_config
        logging.config.dictConfig(logging_config)
        self.plugins_config = plugins_config


pass_config = click.make_pass_decorator(Config)
"""Decorator for passing the Victoria config to a command."""


def _print_validation_err(err: ValidationError,
                          name: str,
                          use_log: bool = True) -> None:
    """Internal function used for printing a validation error in the Schema.

    Args:
        err (ValidationError): The error to log.
        name (str): A human-readable identifier for the Schema data source. 
            Like a filename.
        use_log (bool): Whether to use the logging package to log the error.
            This is needed because sometimes a validation error might occur
            when loading the logging config, before it's configured.
    """
    # build up a string for each error
    log_str = []
    log_str.append(f"Error validating config '{name}':")
    for field_name, err_msgs in err.messages.items():
        log_str.append(f"{field_name}: {err_msgs}")

    # print the joined up string
    print(" ".join(log_str))


def load_plugin_config(plugin: Plugin, cfg: Config) -> object:
    """Load the config of a plugin from the main Victoria config.

    Args:
        plugin (Plugin): The plugin to load the config for.
        cfg (Config): The config file to load the config from.

    Returns:
        object: The loaded config object. It will be the same type as whatever
            the plugin's config marshmallow schema will marshal it to, or None
            if there was some error loading the plugin config.

    Raises:
        ValueError: if the plugin didn't have a config schema.
    """
    # we don't want to try to load a config from the config if it wasn't loaded
    if cfg is None:
        logging.warn(f"Can't load '{plugin.name}' config: victoria config "
                     "not loaded.")
        return None

    if plugin.config_schema is None:
        raise ValueError(f"Can't load plugin config: plugin '{plugin.name}' "
                         "did not have config schema")

    # check to see if we have the plugins_config section in the main config
    if not cfg.plugins_config:
        logging.error("Can't load plugin config: config did not "
                      "have 'plugins_config' section")
        return None

    # check to see if that section has a section for the plugin
    if not cfg.plugins_config.get(plugin.name):
        logging.error(
            "Can't load plugin config: "
            f"config did not have section for plugin '{plugin.name}'")
        return None

    # try validating the contents of the plugin section with the schema
    try:
        loaded_config = plugin.config_schema.load(
            cfg.plugins_config[plugin.name])
        return loaded_config
    except ValidationError as err:
        # if the loaded YAML wasn't a valid config
        _print_validation_err(err, f"plugins_config.{plugin.name}")
        return None


def load(config_path: str) -> Config:
    """Load a config file from a given path and make sure it's valid.

    If an error occurred, it will print it and return None.

    Args:
        config_path (str): The path to the YAML config file.

    Returns:
        Config: The loaded config file, or None if an error occurred.
    """
    try:
        with open(config_path, "r") as config_file:
            raw_config = yaml.safe_load(config_file)
            loaded_config = CONFIG_SCHEMA.load(raw_config)
            return loaded_config
    except OSError as err:
        # if there was an error opening the file
        print("Error opening config file: " + str(err))
        return None
    except yaml.YAMLError as err:
        # if the loaded YAML was invalid YAML
        print("Error in config file: " + str(err))
        return None
    except ValidationError as err:
        # if the loaded YAML wasn't a valid config
        _print_validation_err(err, config_path)
        return None
    except (ValueError, TypeError, AttributeError, ImportError) as err:
        # if the logging config was invalid
        print("Unable to load logging config: " + str(err))
        return None
