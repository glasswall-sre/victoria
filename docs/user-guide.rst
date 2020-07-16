User Guide
==========

Prerequisites
-------------

- Python 3.6+
- Pip

Installation
------------

.. code-block:: bash

    pip install -U victoria

Stock plugins
-------------

Victoria comes with 3 plugins preinstalled:

- ``config``
  - can be used to print the current config, and get the path to it
- ``store``
  - can be used to interact with cloud storage backends
- ``encrypt``
  - can be used to encrypt data for Victoria to load in config files

Configuration
-------------
Victoria has a YAML config file that it uses to control the main CLI, which can
specify other YAML files (both local and remote) to use to configure plugins.

You can get the path to the config file by running ``victoria config path``.

A quick way to edit your config if you have VSCode installed is by running
``code $(victoria config path)``.

Please note that the config file is not isolated. All installations of Victoria
on the same machine will use the same core config file.

Plugin configuration
^^^^^^^^^^^^^^^^^^^^
Config is in a section of the Victoria YAML config called ``plugins_config``. 

.. code-block:: yaml

    plugins_config:
      some_plugin:
        some_value: 123

Sub-objects of ``plugins_config`` have keys of the same name as the plugins. So
a plugin called ``verb`` would have a key in ``plugins_config`` also called ``verb``.

Additionally, you can specify separate config files for plugins with the
``plugins_config_location`` section of the YAML config, instead of
keeping your config all in the core Victoria config file. You can even use
config files stored in the cloud! To do this, you need to have configured a 
storage provider in your core config. A simple one to use is the ``local``
provider, which just uses a directory on your machine to store config files:

.. code-block:: yaml

    storage_providers:
      local:
        container: C:/victoria_storage


Put that in your core config (you can change the directory to be wherever you
want), and you can now configure a separate config location for ``some_plugin``
in your ``plugins_config_location``:

.. code-block:: yaml

    plugins_config_location:
      some_plugin: local://path/to/the_config_for_some_plugin.yaml


As with ``plugins_config``, the keys are plugin names. The values are of the
format ``{storage-provider-name}://{path-to-config-file}``, where
``{storage-provider-name}`` is a key in the ``storage_providers`` section of your
core config. The ``{storage-provider-name}`` can be called anything if you'd like
it to be.

Victoria will grab it and load it as if it were in ``plugins_config``. 

Please see the 'Cloud storage' and 'Cloud backends' sections of the README for 
setting up a cloud storage provider.

Example
^^^^^^^

.. code-block:: yaml

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
        auth_via_cli: true
        account_name: your-account-name
        container: victoria
      local:
        container: C:/victoria_storage

    # your encryption provider config goes here - again only Azure is supported
    encryption_provider:
      provider: azure
      config:
        vault_url: "https://your-vault.vault.azure.net/"
        key: keyencryptionkey
        auth_via_cli: true

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

Cloud storage
-------------
Victoria can interact with cloud storage backends to get config for plugins!

Say you had a plugin used by a team that had a complex config, and you wanted
to share it so everyone could use the same config. You could store the YAML
config in a cloud storage container, and have everyone point their Victoria
config files at the container for that plugin.

Victoria even comes with a stock plugin called ``store`` that makes it easy to 
store and list files in your cloud storage backends!

Let's go through an example in more detail.

You've made a plugin called ``helpful`` which your team finds useful, but has
quite a complex config file that changes a lot and needs to be shared around.
You've previously had issues with it getting out of date and people having
wrong versions, so you decide to put it in cloud storage instead.

You've already set up an Azure storage backend in your Victoria config.

You make a YAML file containing the config for the plugin (``helpful-config.yaml``),
and you put it in cloud storage by running ``victoria store azure put helpful-config.yaml``.

You then ask your team to configure the same Azure storage backend in their
Victoria config files, and point at the shared config file by putting this
section in their config:

.. code-block:: yaml

    plugins_config_location:
      helpful: "azure://helpful-config.yaml"


