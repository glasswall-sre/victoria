import builtins
from contextlib import nullcontext as does_not_raise
import io
from os import path
import pkg_resources

from marshmallow import Schema, fields
from pyfakefs.pytest_plugin import fs
import pytest

import victoria.config
import victoria.plugin

from test_storage_azure import mock_azure_classes as mock_storage
from test_encryption_azure import mock_azure_classes as mock_encryption

VALID_LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}

VALID_CONFIG = victoria.config.Config(VALID_LOGGING_CONFIG,
                                      {'test': {
                                          'test_field': 2
                                      }})


class PluginSchema(Schema):
    test_field = fields.Int()

@pytest.fixture
def config_fixture(mock_storage, mock_encryption, fs):
    config_yml = """logging_config:
  version: 1
  disable_existing_loggers: True
  formatters:
    default:
      format: "%(message)s"
  handlers:
    console:
      class: logging.StreamHandler
      level: INFO
      formatter: default
      stream: ext://sys.stdout
  root:
    level: INFO
    handlers: [console]
  loggers:
    azure.core.pipeline.policies.http_logging_policy:
      level: CRITICAL
encryption_provider:
  provider: azure
  config:
    vault_url: "https://your-vault.vault.azure.net/"
    key: keyencryptionkey
    tenant_id: tenant-id-here
    client_id: sp-client-id-here
    client_secret: sp-client-secret-here
storage_providers:
  azure:
    account: storageaccountname
    credential: your-access-key-here
    container: victoria
plugins_config:
  config:
    indent: 2
plugins_config_location: {}"""
    fs.create_file("victoria.yaml", contents=config_yml)
    return victoria.config.load("victoria.yaml")


@pytest.mark.parametrize(
    "config_file,expected", [("""logging_config:
  version: 1
  formatters:
    default:
      format: "%(message)s"
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: default
      stream: ext://sys.stdout
  root:
    level: DEBUG
    handlers: [console]
plugins_config:
  test:
    test_field: 2""", VALID_CONFIG), ("non-valid yaml: sadad:", None),
                             ("""logging_config:
  version: 1
  formatters:
    default:
      format: "%(message)s"
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: default
      stream: ext://sys.stdout
  root:
    level: DEBUG
    handlers: [console]
plugins_config: invalid!""", None),
                             ("""logging_config:
  formatters:
    default:
      format: "%(message)s"
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: default
      stream: ext://sys.stdout
  root:
    level: DEBUG
    handlers: [console]
plugins_config:
  test:
    test_field: 2""", None)],
    ids=["success", "YAMLError", "ValidationError", "InvalidLoggingConfig"])
def test_load(monkeypatch, config_file, expected):
    def mock_open(*args, **kwargs):
        return io.StringIO(config_file)

    with monkeypatch.context() as m:
        m.setattr(builtins, "open", mock_open)

        result = victoria.config.load("")
        assert result == expected


@pytest.mark.parametrize("a,b,expected",
                         [(VALID_CONFIG, VALID_CONFIG, True),
                          (VALID_CONFIG, "not a config", False)])
def test_config_eq(a, b, expected):
    result = a == b
    assert result == expected


@pytest.mark.parametrize("plugin,cfg,expected,raises", [
    (victoria.plugin.Plugin("test", None, None), None, None, does_not_raise()),
    (victoria.plugin.Plugin(
        "test", None, None), VALID_CONFIG, None, pytest.raises(ValueError)),
    (victoria.plugin.Plugin("test", None, Schema()),
     victoria.config.Config(VALID_LOGGING_CONFIG,
                            None), None, does_not_raise()),
    (victoria.plugin.Plugin("test", None, Schema()),
     victoria.config.Config(VALID_LOGGING_CONFIG,
                            {"not_here": {}}), None, does_not_raise()),
    (victoria.plugin.Plugin("test", None, PluginSchema()),
     victoria.config.Config(VALID_LOGGING_CONFIG,
                            {"test": {
                                "test_field": "not an int"
                            }}), None, does_not_raise()),
    (victoria.plugin.Plugin("test", None, PluginSchema()), VALID_CONFIG, {
        "test_field": 2,
        "victoria_config": VALID_CONFIG
    }, does_not_raise())
],
                         ids=[
                             "NoConfig", "NoPluginConfig", "NoConfigPlugins",
                             "NoConfigPluginsSection", "BadPluginConfig",
                             "Success"
                         ])
def test_load_plugin_config(plugin, cfg, expected, raises):
    with raises:
        result = victoria.config.load_plugin_config(plugin, cfg)
        assert result == expected

def test_get_storage(config_fixture):
    storage = config_fixture.get_storage("azure")
    assert storage.container == "victoria"

def test_get_storage_error(config_fixture):
    with pytest.raises(ValueError):
        config_fixture.get_storage("bad type")

def test_get_storage_invalid_config(mock_storage, fs):
    config_yml = """storage_providers:
  azure:
    wrong: values
logging_config:
  version: 1
encryption_provider: null
plugins_config: {}
plugins_config_location: {}"""
    fs.create_file("victoria.yaml", contents=config_yml)
    config = victoria.config.load("victoria.yaml")
    with pytest.raises(TypeError):
        config.get_storage("azure")

def test_get_encryption(config_fixture):
    encryption = config_fixture.get_encryption()
    assert encryption.key_client.vault_url == "https://your-vault.vault.azure.net/"

def test_get_encryption_error(mock_encryption, fs):
    config_yml = """storage_providers: {}
logging_config:
  version: 1
encryption_provider:
  provider: non exist
  config: {}
plugins_config: {}
plugins_config_location: {}"""
    fs.create_file("victoria.yaml", contents=config_yml)
    config = victoria.config.load("victoria.yaml")
    with pytest.raises(ValueError):
        config.get_encryption()

def test_get_encryption_invalid_config(mock_encryption, fs):
    config_yml = """storage_providers: {}
logging_config:
  version: 1
encryption_provider:
  provider: azure
  config:
    bad: config
plugins_config: {}
plugins_config_location: {}"""
    fs.create_file("victoria.yaml", contents=config_yml)
    config = victoria.config.load("victoria.yaml")
    with pytest.raises(TypeError):
        config.get_encryption()

def test_load_plugin_config_storage_provider(fs):
    config_yml = """storage_providers:
  local:
    container: container
logging_config:
  version: 1
encryption_provider: null
plugins_config: {}
plugins_config_location:
  config: local://config.yaml"""
    fs.create_file("victoria.yaml", contents=config_yml)
    fs.create_file("container/config.yaml", contents="test_field: 2")
    config = victoria.config.load("victoria.yaml")
    plugin_def = victoria.plugin.Plugin("config", None, PluginSchema())
    plugin_config = victoria.config.load_plugin_config(plugin_def, config)
    assert plugin_config["test_field"] == 2

def test_load_plugin_config_from_both(fs):
    config_yml = """storage_providers:
  local:
    container: container
logging_config:
  version: 1
encryption_provider: null
plugins_config:
  config:
    test_field: 4
plugins_config_location:
  config: local://config.yaml
"""
    fs.create_file("victoria.yaml", contents=config_yml)
    fs.create_file("container/config.yaml", contents="test_field: 2")
    config = victoria.config.load("victoria.yaml")
    plugin_def = victoria.plugin.Plugin("config", None, PluginSchema())
    plugin_config = victoria.config.load_plugin_config(plugin_def, config)

    # plugins_config_location should take precedence over plugins_config
    assert plugin_config["test_field"] == 2