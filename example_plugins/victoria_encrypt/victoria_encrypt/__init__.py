"""victoria_encrypt

A Victoria plugin to make envelope encryption easier.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import logging

import click
import yaml

from victoria.config import Config
from victoria.plugin import Plugin
from victoria.encryption import azure_provider


@click.command()
@click.pass_obj
@click.argument("plaintext")
def encrypt(cfg: Config, plaintext: str):
    """Envelope encrypt data easily."""
    provider = cfg.get_encryption()
    print("--> Encrypting data...")
    envelope = provider.encrypt(plaintext.encode("utf-8"))
    print(f"--> Ciphertext: {envelope.data}")
    print(f"--> Decrypting data...")
    plaintext = provider.decrypt(envelope)
    print(f"--> Plaintext: {plaintext}")


# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="encrypt", cli=encrypt)