They can remove their old config from ``plugins_config``, and now when they run
``helpful`` it will use the config from cloud storage! Easy.

Please note that `plugins_config_location` takes precedence over ``plugins_config``,
so if you have a config specified for the same plugin in both, then only the one
in ``plugins_config_location`` will be loaded.


Cloud encryption
----------------
Victoria can use `envelope encryption <https://cloud.google.com/kms/docs/envelope-encryption>`_
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

.. code-block:: bash

    $ victoria encrypt data "your-top-secret-access-key"
    data: <encrypted data>
    key: <encrypted data key>
    iv: <the nonce used with the key>
    version: <the key version>


You can then paste this directly into a plugin config that needs a secret value,
like this:

.. code-block:: yaml

    plugins_config:
      some_plugin:
        super_secret_access_key:
          data: <encrypted data>
          key: <encrypted data key>
          iv: <the nonce used with the key>
          version: <the key version>


The plugin will handle decryption and usage of this encrypted data.

If you want to test out to see if your data can be decrypted, then you can
do so with the `decrypt` subcommand. It accepts a YAML file containing the
encrypted data somewhere, and a path within the YAML file to get the data from.
The path is in `dpath format <https://github.com/akesterson/dpath-python>`_.

Using the example from above, if you wanted to decrypt:

.. code-block:: bash

    $ victoria encrypt decrypt ./some_config.yaml "plugins/some_plugin/super_secret_access_key"
    your-top-secret-access-key


As you can see, it prints the decrypted value to the console.

KEK rotation
^^^^^^^^^^^^
Occasionally you may want to update your KEK to a new version in order to be
more secure. Victoria supports this via key rotation.

If your KEK ever gets out of date, data decryption will fail and you will
see this message instead:
.. code-block::

    Encryption key version xxx is out of date, please re-encrypt with 'victoria encrypt rotate'


This means you need to rotate the key of whatever you were trying to decrypt.

This can be done with the ``rotate`` subcommand of the encrypt plugin. It has
the same arguments as the ``decrypt`` subcommand: a YAML file containing the
encrypted data somewhere, and a path within the YAML file to get the data from.
The path is in `dpath format <https://github.com/akesterson/dpath-python>`_.

.. code-block:: bash

    $ victoria encrypt rotate ./some_config.yaml "plugins/some_plugin/super_secret_access_key"
    data: <encrypted data>
    key: <encrypted data key>
    iv: <the nonce used with the key>
    version: <the new key version>


It will print out the data encrypted with the new key, and you can now
paste it into the right location in the config file and it will be able
to be decrypted.


Cloud backends
--------------

Azure
^^^^^

An easy way to deploy the Victoria Azure cloud backend is to use Pulumi_.

A Pulumi project that deploys all of the necessary Azure infrastructure can
be found here: https://github.com/glasswall-sre/victoria_cloud_backend

You'll need to add the following sections to your ``victoria.yaml`` config:

.. code-block:: yaml

    storage_providers:
      azure:
        account_name: {storage-name}
        container: victoria
        auth_via_cli: true

    encryption_provider:
      provider: azure
      config:
        vault_url: {vault-url}
        key: keyencryptionkey
        auth_via_cli: true

Where ``{storage-name}`` can be found by running: 
``pulumi stack output storage_account_name``

And ``{vault-url}`` can be found by running:
``pulumi stack output key_vault_url``

.. _Pulumi: https://www.pulumi.com/

Storage
*******

The Azure storage backend requires an Azure storage account with a blob container.

You can create one like this (with Azure CLI):

.. code-block:: bash

    $ az group create --name rg-victoria \
        --location uksouth
    $ az storage account create --name {storage-name} \
        --resource-group rg-victoria \
        --location uksouth \
        --kind "StorageV2"
    $ az storage container create --name victoria \
        --public-access off


This creates a resource group, a storage account within it, and a storage 
container for Victoria to use. Make sure you replace ``{storage-name}`` with 
whatever you want to call your account.

This storage account can be used by putting this in your Victoria config:

