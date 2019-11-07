from click.testing import CliRunner
import pytest

from victoria.script.victoria import cli
import victoria.config

DEFAULT_CONFIG = """logging_config:
  formatters:
    default:
      format: '%(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      formatter: default
      level: DEBUG
      stream: ext://sys.stdout
  root:
    handlers:
    - console
    level: DEBUG
  version: 1
plugins_config:
  config:
    indent: 2

"""

DEFAULT_CONFIG_BAD_PLUGIN = """logging_config:
  formatters:
    default:
      format: '%(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      formatter: default
      level: DEBUG
      stream: ext://sys.stdout
  root:
    handlers:
    - console
    level: DEBUG
  version: 1
plugins_config:
  non_existent_plugin:
"""


def test_victoria_cli():
    """Test to see if the CLI runs fine with no args."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("victoria.yaml", "w") as config_file:
            config_file.write(DEFAULT_CONFIG)

        cfg = victoria.config.load("victoria.yaml")

        result = runner.invoke(cli, obj=cfg)
        assert result.exit_code == 0


def test_victoria_cli_bad_plugin_config():
    """Test to see if the CLI exits with 1 on loading a bad plugin config."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("victoria.yaml", "w") as config_file:
            config_file.write(DEFAULT_CONFIG_BAD_PLUGIN)

        cfg = victoria.config.load("victoria.yaml")

        result = runner.invoke(cli, ["config"], obj=cfg)
        assert result.exit_code == 1


def test_victoria_cli_bad_command():
    """Test to see if the CLI exits with 2 on specifying a nonexistent command."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("victoria.yaml", "w") as config_file:
            config_file.write(DEFAULT_CONFIG)

        cfg = victoria.config.load("victoria.yaml")

        result = runner.invoke(cli, ["bad_command"], obj=cfg)
        assert result.exit_code == 2


def test_victoria_cli_config():
    """Test to see if the example plugin works correctly."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("victoria.yaml", "w") as config_file:
            config_file.write(DEFAULT_CONFIG)

        cfg = victoria.config.load("victoria.yaml")

        result = runner.invoke(cli, ["config", "view"], obj=cfg)
        assert result.output == DEFAULT_CONFIG