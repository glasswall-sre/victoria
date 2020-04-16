from contextlib import nullcontext as does_not_raise

import pytest

from victoria import storage
from victoria.storage import azure_provider, local_provider

from test_storage_azure import mock_azure_classes
from test_storage_local import fs


@pytest.mark.parametrize(
    "kind,kwargs,expected,raises",
    [("local", {
        "container": ""
    }, local_provider.LocalStorageProvider, does_not_raise()),
     ("azure", {
         "account": "",
         "credential": "",
         "container": ""
     }, azure_provider.AzureStorageProvider, does_not_raise()),
     ("unknown", {}, None, pytest.raises(ValueError))])
def test_make_provider(mock_azure_classes, fs, kind, kwargs, expected, raises):
    with raises:
        provider = storage.make_provider(kind, **kwargs)
        assert type(provider) == expected