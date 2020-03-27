"""victoria.encryption.azure_provider

Implementation of an EncryptionProvider for Azure Key Vault.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import base64
import logging
import os

from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

from .provider import EncryptionProvider, EncryptionEnvelope

ENCRYPTION_ALGORITHM = EncryptionAlgorithm.rsa_oaep_256

TENANT_ID_ENVVAR = "AZURE_TENANT_ID"
CLIENT_ID_ENVVAR = "AZURE_CLIENT_ID"
CLIENT_SECRET_ENVVAR = "AZURE_CLIENT_SECRET"


class AzureEncryptionProvider(EncryptionProvider):
    """An EncryptionProvider implementation for Azure Key Vault.

    To authenticate, please provide Azure AD service principal info as 
    'tenant_id', 'client_id', and 'client_secret' kwargs, or as
    AZURE_TENANT_ID, AZURE_CLIENT_ID, and AZURE_CLIENT_SECRET environment
    variables.

    Attributes:
        tenant_id (str): The tenant ID of the Azure SP to connect with.
        client_id (str): The client ID of the Azure SP to connect with.
        client_secret (str): The client secret of the Azure SP to connect with.
        key_client (KeyClient): Azure Key Vault key client.
        crypto_client (CryptographyClient): Azure Key Vault crypto client.

    Args:
        vault_url (str): The URL of the key vault to connect to.
        key (str): The name of the key encryption key to use for envelope encryption.
        **kwargs: Authentication information.

    Raises:
        TypeError: If authentication information is not provided correctly.
    """
    def __init__(self, vault_url: str, key: str, **kwargs) -> None:
        tenant_id = kwargs.pop("tenant_id", os.getenv(TENANT_ID_ENVVAR))
        client_id = kwargs.pop("client_id", os.getenv(CLIENT_ID_ENVVAR))
        client_secret = kwargs.pop("client_secret",
                                   os.getenv(CLIENT_SECRET_ENVVAR))
        if tenant_id is None or client_id is None or client_secret is None:
            raise TypeError(
                "Please specify tenant_id, client_id, and client_secret "
                "in config or in environment variables as in "
                "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity#service-principal-with-secret"
            )
        cred = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.key_client = KeyClient(vault_url, credential=cred, logger=None)
        self.crypto_client = CryptographyClient(self.key_client.get_key(key),
                                                cred)

    # overrides EncryptionProvider.encrypt()
    def encrypt(self, data: bytes) -> EncryptionEnvelope:
        # encrypt the data locally, generating a data key and a nonce
        ciphertext, data_key, nonce = self._data_encrypt(data)

        # encrypt the data key using the key from the vault
        result = self.crypto_client.encrypt(ENCRYPTION_ALGORITHM, data_key)
        del data_key  # we don't wanna keep this around after we've encrypted it
        encrypted_data_key = result.ciphertext

        # encode to base64 for storage/transmission
        b64_ciphertext = base64.b64encode(ciphertext).decode("utf-8")
        b64_encrypted_data_key = base64.b64encode(encrypted_data_key).decode(
            "utf-8")
        b64_nonce = base64.b64encode(nonce).decode("utf-8")

        return EncryptionEnvelope(b64_ciphertext, b64_encrypted_data_key,
                                  b64_nonce)

    # overrides EncryptionProvider.decrypt()
    def decrypt(self, envelope: EncryptionEnvelope) -> bytes:
        # decode from base64
        ciphertext = base64.b64decode(envelope.data)
        encrypted_data_key = base64.b64decode(envelope.key)
        nonce = base64.b64decode(envelope.iv)

        # decrypt the data key
        result = self.crypto_client.decrypt(ENCRYPTION_ALGORITHM,
                                            encrypted_data_key)
        data_key = result.plaintext

        # decrypt the data locally using the nonce and decrypted data key
        return self._data_decrypt(ciphertext, data_key, nonce)
