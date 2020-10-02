"""victoria_store

A Victoria plugin to store things in cloud storage.

Author:
    Sam Gibson 
"""
import io
import logging
import os
import sys
from os import path

import click
import yaml

from victoria import storage
from victoria.plugin import Plugin


@click.group()
@click.pass_context
@click.argument("backend")
def store(ctx, backend: str):
    """Store files/data in cloud storage."""
    # get the victoria config, so we can get cloud storage details from it
    v_cfg = ctx.obj
    ctx.obj = v_cfg.get_storage(backend)


@store.command()
@click.argument("filename", type=click.File('rb'))
@click.argument("key", type=str, required=False)
@click.pass_obj
def put(provider: storage.StorageProvider, filename, key):
    """Put a file at FILENAME into cloud storage, under an optional KEY."""
    key_name = key if key else path.basename(filename.name)
    logging.info(f"Uploading '{filename.name}' to object '{key_name}'")
    provider.store(filename, key_name)


@store.command()
@click.argument("key", type=str, required=False)
@click.pass_obj
def get(provider: storage.StorageProvider, key):
    """Get a file from KEY in cloud storage and print it to stdout."""
    stream = io.BytesIO()
    provider.retrieve(key, stream)
    print(stream.getvalue().decode("utf-8"))


@store.command()
@click.pass_obj
def ls(provider: storage.StorageProvider):
    """List files from cloud storage."""
    for blob in provider.ls():
        print(blob)


# this object is loaded by Victoria and used as the plugin entry point
plugin = Plugin(name="store", cli=store)
