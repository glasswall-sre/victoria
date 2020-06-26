#!/usr/bin/env python3
"""victoria

Victoria is the SRE toolbelt -- a single command with multiple pluggable
subcommands for automating any number of 'toil' tasks that inhibit SRE
productivity.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import argparse

import click

from .. import config
from .. import plugin

# used for making it so we can use both -h and --help for help text.
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

HELP_TEXT = """
V.I.C.T.O.R.I.A.

\b
Very
Important
Commands for
Toil
Optimization:
Reducing
Inessential
Activities

Victoria is the SRE toolbelt -- a single command with multiple pluggable
subcommands for automating any number of 'toil' tasks that inhibit SRE
productivity.
"""

VERSION_NUMBER = "#{TAG_NAME}#"
"""The version number of the application, to print when calling with --version."""


class VictoriaCLI(click.MultiCommand):
    """VictoriaCLI overrides click.MultiCommand to support loading click
    commands from python files. This is the bread and butter of the plugin
    system."""
    def __init__(self, name=None, **attrs):
        click.MultiCommand.__init__(self, name, **attrs)
        self.plugins = plugin.load_all()

    def list_commands(self, ctx):
        """List the available subcommands."""
        return [plgn.name for plgn in self.plugins]

    def get_command(self, ctx, cmd_name):
        """Get a subcommand from the list of installed plugins."""
        for plgn in self.plugins:
            # if the command name matches a loaded plugin name
            if plgn.name == cmd_name:
                # if the plugin has a config schema, load its config
                if plgn.config_schema and ctx.obj:
                    cfg = config.load_plugin_config(plgn, ctx.obj)
                    if not cfg:
                        # if there was an error loading the config, exit
                        raise SystemExit(1)
                    # HACK: patch the CLI context with the plugin config object
                    # this is a bit hacky, but it works
                    plgn.cli.context_settings = {"obj": cfg}
                return plgn.cli
        return None


@click.command(cls=VictoriaCLI,
               context_settings=CONTEXT_SETTINGS,
               help=HELP_TEXT)
@click.option("-c",
              "--config-file",
              default=config.get_config_loc(),
              metavar="FILE",
              help="The config file to load.")
@click.version_option(version=VERSION_NUMBER)
@click.pass_context
def cli(ctx, config_file):
    """This is the main CLI of the application. It uses VictoriaCLI to call
    loaded plugins based on subcommand name."""
    #pylint: disable=unused-argument
    if config_file is None:
        raise SystemExit(1)


def main():
    # HACK: use argparse to get the config-file argument, as we need it in
    # VictoriaCLI methods before it would be parsed in the click cli() command...
    # this is utter filth, but I couldn't think of a better way to do it,
    # and it works transparent to the user
    parser = argparse.ArgumentParser(description="", add_help=False)
    parser.add_argument("-c", "--config-file", default=config.get_config_loc())
    parsed_args, _ = parser.parse_known_args()

    # make sure a config already exists if a custom one was not specified
    if parsed_args.config_file == config.get_config_loc():
        config.ensure()

    # load the config
    cfg = config.load(parsed_args.config_file)

    # execute the main CLI, passing the config in through the context
    cli.main(obj=cfg)


if __name__ == "__main__":
    main()