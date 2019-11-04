import builtins
from contextlib import nullcontext as does_not_raise
import io

import pytest

import victoria.config
import victoria.plugin

VALID_CONFIG = victoria.config.Config(
    {
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
    }, {'config': {
        'indent': 2
    }})


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
  config:
    indent: 2""", VALID_CONFIG), ("non-valid yaml: sadad:", None),
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
  config:
    indent: 2""", None)],
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
        "test", None, None), VALID_CONFIG, None, pytest.raises(ValueError))
],
                         ids=["NoConfig", "NoPluginConfig"])
def test_load_plugin_config(plugin, cfg, expected, raises):
    with raises:
        result = victoria.config.load_plugin_config(plugin, cfg)
        assert result == expected