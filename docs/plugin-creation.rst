Plugin Creation
===============

A Victoria plugin is just a Python package with some certain 
requirements/properties.

General
-------

Your package name must start with ``victoria_`` in order for Victoria to 
use it.

For example: ``victoria_pbi``.

``setup.py``
------------
In your ``setup()`` function you need to have ``"victoria"`` in your 
``install_requires``.

For example:

.. code-block:: python

    from setuptools import setup, find_packages

    setup(
        install_requires=[
            "victoria"
        ],
        name="victoria_pbi",
        version="#{TAG_NAME}#",
        description="Victoria plugin to manipulate Azure DevOps PBIs",
        author="Ash Powell",
        author_email="apowell@glasswallsolutions.com",
        packages=find_packages(),
    )


Package structure
-----------------

Your repo should have the following structure as a python package:

::

    - victoria_{plugin_name}/
        - __init__.py
        - some_other_module.py
    - setup.py

``__init__.py``
---------------

In your package's ``__init__.py`` you need to declare a 
:class:`victoria.plugin.Plugin` object called ``plugin`` for Victoria to 
know how to execute your plugin.

A Plugin object has three elements:

- ``name``: The name of the subcommand.
- ``cli``: The 'entry point' function to execute for the subcommand. Should be 
  a `Click <https://click.palletsprojects.com/en/7.x/>`_ command or group.
- ``config_schema``: If your plugin requires config, this is an instance of a 
  `Marshmallow schema <https://marshmallow.readthedocs.io/en/stable/>`_ for 
  your config. Otherwise, if you don't specify it your plugin won't use config, 
  as it defaults to ``None``.

Here is a minimal example of a plugin defined in ``__init__.py``:

.. code-block:: python

    from victoria.plugin import Plugin

    @click.command()
    @click.argument('name', nargs=1, type=str, required=True)
    def hello(name: str):
        print(f"Hello, {name}!")

    plugin = Plugin(name="hello", cli=hello)


When this package is installed, a ``hello`` subcommand will be available to 
Victoria.

You will be able to run it like so:

.. code-block:: bash

    $ victoria hello "world"
    Hello, world!


Obviously, you could specify your CLI entry point function in a separate Python 
module, import that function in ``__init__.py``, and specify ``cli`` as that 
function. This is generally the best practice.

Specifying plugin config
------------------------

You can specify plugin config by setting ``config_schema`` of your 
:class:`victoria.plugin.Plugin` object to be an instance of a 
`Marshmallow schema <https://marshmallow.readthedocs.io/en/stable/>`_.

Config is in a section of the Victoria YAML config called ``plugins_config``. 
Sub-objects of ``plugins_config`` have keys of the same name as the ``name`` parameter
in your :class:`victoria.plugin.Plugin` object in ``__init__.py``. 
So this ``Plugin(name="some_plugin", ...)``
would be in key ``some_plugin`` under ``plugins_config``.

Going by the example of a ``hello`` plugin in the previous section, let's customise
the greeting by allowing a user to specify a custom one in the Victoria config:

.. code-block:: yaml

    plugins_config:
      hello:
        greeting: "Bonjour,"


We need to create a Marshmallow schema for the config, put this in ``__init__.py``:

.. code-block:: python

    from marshmallow import Schema, fields, post_load

    class HelloConfigSchema(Schema):
        greeting = fields.Str(required=True)

        @post_load
        def create_hello_config(self, data, **kwargs):
            return HelloConfig(**data)

    class HelloConfig:
        def __init__(self, greeting: str) -> None:
            self.greeting = greeting


Note: you can use any field name inside your plugin schema except ``victoria_config``,
as this is reserved for storing the core Victoria config in Plugin configs.

And now modify the definition of your :class:`victoria.plugin.Plugin` object 
to include the schema:

.. code-block:: python

    plugin = Plugin(name="hello", cli=hello, config_schema=HelloConfigSchema())


Now we need to pass the config object to the CLI entry point function, we can do this
using Click by adding the ``pass_obj`` decorator and an argument to the function:

.. code-block:: python

    @click.command()
    @click.argument('name', nargs=1, type=str, required=True)
    @click.pass_obj
    def hello(cfg: HelloConfig, name: str):
        print(f"{cfg.greeting} {name}!")


As you can see, we're using our config's ``greeting`` field in the function now.

When you run the plugin, it should now greet the user with the value from the config:

.. code-block:: bash

    $ victoria hello "le monde"
    Bonjour, le monde!


This will also work with Click groups, like so:

