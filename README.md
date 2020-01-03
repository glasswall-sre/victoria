# V.I.C.T.O.R.I.A.
Very Important Commands for Toil Optimization: Reducing Inessential Activities.

Victoria is the SRE toolbelt -- a single command with multiple pluggable
subcommands for automating any number of 'toil' tasks that inhibit SRE
productivity.

## User guide

### Prerequisites
- Python
- Pip
- You've set up the [SRE package feed](https://dev.azure.com/glasswall/Glasswall%20Cloud/_wiki/wikis/Service%20Reliability%20Engineering%20Wiki/393/Using-SRE-Python-Packages)

### Installation
```terminal
pip install victoria --extra-index-url $SRE_PACKAGE_FEED
```

### Configuration
```yaml
# the python logging config, you generally don't want to change this - but you can!
logging_config:
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

# config for any plugins loaded, objects should have the same name as
# the plugin module, i.e. 'pbi.py' would have a 'pbi' object here
plugins_config:
  config:
    indent: 2
```

## Development guide

### Prerequisites
- Python
- Pipenv

### Quick start
1. Clone the repo.
2. Run `pipenv install`.
3. You're good to go.

## Making a plugin
A Victoria plugin is just a Python package with some certain requirements/properties.

### General
Your package name must start with `victoria_` in order for Victoria to use it.

For example: `victoria_pbi`.

### `setup.py`
In your `setup()` function you need to have `"victoria"` in your `install_requires`.

For example:
```python
from setuptools import setup, find_packages

setup(
    install_requires=[
        "victoria"
    ],
    name="victoria_pbi",
    version="#{TAG_NAME}#",
    description="Victoria plugin to manipulate Azure DevOps PBIs",
    author="Sam Gibson",
    author_email="sgibson@glasswallsolutions.com",
    packages=find_packages(),
)
```

### Package structure
Your repo should have the following structure as a python package:
- `victoria_{plugin_name}/`
    - `__init__.py`
    - `some_other_module.py`
- `setup.py`

### `__init__.py`
In your package's `__init__.py` you need to declare a `Plugin` object called `plugin` for
Victoria to know how to execute your plugin.

A Plugin object has three elements:
- `name`: The name of the subcommand.
- `cli`: The 'entry point' function to execute for the subcommand. Should be a [Click](https://click.palletsprojects.com/en/7.x/) command or group.
- `config_schema`: If your plugin requires config, this is an instance of a [Marshmallow schema](https://marshmallow.readthedocs.io/en/stable/) for your config. Otherwise, if you don't specify it your plugin won't use config, as it defaults to `None`.

Here is a minimal example of a plugin defined in `__init__.py`:
```python
from victoria.plugin import Plugin

@click.command()
@click.argument('name', nargs=1, type=str, required=True)
def hello(name: str):
    print(f"Hello, {name}!")

plugin = Plugin(name="hello", cli=hello)
```

When this package is installed, a `hello` subcommand will be available to Victoria.

You will be able to run it like so:
```bash
$ victoria hello "world"
Hello, world!
```

Obviously, you could specify your CLI entry point function in a separate Python module,
import that function in `__init__.py`, and specify `cli` as that function. This is
generally the best practice.

### Specifying plugin config
You can specify plugin config by setting `config_schema` of your `Plugin` object 
to be an instance of a [Marshmallow schema](https://marshmallow.readthedocs.io/en/stable/).

Config is in a section of the Victoria YAML config called `plugins_config`. 
```yaml
plugins_config:
  some_plugin:
    some_value: 123
```

Sub-objects of `plugins_config` have keys of the same name as the `name` parameter
in your `Plugin` object in `__init__.py`. So this `Plugin(name="some_plugin", ...)`
would be in key `some_plugin` under `plugins_config`.

Going by the example of a `hello` plugin in the previous section, let's customise
the greeting by allowing a user to specify a custom one in the Victoria config:
```yaml
plugins_config:
  hello:
    greeting: "Bonjour,"
```

We need to create a Marshmallow schema for the config, put this in `__init__.py`:
```python
from marshmallow import Schema, fields, post_load

class HelloConfigSchema(Schema):
    greeting = fields.Str(required=True)

    @post_load
    def create_hello_config(self, data, **kwargs):
        return HelloConfig(**data)

class HelloConfig:
    def __init__(self, greeting: str) -> None:
        self.greeting = greeting
```

And now modify the definition of your `Plugin` object to include the schema:
```python
plugin = Plugin(name="hello", cli=hello, config_schema=HelloConfigSchema())
```

Now we need to pass the config object to the CLI entry point function, we can do this
using Click by adding the `pass_obj` decorator and an argument to the function:
```python
@click.command()
@click.argument('name', nargs=1, type=str, required=True)
@click.pass_obj
def hello(cfg: HelloConfig, name: str):
    print(f"{cfg.greeting} {name}!")
```

As you can see, we're using our config's `greeting` field in the function now.

When you run the plugin, it should now greet the user with the value from the config:
```bash
$ victoria hello "le monde"
Bonjour, le monde!
```

This will also work with Click groups, like so:
```python
@click.group()
@click.pass_obj
def grouped(cfg: HelloConfig):
    pass

@grouped.command()
@click.pass_obj
def subcommand(cfg: HelloConfig):
    pass
```