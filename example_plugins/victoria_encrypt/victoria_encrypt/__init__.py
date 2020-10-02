"""victoria_encrypt

A Victoria plugin to make envelope encryption easier.

Author:
    Sam Gibson 
"""
import logging

import click
import dpath.util
from marshmallow import ValidationError
import yaml

from victoria.config import Config
from victoria.plugin import Plugin
from victoria.encryption.schemas import EncryptionEnvelopeSchema, EncryptionEnvelope


@click.group()
@click.pass_obj
def encrypt(cfg: Config):
    """Envelope encrypt data easily."""
    pass


@encrypt.command()
@click.pass_obj
@click.argument("plaintext")
def data(cfg: Config, plaintext: str):
    """Envelope encrypt a piece of data."""
    # get the provider, and encrypt the data
    provider = cfg.get_encryption()
    envelope = provider.encrypt_str(plaintext)

    # print out the encrypted data in YAML format
    print(f"data: {envelope.data}")
    print(f"iv: {envelope.iv}")
    print(f"key: {envelope.key}")
    print(f"version: {envelope.version}")


@encrypt.command()
@click.pass_obj
@click.argument("file")
@click.argument("path")
def decrypt(cfg: Config, file: str, path: str):
    """Decrypt a piece of data."""
    # get the provider
    provider = cfg.get_encryption()
    envelope = None
    try:
        loaded_dict = None

        # load the YAML file
        with open(file, 'r') as file_handle:
            loaded_dict = yaml.safe_load(file_handle)

        # scope to the envelope directly with dpath
        raw_envelope = dpath.util.get(loaded_dict, path)

        # load it with the schema
        envelope = EncryptionEnvelopeSchema().load(raw_envelope)
    except (OSError, yaml.YAMLError, ValueError, KeyError,
            ValidationError) as err:
        logging.error(err)
        raise SystemExit(1)

    decrypted = provider.decrypt_str(envelope)
    if decrypted is None:
        raise SystemExit(1)

    print(decrypted)



@encrypt.command()
@click.pass_obj
@click.argument("file")
@click.argument("path")
def rotate(cfg: Config, file: str, path: str):
    """Rotate an encryption key."""
    # get the provider
    provider = cfg.get_encryption()

    envelope = None
    try:
        loaded_dict = None

        # load the YAML file
        with open(file, 'r') as file_handle:
            loaded_dict = yaml.safe_load(file_handle)

        # scope to the envelope directly with dpath
        raw_envelope = dpath.util.get(loaded_dict, path)

        # load it with the schema
        envelope = EncryptionEnvelopeSchema().load(raw_envelope)
    except (OSError, yaml.YAMLError, ValueError, KeyError,
            ValidationError) as err:
        logging.error(err)
        raise SystemExit(1)

    # now re-encrypt it with the new key
    rotated_envelope = provider.rotate_key(envelope)

    # and print it
    print(f"data: {rotated_envelope.data}")
    print(f"iv: {rotated_envelope.iv}")
    print(f"key: {rotated_envelope.key}")
    print(f"version: {rotated_envelope.version}")


# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="encrypt", cli=encrypt)