.. code-block:: python

    @click.group()
    @click.pass_obj
    def grouped(cfg: HelloConfig):
        pass

    @grouped.command()
    @click.pass_obj
    def subcommand(cfg: HelloConfig):
        pass


Accessing core Victoria config from a plugin's config
-----------------------------------------------------

All plugin config objects will have the core Victoria config injected into them.
Following the above example, within our ``hello`` function, we could access the
core Victoria config like so:

.. code-block:: python

    from pprint import pprint

    @click.command()
    @click.argument('name', nargs=1, type=str, required=True)
    @click.pass_obj
    def hello(cfg: HelloConfig, name: str):
        core_config = cfg.victoria_config
        print(f"My logging config is:\n {pprint(core_config.logging_config)}")


Every plugin config will have the ``victoria_config`` field injected into it.
It is of type :class:`victoria.config.Config`. As a consequence of the injection 
process, it is recommended to not use ``victoria_config`` as a field name in 
your schemas, as it is liable to be overwitten.

Storing secrets in config files
-------------------------------

You can use a cloud encryption provider to handle encryption/decryption of
secrets from config files.

Perhaps your plugin accesses some API, and you need the user to specify an
API key in their config file. You wouldn't want them to store this in plaintext,
so you require that it be encrypted in the config file.

Your config schema could be:

.. code-block:: python

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


:class:`victoria.encryption.schemas.EncryptionEnvelope` is a container for 
encrypted data. Victoria uses `envelope encryption <https://cloud.google.com/kms/docs/envelope-encryption>`_
to securely store/transmit sensitive data. The ``EncryptionEnvelope`` object
contains four fields:

- ``data``: The sensitive data encrypted with the 'data encryption key' (DEK).
- ``key``: The DEK encrypted with a 'key encryption key' (KEK) from your cloud 
  encryption provider.
- ``iv``: A 96-bit nonce used for further security.
- ``version``: The version of the KEK used. This field is used to check if this 
  envelope was encrypted with an old key.

When a user installs your plugin, they will have to provide these
fields in the plugin config by editing it. The fields can be
easily generated by Victoria itself using the built-in ``encrypt`` command. 
The user would run ``victoria encrypt data {their-api-key}`` with Victoria 
configured to use a cloud encryption provider, and the ``data``, ``key``, ``iv``, 
and ``version`` fields will be printed to stdout in YAML format, ready for 
pasting into the plugin config file.

To decrypt user-provided sensitive data from an ``EncryptionEnvelope`` in a 
plugin config file, use the encryption provider API:

.. code-block:: python

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


Here we're getting the encryption provider from the core Victoria config 
with ``cfg.victoria_config.get_encryption()`` 
(:meth:`victoria.config.Config.get_encryption`). The object returned is an
:class:`victoria.encryption.provider.EncryptionProvider`.
This object is our connection 
to the cloud encryption service, and has functions to encrypt/decrypt data 
into envelopes for safe storage.

As we've specified in our config schema that the ``api_key`` field is an 
``EncryptionEnvelope``, all we need to do to get the key is use the provider 
to securely decrypt it: ``provider.decrypt_str(cfg.api_key)``.

:meth:`victoria.encryption.provider.EncryptionProvider.decrypt_str` 
can return ``None`` if the key in the envelope is now out of 
date. It will log that the user needs to rotate the key. Usually what you'll 
want to do in this case is simply exit so the user can run 
``victoria encrypt rotate`` on the data and try again.

The result will be the plaintext value we need. We can do whatever we want 
with it now, just make sure you delete it as soon as you no longer need it 
anymore, as the longer it's around in memory the more opportunities someone 
might have to steal your private information!

The encryption provider API provides encryption methods 
:meth:`victoria.encryption.provider.EncryptionProvider.encrypt` , 
and :meth:`victoria.encryption.provider.EncryptionProvider.encrypt_str` 
for encrypting data into an ``EncryptionEnvelope``, 
as well as 
:meth:`victoria.encryption.provider.EncryptionProvider.decrypt` 
and :meth:`victoria.encryption.provider.EncryptionProvider.decrypt_str`  
for decrypting an 
``EncryptionEnvelope``. The ``*_str()`` functions handle ``str`` data, and the rest 
handle ``bytes`` data. All of the decryption functions can return ``None`` in the 
event of an outdated key, so please be mindful of that.

Victoria uses a 256-bit AES cipher in Galois-counter mode, with an 
initialization vector of 96-bits. This is based on advice from 
`Google <https://cloud.google.com/kms/docs/envelope-encryption#data_encryption_keys>`_ 
and `NIST <https://csrc.nist.gov/publications/detail/sp/800-38d/final>`_.