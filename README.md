<div align="center" style="text-align:center">

# V.I.C.T.O.R.I.A.

![Victoria demo](https://raw.githubusercontent.com/glasswall-sre/victoria/master/img/victoria.gif)

**V**ery **I**mportant **C**ommands for **T**oil **O**ptimization: **R**educing **I**nessential **A**ctivities.

Victoria is the SRE toolbelt—a single command with multiple pluggable
subcommands for automating any number of 'toil' tasks that inhibit SRE
productivity.

<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=alert_status">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=sqale_rating">
<img align="center" src="https://sonarcloud.io/api/project_badges/measure?project=victoria&metric=reliability_rating">
<img align="center" src="https://codecov.io/gh/glasswall-sre/victoria/branch/master/graph/badge.svg">
<img align="center" src="https://img.shields.io/github/license/glasswall-sre/victoria">
<img align="center" src="https://img.shields.io/github/workflow/status/glasswall-sre/victoria/CD">
<img align="center" src="https://img.shields.io/pypi/pyversions/victoria">
<img align="center" src="https://img.shields.io/pypi/v/victoria">
</div>

## Table of Contents
- [V.I.C.T.O.R.I.A.](#victoria)
  - [Table of Contents](#table-of-contents)
  - [User guide](#user-guide)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Stock plugins](#stock-plugins)
    - [Configuration](#configuration)
      - [Plugin configuration](#plugin-configuration)
      - [Example](#example)
    - [Cloud storage](#cloud-storage)
    - [Cloud encryption](#cloud-encryption)
      - [KEK rotation](#kek-rotation)
    - [Cloud backends](#cloud-backends)
      - [Azure](#azure)
        - [Storage](#storage)
        - [Encryption](#encryption)
  - [Development guide](#development-guide)
    - [Prerequisites](#prerequisites-1)
    - [Quick start](#quick-start)
  - [Making a plugin](#making-a-plugin)
    - [General](#general)
    - [`setup.py`](#setuppy)
    - [Package structure](#package-structure)
    - [`__init__.py`](#initpy)
    - [Specifying plugin config](#specifying-plugin-config)
      - [Accessing core Victoria config from a plugin's config](#accessing-core-victoria-config-from-a-plugins-config)
    - [Storing secrets in config files](#storing-secrets-in-config-files)

## User guide

### Prerequisites
- Python 3.6+
- Pip

### Installation
```terminal
pip install -U victoria
```

### Stock plugins
Victoria comes with 3 plugins preinstalled:

- `config`
  - can be used to print the current config, and get the path to it
- `store`
  - can be used to interact with cloud storage backends
- `encrypt`
  - can be used to encrypt data for Victoria to load in config files

### Configuration
Victoria has a YAML config file that it uses to control the main CLI, which can
specify other YAML files (both local and remote) to use to configure plugins.

You can get the path to the config file by running `victoria config path`.

A quick way to edit your config if you have VSCode installed is by running
`code $(victoria config path)`.

Please note that the config file is not isolated. All installations of Victoria
on the same machine will use the same core config file.

#### Plugin configuration
Config is in a section of the Victoria YAML config called `plugins_config`. 
```yaml
plugins_config:
  some_plugin:
    some_value: 123
```

Sub-objects of `plugins_config` have keys of the same name as the plugins. So
a plugin called `verb` would have a key in `plugins_config` also called `verb`.

Additionally, you can specify separate config files for plugins with the
`plugins_config_location` section of the YAML config, instead of
keeping your config all in the core Victoria config file. You can even use
config files stored in the cloud! To do this, you need to have configured a 
storage provider in your core config. A simple one to use is the `local`
provider, which just uses a directory on your machine to store config files:

```yaml
storage_providers:
  local:
    container: C:/victoria_storage
```

Put that in your core config (you can change the directory to be wherever you
want), and you can now configure a separate config location for `some_plugin`
in your `plugins_config_location`:

```yaml
plugins_config_location:
  some_plugin: local://path/to/the_config_for_some_plugin.yaml
```

As with `plugins_config`, the keys are plugin names. The values are of the
format `{storage-provider-name}://{path-to-config-file}`, where
`{storage-provider-name}` is a key in the `storage_providers` section of your
core config. The `{storage-provider-name}` can be called anything if you'd like
it to be.

Victoria will grab it and load it as if it were in `plugins_config`. 

Please see the 'Cloud storage' and 'Cloud backends' sections of the README for 
setting up a cloud storage provider.

#### Example
```yaml
# the python logging config
logging_config:
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

# any storage provider config goes here - currently only Azure and local 
# storage is supported
storage_providers:
  azure:
    connection_string: your-connection-string
    container: victoriacontainer
  local:
    container: C:/victoria_storage

# your encryption provider config goes here - again only Azure is supported
encryption_provider:
  provider: azure
  config:
    vault_url: "https://your-vault.vault.azure.net/"
    key: keyencryptionkey
    tenant_id: tenant-id-here
    client_id: sp-client-id-here
    client_secret: sp-client-secret-here

# inline config for any plugins loaded, objects should have the same name as
# the plugin module, i.e. 'pbi.py' would have a 'pbi' object here
# note: if you don't want to put this inline, use 'plugins_config_location'
# as below, you don't have to specify it all here
# note: plugins_config_location takes precedence over this
plugins_config:
  config:
    indent: 2

# here you can specify separate file locations for plugin config files
# these use the storage_providers defined above. Like plugins_config, the
# keys of this object need to have the same name as the plugin.
# note: this takes precedence over plugins_config
plugins_config_location:
  a_plugin: "local://a_subdir/config_for_a_plugin.yaml"
  another_plugin: "azure://another_subdir/further/config_file.yaml"
```

### Cloud storage
Victoria can interact with cloud storage backends to get config for plugins!

Say you had a plugin used by a team that had a complex config, and you wanted
to share it so everyone could use the same config. You could store the YAML
config in a cloud storage container, and have everyone point their Victoria
config files at the container for that plugin.

Victoria even comes with a stock plugin called `store` that makes it easy to 
store and list files in your cloud storage backends!

Let's go through an example in more detail.

You've made a plugin called `helpful` which your team finds useful, but has
quite a complex config file that changes a lot and needs to be shared around.
You've previously had issues with it getting out of date and people having
wrong versions, so you decide to put it in cloud storage instead.

You've already set up an Azure storage backend in your Victoria config.

You make a YAML file containing the config for the plugin (`helpful-config.yaml`),
and you put it in cloud storage by running `victoria store azure put helpful-config.yaml`.

You then ask your team to configure the same Azure storage backend in their
Victoria config files, and point at the shared config file by putting this
section in their config:

```yaml
plugins_config_location:
  helpful: "azure://helpful-config.yaml"
```

They can remove their old config from `plugins_config`, and now when they run
`helpful` it will use the config from cloud storage! Easy.

Please note that `plugins_config_location` takes precedence over `plugins_config`,
so if you have a config specified for the same plugin in both, then only the one
in `plugins_config_location` will be loaded.


### Cloud encryption
Victoria can use [envelope encryption](https://cloud.google.com/kms/docs/envelope-encryption)
via a cloud key management solution to encrypt data that would normally have to 
be stored in config files in plaintext. This can help when storing config files
with secrets in cloud storage, as it will ensure any sensitive data is securely
encrypted at rest.

Envelope encryption uses a cloud encryption key (the key encryption key, or KEK)
in combination with a locally generated key (the data encryption key, or DEK) to
keep your data secure.

Please see the 'Cloud backends' section for configuring different encryption
providers.

You can envelope encrypt data by using the `encrypt` stock plugin provided with
Victoria. Give it a piece of text to encrypt, and it will output the encrypted
data in YAML format suitable for putting in a config file.

```bash
$ victoria encrypt data "your-top-secret-access-key"
data: <encrypted data>
key: <encrypted data key>
iv: <the nonce used with the key>
version: <the key version>
```

You can then paste this directly into a plugin config that needs a secret value,
like this:
```yaml
plugins_config:
  some_plugin:
    super_secret_access_key:
      data: <encrypted data>
      key: <encrypted data key>
      iv: <the nonce used with the key>
      version: <the key version>
```

The plugin will handle decryption and usage of this encrypted data.

If you want to test out to see if your data can be decrypted, then you can
do so with the `decrypt` subcommand. It accepts a YAML file containing the
encrypted data somewhere, and a path within the YAML file to get the data from.
The path is in [dpath format](https://github.com/akesterson/dpath-python).

Using the example from above, if you wanted to decrypt:
```bash
$ victoria encrypt decrypt ./some_config.yaml "plugins/some_plugin/super_secret_access_key"
your-top-secret-access-key
```

As you can see, it prints the decrypted value to the console.

#### KEK rotation
Occasionally you may want to update your KEK to a new version in order to be
more secure. Victoria supports this via key rotation.

If your KEK ever gets out of date, data decryption will fail and you will
see this message instead:
```
Encryption key version xxx is out of date, please re-encrypt with 'victoria encrypt rotate'
```
This means you need to rotate the key of whatever you were trying to decrypt.

This can be done with the `rotate` subcommand of the encrypt plugin. It has
the same arguments as the `decrypt` subcommand: a YAML file containing the
encrypted data somewhere, and a path within the YAML file to get the data from.
The path is in [dpath format](https://github.com/akesterson/dpath-python).

```bash
$ victoria encrypt rotate ./some_config.yaml "plugins/some_plugin/super_secret_access_key"
data: <encrypted data>
key: <encrypted data key>
iv: <the nonce used with the key>
version: <the new key version>
```

It will print out the data encrypted with the new key, and you can now
paste it into the right location in the config file and it will be able
to be decrypted.


### Cloud backends

#### Azure

##### Storage

The Azure storage backend requires an Azure storage account with a blob container.

You can create one like this (with Azure CLI):

```bash
$ az group create --name rg-victoria \
    --location uksouth
$ az storage account create --name {storage-name} \
    --resource-group rg-victoria \
    --location uksouth \
    --kind "StorageV2"
$ az storage container create --name victoria \
    --public-access off
```

This creates a resource group, a storage account within it, and a storage container for Victoria to use. Make sure you replace `{storage-name}` with whatever you want to call your account.

This storage account can be used by putting this in your Victoria config:
```yaml
storage_providers:
  azure:
    connection_string: your-connection-string-here
    container: victoria
```

Make sure you put your storage account name in the `account` field.

In order to get the access key for the container, you can run (with Azure CLI):
```bash
$ az storage account show-connection-string \
    --name stvictoria \
    --resource-group rg-victoria \
    --query "connectionString" \
    -o tsv
```

Obviously this key is a secret, so don't go putting it in source control or otherwise
sharing it with anyone.

##### Encryption

The Azure encryption backend requires an Azure Key Vault with a key, as well as a
service principal to perform actions with the key.

You can create the key vault and key like this (with Azure CLI):
```bash
$ az group create --name rg-victoria \
    --location uksouth
$ az keyvault create --name {keyvault-name} \
    --resource-group rg-victoria \
    --location uksouth \
    --sku standard \
    --enabled-for-template-deployment true
$ az keyvault key create --name keyencryptionkey \
    --vault-name {keyvault-name} \
    --kty RSA \
    --protection software \
    --size 2048
```

Make sure you replace `{keyvault-name}` in the bottom two commands with
whatever you want to call your key vault.

You can create an Azure AD Service Principal to give Victoria access to your
Key Vault like this:
```bash
$ az ad sp create-for-rbac --name VictoriaServicePrincipal
```

Watch the output of this command, you'll need the JSON fields `"tenant"`, 
`"appId"`, and `"password"` for your config file. You can't get the password
back, so make sure you remember it!

Give your new Service Principal the permissions it needs for keys (replacing 
`{your-sp-appid}` with the JSON `"appId"` field you got when creating the SP):
```bash
SP_OBJECT_ID=$(az ad sp show --id {your-sp-appid} --query objectId -o tsv)
az keyvault set-policy --name kv-victoria \
    --object-id $SP_OBJECT_ID \
    --key-permissions get list encrypt decrypt
```

Now finally, add the following to your Victoria config file:
```yaml
encryption_provider:
  provider: azure
  config:
    vault_url: "https://{keyvault-name}.vault.azure.net/"
    key: keyencryptionkey
    tenant_id: your-tenant-id-here
    client_id: your-client-id-here
    client_secret: your-client-secret-here
```

Replacing `{keyvault-name}` with the name of your keyvault, and mapping the
JSON values from the SP creation to the keys here as follows:

- `tenant_id` is `"tenant"` from JSON
- `client_id` is `"appId"` from JSON
- `client_secret` is `"password"` from JSON

Obviously, all this stuff is secret, so don't go putting it in source control or
sharing it with anyone.

Additionally, you can actually leave `tenant_id`, `client_id`, and `client_secret`
out of your config file and specify them in environment variables instead.
These are (respectively): `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET`.


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

Note: you can use any field name inside your plugin schema except `victoria_config`,
as this is reserved for storing the core Victoria config in Plugin configs.

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

#### Accessing core Victoria config from a plugin's config
All plugin config objects will have the core Victoria config injected into them.
Following the above example, within our `hello` function, we could access the
core Victoria config like so:
```python
from pprint import pprint

@click.command()
@click.argument('name', nargs=1, type=str, required=True)
@click.pass_obj
def hello(cfg: HelloConfig, name: str):
    core_config = cfg.victoria_config
    print(f"My logging config is:\n {pprint(core_config.logging_config)}")
```

Every plugin config will have the `victoria_config` field injected into it.
It is of type `victoria.config.Config`. As a result of the injection process,
it is recommended to not use `victoria_config` as a field name in your
schemas, as it is liable to be overwitten.

### Storing secrets in config files

You can use a cloud encryption provider to handle encryption/decryption of
secrets from config files.

Perhaps your plugin accesses some API, and you need the user to specify an
API key in their config file. You wouldn't want them to store this in plaintext,
so you require that it be encrypted in the config file.

Your config schema could be:
```python
from marshmallow import Schema, fields, post_load

from victoria.encryption.schemas import EncryptionEnvelopeSchema, EncryptionEnvelope

class APIPluginConfigSchema(Schema):
    api_key = fields.Nested(EncryptionEnvelopeSchema)

    @post_load
    def create_config(self, data, **kwargs):
        return APIPluginConfig(**data)

class APIPluginConfig:
    def __init__(self, api_key: EncryptionEnvelope) -> None:
        self.api_key = api_key
```

An `EncryptionEnvelope` is a container for encrypted data. Victoria uses [envelope encryption](https://cloud.google.com/kms/docs/envelope-encryption)
to securely store/transmit sensitive data. The `EncryptionEnvelope` object
contains three fields:
- `data`: The sensitive data encrypted with the 'data encryption key' (DEK).
- `key`: The DEK encrypted with a 'key encryption key' (KEK) from your cloud encryption provider.
- `iv`: A 96-bit nonce used for further security.
- `version`: The version of the KEK used. This field is used to check if this envelope was encrypted with an old key.

When a user installs your plugin, they will have to provide these
fields in the plugin config by editing it. The fields can be
easily generated by Victoria itself using the built-in `encrypt` command. The user would run `victoria encrypt data {their-api-key}` with Victoria configured to use a cloud encryption provider, and the `data`, `key`, `iv`, and `version` fields will be printed to stdout in YAML format, ready for pasting into the plugin config file.

To decrypt user-provided sensitive data from an `EncryptionEnvelope` in a plugin config file, use the encryption provider API:
```python
@click.command()
@click.pass_obj
def do_api_thing(cfg: schema.APIPluginConfig):
    provider = cfg.victoria_config.get_encryption()
    decrypted_key = provider.decrypt_str(cfg.api_key)
    if decrypted_key is None:
        # the key was out of date
        raise SystemExit(1)
    conn = some_api.connect(api_key=decrypted_key)
    del decrypted_key  # get rid of it as soon as you don't need it anymore, it's plaintext!
    result = conn.perform_some_api_action()
    print(result.status)
```

Here we're getting the encryption provider from the core Victoria config with `cfg.victoria_config.get_encryption()`. This object is our connection to the cloud encryption service, and has functions to encrypt/decrypt data into envelopes for safe storage.

As we've specified in our config schema that the `api_key` field is an `EncryptionEnvelope`, all we need to do to get the key is use the provider to securely decrypt it: `provider.decrypt_str(cfg.api_key)`.

`decrypt_str()` can return `None` if the key in the envelope is now out of date. It will log that the user needs to rotate the key. Usually what you'll want to
do in this case is simply exit so the user can run `victoria encrypt rotate` on the data and try again.

The result will be the plaintext value we need. We can do whatever we want with it now, just make sure you delete it as soon as you no longer need it anymore, as the longer it's around in memory the more opportunities someone might have to steal your private information!

The encryption provider API provides encryption methods `encrypt()`, and `encrypt_str()` for encrypting data into an `EncryptionEnvelope`, as well as `decrypt()` and `decrypt_str()` for decrypting an `EncryptionEnvelope`. The `*_str()` functions handle `str` data, and the rest handle `bytes` data. All of the decryption functions can return `None` in the event of an outdated key, so please be mindful of that.

Victoria uses a 256-bit AES cipher in Galois-counter mode, with an initialization vector of 96-bits. This is based on advice from [Google](https://cloud.google.com/kms/docs/envelope-encryption#data_encryption_keys) and [NIST](https://csrc.nist.gov/publications/detail/sp/800-38d/final).