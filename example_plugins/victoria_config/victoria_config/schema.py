"""schema.py

This is used to store a schema for the plugin's config section.

Author:
    Sam Gibson 
"""

from marshmallow import Schema, fields, post_load, validate


class ConfigConfig:
    """ConfigConfig is the config for the config printing plugin.

    Attributes:
        indent (int): How much to indent the YAML by. Can be between 1 and 10.
    """
    def __init__(self, indent: int):
        self.indent = indent


class ConfigSchema(Schema):
    """Marshmallow schema for the config printing plugin's config section."""
    indent = fields.Int(validate=validate.Range(min=1, max=10))

    @post_load
    def make_config(self, data, **kwargs):
        return ConfigConfig(**data)