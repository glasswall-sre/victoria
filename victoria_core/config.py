"""config

Contains various classes and methods for loading the config of Victoria.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import logging.config
from typing import List

from marshmallow import Schema, fields, post_load, ValidationError
import yaml


class ConfigSchema(Schema):
    """Marshmallow schema for the Config object."""
    plugins = fields.List(fields.Str)
    logging_config = fields.Dict()

    @post_load
    def make_config_obj(self, data, **kwargs):
        return Config(**data)


CONFIG_SCHEMA = ConfigSchema()
"""Instance of ConfigSchema used for validating loaded configs."""


class Config:
    """Config is used for storing deserialized values from Config files.

    Attributes:
        plugins (List[str]): The list of paths to plugin Python modules to load.
        logging_config (dict): The config to use for logging.
    """
    def __init__(self, plugins: List[str], logging_config: dict):
        self.plugins = plugins
        self.logging_config = logging_config
        logging.config.dictConfig(logging_config)


def _print_validation_err(err: ValidationError, name: str) -> None:
    """Internal function used for printing a validation error in the Schema.

    Args:
        err (ValidationError): The error to log.
        name (str): A human-readable identifier for the Schema data source. Like a filename.
    """
    # build up a string for each error
    log_str = []
    log_str.append(f"Error loading file '{name}':")
    for field_name, err_msgs in err.messages.items():
        log_str.append(f"{field_name}: {err_msgs}")

    # print the joined up string, and exit with an error
    print(" ".join(log_str))


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
