from collections import namedtuple

import pytest
from munch import munchify

from victoria.encryption import azure_provider
from victoria.encryption.schemas import EncryptionEnvelope


@pytest.fixture
def mock_azure_classes(monkeypatch):
    MockClientSecretCredential = namedtuple(
        "MockClientSecretCredential",
        ["tenant_id", "client_id", "client_secret"])

    class MockKeyClient:
        def __init__(self, vault_url, **kwargs):
            self.vault_url = vault_url
            pass

        def get_key(self, key, version="one"):
            return munchify({"name": key, "properties": {"version": version}})

    class MockCryptoClient:
        def __init__(self, key_encryption_key, creds):
            pass

        def encrypt(self, algorithm, data):
            # I shouldn't even have to say this, but this isn't real encryption
            return munchify({"ciphertext": data})

        def decrypt(self, algorithm, data):
            return munchify({"plaintext": data})

    monkeypatch.setattr(azure_provider, "ClientSecretCredential",
                        MockClientSecretCredential)
    monkeypatch.setattr(azure_provider, "KeyClient", MockKeyClient)
    monkeypatch.setattr(azure_provider, "CryptographyClient", MockCryptoClient)


def test_provider_init(mock_azure_classes):
    with pytest.raises(TypeError):
        azure_provider.AzureEncryptionProvider(vault_url="", key="")


def test_encrypt_decrypt(mock_azure_classes):
    provider = azure_provider.AzureEncryptionProvider(vault_url="",
                                                      key="key",
                                                      tenant_id="",
                                                      client_id="",
                                                      client_secret="")
    data = b"hello world"
    envelope = provider.encrypt(data)
    decrypted = provider.decrypt(envelope)
    assert decrypted == data


def test_encrypt_decrypt_str(mock_azure_classes):
    provider = azure_provider.AzureEncryptionProvider(vault_url="",
                                                      key="key",
                                                      tenant_id="",
                                                      client_id="",
                                                      client_secret="")
    data = "hello world"
    envelope = provider.encrypt_str(data)
    decrypted = provider.decrypt_str(envelope)
    assert decrypted == data


def test_decrypt_outdated_key(mock_azure_classes, caplog):
    {
        'data': 'JzB8FfI25EOyd3UiihlID6OqdF0=',
        'key': 'ISPnWiRdWTNMQxAk4f/uhdg7H+kUkCSvL80J1/oQQdw=',
        'iv': 'KuO9ImCHeoBzlWIn',
        'version': 'one'
    }
    provider = azure_provider.AzureEncryptionProvider(vault_url="",
                                                      key="key",
                                                      tenant_id="",
                                                      client_id="",
                                                      client_secret="")

    envelope = provider.encrypt_str("test")
    envelope.version = "zero"
    decrypted = provider.decrypt_str(envelope)
    assert decrypted == None
    assert caplog.records[
        0].message == "Encryption key version zero is out of date, please re-encrypt with 'victoria encrypt rotate'"


def test_rotate_key(mock_azure_classes):
    provider = azure_provider.AzureEncryptionProvider(vault_url="",
                                                      key="key",
                                                      tenant_id="",
                                                      client_id="",
                                                      client_secret="")
    envelope = provider.encrypt_str("test")
    envelope.version = "zero"
    rotated_envelope = provider.rotate_key(envelope)
    decrypted = provider.decrypt_str(rotated_envelope)
    assert decrypted == "test"