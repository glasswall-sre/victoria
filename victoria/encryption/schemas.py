from typing import Mapping

from marshmallow import Schema, fields, post_load


class EncryptionEnvelopeSchema(Schema):
    data = fields.Str()
    key = fields.Str()
    iv = fields.Str()

    @post_load
    def make_encryption_envelope(self, data, **kwargs):
        return EncryptionEnvelope(**data)


class EncryptionEnvelope:
    def __init__(self, data: str, key: str, iv: str) -> None:
        self.data = data
        self.key = key
        self.iv = iv


class EncryptionProviderConfigSchema(Schema):
    provider = fields.Str()
    config = fields.Mapping(keys=fields.Str(), values=fields.Str(), missing={})

    @post_load
    def make_encryption_provider_config(self, data, **kwargs):
        return EncryptionProviderConfig(**data)


class EncryptionProviderConfig:
    def __init__(self, provider: str, config: Mapping[str, str]) -> None:
        self.provider = provider
        self.config = config