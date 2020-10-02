"""victoria.encryption.schemas

Marshmallow schemas for the encryption functionality.

Author:
    Sam Gibson 
"""
from marshmallow import Schema, fields, post_load


class EncryptionEnvelopeSchema(Schema):
    """Marshmallow schema for an EncryptionEnvelope.

    Fields:
        data (str): The base64-encoded encrypted data.
        key (str): The base64-encoded encrypted data encryption key.
        iv (str): The base64-encoded nonce.
        version (str): The version of the key encryption key used.
    """
    data = fields.Str()
    key = fields.Str()
    iv = fields.Str()
    version = fields.Str()

    @post_load
    def make_encryption_envelope(self, data, **kwargs):
        #pylint: disable=unused-argument
        return EncryptionEnvelope(**data)


class EncryptionEnvelope:
    """Stores data that has been envelope encrypted.

    Attributes:
        data (str): The base64-encoded encrypted data.
        key (str): The base64-encoded encrypted data encryption key.
        iv (str): The base64-encoded nonce.
        version (str): The version of the key encryption key used.

    See:
        https://cloud.google.com/kms/docs/envelope-encryption
    """
    def __init__(self, data: str, key: str, iv: str, version: str) -> None:
        self.data = data
        self.key = key
        self.iv = iv
        self.version = version


class EncryptionProviderConfigSchema(Schema):
    """Marshmallow schema for the encryption provider config in Victoria core
    config.

    Fields:
        provider (str): The type of the provider.
        config (Mapping[str, str]): Params to pass to the constructor of the
            encryption provider implementation.
    """
    provider = fields.Str(required=True)
    config = fields.Mapping(keys=fields.Str(), values=fields.Raw(), missing={})

    @post_load
    def make_encryption_provider_config(self, data, **kwargs):
        #pylint: disable=unused-argument
        return EncryptionProviderConfig(**data)


class EncryptionProviderConfig:
    """Stores config for Victoria's encryption providing functionality.

    Attributes:
        provider (str): The type of the provider.
        config (Mapping[str, str]): Params to pass to the constructor of the
            encryption provider implementation.
    """
    def __init__(self, provider: str, config: dict) -> None:
        self.provider = provider
        self.config = config

    @classmethod
    def to_yaml(cls, dumper, data):
        #pylint: disable=unused-argument
        return vars(data)