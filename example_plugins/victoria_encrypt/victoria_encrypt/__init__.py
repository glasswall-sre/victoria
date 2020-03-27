"""victoria_encrypt

A Victoria plugin to make envelope encryption easier.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import logging

import click

from victoria.config import Config
from victoria.plugin import Plugin


@click.command()
@click.pass_obj
@click.argument("plaintext")
def encrypt(cfg: Config, plaintext: str):
    """Envelope encrypt data easily."""
    provider = cfg.get_encryption()
    envelope = provider.encrypt(plaintext.encode("utf-8"))
    print(f"data: {envelope.data}")
    print(f"iv: {envelope.iv}")
    print(f"key: {envelope.key}")


# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="encrypt", cli=encrypt)