.. code-block:: yaml

    storage_providers:
      azure:
        account_name: {storage-name}
        container: victoria
        auth_via_cli: true


Make sure you put your storage account name in the ``account_name`` field.

Setting ``auth_via_cli`` here means that Victoria will piggyback off of the
Azure CLI login on the machine it's running on. As long as you're logged in
with ``az login`` and you have the right IAM permissions you'll be able to
use the storage provider.

Victoria requires 'Storage Blob Data Contributor' permissions for the Service
Principal being used to access the storage account.

You can also connect to blob storage directly with a connection string.

In order to get the connection string for the container, you can run (with Azure CLI):

.. code-block:: bash

    $ az storage account show-connection-string \
        --name stvictoria \
        --resource-group rg-victoria \
        --query "connectionString" \
        -o tsv


Obviously this key is a secret, so don't go putting it in source control or otherwise
sharing it with anyone.

You can put it in your config like so:

.. code-block:: yaml

    storage_providers:
      azure:
        connection_string: {your-connection-string}
        container: victoria


Encryption
**********

The Azure encryption backend requires an Azure Key Vault with a key, as well as a
service principal to perform actions with the key.

You can create the key vault and key like this (with Azure CLI):

.. code-block:: bash

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


Make sure you replace ``{keyvault-name}`` in the bottom two commands with
whatever you want to call your key vault.

Now add the following to your config to use Azure Key Vault as your encryption
provider:

.. code-block:: yaml

    encryption_provider:
      provider: azure
      config:
        vault_url: https://{keyvault-name}.vault.azure.net/
        key: keyencryptionkey
        auth_via_cli: true

Setting ``auth_via_cli`` to ``true`` here allows Victoria to piggyback off of
the Azure CLI login on the system. As long as you're logged into Azure CLI via
``az login`` and the Key Vault's access policy is set up correctly it'll work.

The Service Principal Victoria uses to access Key Vault needs to have the 
following access policy on the Key Vault:

- Key permissions
    - get 
    - list 
    - encrypt 
    - decrypt

Alternatively, if you don't want to authenticate using the Azure CLI, you can
directly use Service Principal details.

You can create an Azure AD Service Principal to give Victoria access to your
Key Vault like this:

.. code-block:: bash

    $ az ad sp create-for-rbac --name VictoriaServicePrincipal


Watch the output of this command, you'll need the JSON fields ``"tenant"``, 
``"appId"``, and ``"password"`` for your config file. You can't get the password
back, so make sure you remember it!

Give your new Service Principal the permissions it needs for keys (replacing 
``{your-sp-appid}`` with the JSON ``"appId"`` field you got when creating the SP):

.. code-block:: bash

    SP_OBJECT_ID=$(az ad sp show --id {your-sp-appid} --query objectId -o tsv)
    az keyvault set-policy --name kv-victoria \
        --object-id $SP_OBJECT_ID \
        --key-permissions get list encrypt decrypt
        

Now finally, add the following to your Victoria config file:

.. code-block:: yaml

    encryption_provider:
      provider: azure
      config:
        vault_url: "https://{keyvault-name}.vault.azure.net/"
        key: keyencryptionkey
        tenant_id: your-tenant-id-here
        client_id: your-client-id-here
        client_secret: your-client-secret-here


Replacing ``{keyvault-name}`` with the name of your keyvault, and mapping the
JSON values from the SP creation to the keys here as follows:

- ``tenant_id`` is ``"tenant"`` from JSON
- ``client_id`` is ``"appId"`` from JSON
- ``client_secret`` is ``"password"`` from JSON

Obviously, all this stuff is secret, so don't go putting it in source control or
sharing it with anyone.

Additionally, you can actually leave ``tenant_id``, ``client_id``, and ``client_secret``
out of your config file and specify them in environment variables instead.
These are (respectively): ``AZURE_TENANT_ID``, ``AZURE_CLIENT_ID``, and ``AZURE_CLIENT_SECRET``.

