from contextlib import nullcontext as does_not_raise

import pytest

from victoria import encryption
from victoria.encryption import azure_provider

from test_encryption_azure import mock_azure_classes


@pytest.mark.parametrize(
    "kind,kwargs,expected,raises",
    [("azure", {
        "vault_url": "",
        "key": "",
        "tenant_id": "",
        "client_id": "",
        "client_secret": ""
    }, azure_provider.AzureEncryptionProvider, does_not_raise()),
     ("unknown", {}, None, pytest.raises(ValueError)),
     ("azure", {
         "vault_url": "",
         "key": "",
         "auth_via_cli": True
     }, azure_provider.AzureEncryptionProvider, does_not_raise())])
def test_make_provider(mock_azure_classes, fs, kind, kwargs, expected, raises):
    with raises:
        provider = encryption.make_provider(kind, **kwargs)
        assert type(provider) == expected