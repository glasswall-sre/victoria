"""plugin

Contains functions for loading Victoria plugins at runtime.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

import importlib
from os.path import basename, splitext

import click


def load(plugin_path: str) -> click.Command:
    """Load a plugin from a given path to a Python file. The plugin name will
    be the same as the subcommand name within Victoria. It returns the click
    Command loaded from the plugin file, or None if there was an error.

    The plugin should define a method with the same name as the python file,
    decorated with click.command() decorator.

    For example: a plugin called 'test.py' would define a function 'test()'
    within it, which would be called by Victoria when a user executes the
    command 'victoria test'.

    Args:
        plugin_path (str): The path to the plugin to load.

    Returns:
        click.Command: The loaded command, or None if there was an error.
    """
    try:
        plugin_name = splitext(basename(plugin_path))[0]
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cli_fn = getattr(module, plugin_name)
        if type(cli_fn) is not click.Command:
            # check that the command in the plugin was decorated as a click Command
            print(f"Error loading plugin '{plugin_path}': '{plugin_name}()'"
                  " did not have click.command decorator!")
            return None
        return cli_fn
    except AttributeError:
        # if the function didn't exist in the plugin file
        print(f"Error loading plugin '{plugin_path}': couldn't find function"
              f" '{plugin_name}()' in plugin file.")
        return None
    except OSError as err:
        # if the plugin file could not be found
        print(f"Error loading plugin '{plugin_path}': " + str(err))
        return None
